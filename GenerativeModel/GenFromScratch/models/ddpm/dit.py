"""
DDPM DiT backbone (tiny version) —— Peebles & Xie, 2022 "Scalable Diffusion
Models with Transformers"

对外接口和 UNet 完全一致 (由 GaussianDiffusion 调用):
    model(x_t, t) -> noise_pred
    - x_t: (B, in_channels, H, W)
    - t:   (B,) long
    - 返回: (B, out_channels, H, W)

整体流程 (默认 image_size=64, patch_size=4, hidden_size=256, depth=8):
    (B, 3, 64, 64)
      │ PatchEmbed: Conv2d(k=4, s=4) + flatten + transpose
      ▼
    (B, 256, 256)         # 256 个 patch token, 每个 hidden_size 维
      │ + pos_embed (learnable)
      │
      │  t (B,)  ──SinEmbed──► MLP ──► t_emb (B, 256)
      │
      ▼  DiTBlock × depth
    (B, 256, 256)
      │ FinalLayer: AdaLN + Linear(256 -> 4*4*3)
      ▼
    (B, 256, 48)
      │ Unpatchify
      ▼
    (B, 3, 64, 64)

关键设计: AdaLN-Zero
    普通 Transformer Block: x = x + Attn(LN(x));  x = x + FFN(LN(x))
    DiT Block:
        shift, scale, gate  ← MLP(t_emb)   # 6 组 (Attn 3 + FFN 3)
        x = x + gate_a * Attn(modulate(LN(x), shift_a, scale_a))
        x = x + gate_f * FFN (modulate(LN(x), shift_f, scale_f))

    其中 modulate(x, shift, scale) = x * (1 + scale) + shift.

    "Zero" 是指 adaLN_mlp 的输出层权重/偏置 zero-init, 使得:
        初始 scale = shift = 0, gate = 0
        -> modulate = identity, 且 block 残差支路被 gate 门控为 0
        -> 整个 block 起始 = identity, 训练稳定开始
    这个初始化是 DiT 论文的核心技巧之一, 严格等价于 "Fixup" 思路.
"""

from typing import Optional

import torch
import torch.nn as nn

from models.ddpm.unet import SinusoidalTimeEmbedding


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

def modulate(x: torch.Tensor, shift: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
    """
    AdaLN 调制: 把 (B, D) 的 shift/scale 广播到 (B, N, D) 上.

    使用 (1 + scale) 而不是 scale 的原因: 零初始化时 scale=0 让结果恰好 = x (identity),
    避免训练一开始就把 feature 乘成 0.
    """
    # shift, scale: (B, D) -> (B, 1, D) 以便沿 token 维度广播
    return x * (1.0 + scale.unsqueeze(1)) + shift.unsqueeze(1)


# ---------------------------------------------------------------------------
#  Input: PatchEmbed
# ---------------------------------------------------------------------------

class PatchEmbed(nn.Module):
    """
    图像 → patch token:  (B, C, H, W) -> (B, N, D),  N = (H/P) * (W/P)

    实现用 Conv2d(kernel=P, stride=P, padding=0) 一步搞定 "切 patch + 线性映射":
        - kernel=stride=P: 不重叠切分
        - out_channels=D: 每个 patch 直接投影到 hidden_size
        - 等价于 reshape 到 (B, N, P*P*C) 再过 Linear(P*P*C, D),
          但 Conv2d 实现更简洁, 计算量完全一致.
    """

    def __init__(self, image_size: int, patch_size: int, in_channels: int, dim: int):
        super().__init__()
        assert image_size % patch_size == 0, (
            f"image_size {image_size} must be divisible by patch_size {patch_size}"
        )
        self.num_patches = (image_size // patch_size) ** 2
        self.proj = nn.Conv2d(in_channels, dim, kernel_size=patch_size, stride=patch_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # (B, C, H, W) -> (B, D, H/P, W/P) -> (B, D, N) -> (B, N, D)
        x = self.proj(x)
        x = x.flatten(2).transpose(1, 2)
        return x


# ---------------------------------------------------------------------------
#  Self-Attention (sequence version, 和 UNet 里空间版的 AttnBlock 区分)
# ---------------------------------------------------------------------------

class SelfAttention(nn.Module):
    """
    标准多头自注意力, 作用在 token 序列上.

    与 UNet/AttnBlock 的区别:
        UNet AttnBlock: 输入 (B, C, H, W), 内部 flatten 成 (B, C, H*W), 再做 attn
        DiT SelfAttention: 输入天生就是 (B, N, D), 结构更干净
    """

    def __init__(self, dim: int, num_heads: int):
        super().__init__()
        assert dim % num_heads == 0, f"dim {dim} must be divisible by num_heads {num_heads}"
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5

        # 合并 Q/K/V 的投影层, 一次矩乘搞定 3 个投影
        self.qkv = nn.Linear(dim, dim * 3, bias=True)
        self.proj = nn.Linear(dim, dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, N, D)
        B, N, D = x.shape
        # (B, N, 3*D) -> (B, N, 3, nh, hd) -> (3, B, nh, N, hd)
        qkv = self.qkv(x).reshape(B, N, 3, self.num_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)
        q, k, v = qkv[0], qkv[1], qkv[2]    # 各 (B, nh, N, hd)

        # einsum 风格与 UNet AttnBlock 保持一致 (区别: 那里是 channel-first 的
        # (B, nh, hd, N), 所以用 "bhdn,bhdm->bhnm";
        # 这里是 token-first 的 (B, nh, N, hd), 用 "bhnd,bhmd->bhnm").
        #
        # QK^T / √d:  d 相同 → 点积求和消掉; n,m 保留 → 两两配对
        attn = torch.einsum("bhnd,bhmd->bhnm", q, k) * self.scale  # (B, nh, N, N)
        attn = attn.softmax(dim=-1)                                 # 沿 m 维归一化

        # attn @ V:  m 相同 → 按权重求和消掉; n,d 保留
        out = torch.einsum("bhnm,bhmd->bhnd", attn, v)              # (B, nh, N, hd)

        # 合多头: (B, nh, N, hd) -> (B, N, nh, hd) -> (B, N, D)
        out = out.transpose(1, 2).reshape(B, N, D)
        return self.proj(out)


# ---------------------------------------------------------------------------
#  DiT Block: AdaLN-Zero 风格
# ---------------------------------------------------------------------------

class DiTBlock(nn.Module):
    """
    一个 DiT Transformer block, 包含:
        - LayerNorm1  (elementwise_affine=False: γ/β 由 AdaLN 提供, 不自带)
        - Self-Attention
        - LayerNorm2  (同上)
        - FFN (Linear -> GELU -> Linear, 扩展比 mlp_ratio)
        - AdaLN MLP: t_emb (B, D) -> 6*D 切成 6 组 shift/scale/gate

    forward:
        shift_a, scale_a, gate_a, shift_f, scale_f, gate_f = AdaLN_MLP(t_emb).chunk(6, -1)
        x = x + gate_a * Attn(modulate(LN1(x), shift_a, scale_a))
        x = x + gate_f * FFN (modulate(LN2(x), shift_f, scale_f))

    零初始化:
        把 adaLN_mlp 的输出层权重/偏置置零, 使得训练初始时 gate=shift=scale=0,
        整个 block 恰好是 identity, 只让 skip path 起作用, 避免初期破坏特征.
    """

    def __init__(self, dim: int, num_heads: int, mlp_ratio: float = 4.0):
        super().__init__()

        # 去掉 LayerNorm 自带的 γ/β, 我们用 AdaLN 动态提供
        self.norm1 = nn.LayerNorm(dim, elementwise_affine=False, eps=1e-6)
        self.attn = SelfAttention(dim, num_heads)

        self.norm2 = nn.LayerNorm(dim, elementwise_affine=False, eps=1e-6)
        hidden = int(dim * mlp_ratio)
        self.ffn = nn.Sequential(
            nn.Linear(dim, hidden),
            nn.GELU(approximate="tanh"),
            nn.Linear(hidden, dim),
        )

        # 一次性预测 6 个向量 (Attn 的 shift/scale/gate + FFN 的 shift/scale/gate)
        self.adaLN_mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(dim, 6 * dim, bias=True),
        )
        # Zero init: 初始 block = identity
        nn.init.zeros_(self.adaLN_mlp[-1].weight)
        nn.init.zeros_(self.adaLN_mlp[-1].bias)

    def forward(self, x: torch.Tensor, t_emb: torch.Tensor) -> torch.Tensor:
        # t_emb: (B, D) -> (B, 6*D) -> 6 * (B, D)
        shift_a, scale_a, gate_a, shift_f, scale_f, gate_f = (
            self.adaLN_mlp(t_emb).chunk(6, dim=-1)
        )

        # 残差 1: Self-Attention 支路
        #   gate 在最后相乘 (形状 (B, 1, D)), gate=0 时支路被 mute
        x = x + gate_a.unsqueeze(1) * self.attn(
            modulate(self.norm1(x), shift_a, scale_a)
        )
        # 残差 2: FFN 支路
        x = x + gate_f.unsqueeze(1) * self.ffn(
            modulate(self.norm2(x), shift_f, scale_f)
        )
        return x


# ---------------------------------------------------------------------------
#  Final Layer: AdaLN + Linear + Unpatchify (在 DiT 主体 forward 里做 unpatchify)
# ---------------------------------------------------------------------------

class FinalLayer(nn.Module):
    """
    输出头: 把 (B, N, D) 映射成 (B, N, P*P*out_channels).

    仍然用 AdaLN 调制, 但只需要 shift/scale (不需要 gate, 因为后面不再有残差, 且
    输出层自身 zero-init, 起始就是 0).
    """

    def __init__(self, dim: int, patch_size: int, out_channels: int):
        super().__init__()
        self.norm = nn.LayerNorm(dim, elementwise_affine=False, eps=1e-6)
        self.linear = nn.Linear(dim, patch_size * patch_size * out_channels)

        self.adaLN_mlp = nn.Sequential(
            nn.SiLU(),
            nn.Linear(dim, 2 * dim, bias=True),    # 只预测 shift, scale
        )
        # Zero init: 初始输出 noise_pred = 0 的张量 (等价于 "什么都没预测"),
        # 让 diffusion loss 的梯度从 0 状态开始, 稳定训练.
        nn.init.zeros_(self.adaLN_mlp[-1].weight)
        nn.init.zeros_(self.adaLN_mlp[-1].bias)
        nn.init.zeros_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)

    def forward(self, x: torch.Tensor, t_emb: torch.Tensor) -> torch.Tensor:
        shift, scale = self.adaLN_mlp(t_emb).chunk(2, dim=-1)
        x = modulate(self.norm(x), shift, scale)
        return self.linear(x)    # (B, N, P*P*out_ch)


# ---------------------------------------------------------------------------
#  DiT 主体
# ---------------------------------------------------------------------------

class DiT(nn.Module):
    """
    Diffusion Transformer, 对齐 UNet 的对外接口.

    Args:
        image_size:   输入图像边长 (HxW 相同)
        patch_size:   patch 边长, 必须整除 image_size
        in_channels / out_channels: 图像通道数 (一般都 = 3)
        hidden_size:  Transformer 维度 D
        depth:        DiTBlock 的个数
        num_heads:    Self-Attention 头数, 必须整除 hidden_size
        mlp_ratio:    FFN 的扩展比例 (hidden = dim * mlp_ratio)

    参数量估算 (忽略 LN / bias 这些小头):
        PatchEmbed:           P²·C·D
        每个 DiTBlock:        4D² (Attn qkv+proj) + 2·mlp_ratio·D² (FFN)
                            + 6D² (AdaLN MLP)           ≈  16 D²
        FinalLayer:           D·(P²·C) + 2D² (AdaLN)

        默认 tiny: D=256, depth=8 -> 主体 ≈ 8 * 16 * 256² ≈ 8.4 M
        加上 PatchEmbed / FinalLayer / pos_emb / time_embed ≈ 10 M 量级.
    """

    def __init__(
        self,
        image_size: int = 64,
        patch_size: int = 4,
        in_channels: int = 3,
        out_channels: int = 3,
        hidden_size: int = 256,
        depth: int = 8,
        num_heads: int = 4,
        mlp_ratio: float = 4.0,
    ):
        super().__init__()
        assert image_size % patch_size == 0
        self.image_size = image_size
        self.patch_size = patch_size
        self.out_channels = out_channels
        self.grid_size = image_size // patch_size
        self.num_patches = self.grid_size ** 2

        # --- 输入 ---
        self.patch_embed = PatchEmbed(image_size, patch_size, in_channels, hidden_size)
        # 可学习位置编码 (也可以用 fixed 2D sincos, 这里用 learnable 更简单)
        self.pos_embed = nn.Parameter(torch.zeros(1, self.num_patches, hidden_size))

        # --- Time embedding: 与 UNet 共用, 保证 sin/cos 频率集合一致 ---
        self.time_embed = nn.Sequential(
            SinusoidalTimeEmbedding(hidden_size),
            nn.Linear(hidden_size, hidden_size),
            nn.SiLU(),
            nn.Linear(hidden_size, hidden_size),
        )

        # --- Transformer 主体 ---
        self.blocks = nn.ModuleList([
            DiTBlock(hidden_size, num_heads, mlp_ratio) for _ in range(depth)
        ])

        # --- 输出头 ---
        self.final = FinalLayer(hidden_size, patch_size, out_channels)

        # --- 初始化 ---
        # pos_embed 用小方差 truncated normal (ViT 标准)
        nn.init.trunc_normal_(self.pos_embed, std=0.02)
        # PatchEmbed 的 Conv2d 用 Kaiming (把 conv 视作 patch-wise linear)
        w = self.patch_embed.proj.weight.data
        nn.init.xavier_uniform_(w.view(w.shape[0], -1))
        nn.init.zeros_(self.patch_embed.proj.bias)

    def unpatchify(self, x: torch.Tensor) -> torch.Tensor:
        """
        (B, N, P*P*C) -> (B, C, H, W)

        索引含义:
            x[b, n, k] 中:
                n = patch_row * G + patch_col      (G = grid_size = H/P)
                k = ch * P*P + in_row * P + in_col

            H 方向坐标 = patch_row * P + in_row
            W 方向坐标 = patch_col * P + in_col

        实现: reshape 出所有索引维, 然后 permute 到 (B, C, H, W) 的语义顺序.
        """
        B = x.shape[0]
        P = self.patch_size
        C = self.out_channels
        G = self.grid_size

        # (B, N, P*P*C) -> (B, G, G, P, P, C)
        x = x.reshape(B, G, G, P, P, C)
        # 把 C 放到最前 (排在 B 后), H/W 各由 (G, P) 拼成
        # (B, G_row, G_col, P_row, P_col, C) -> (B, C, G_row, P_row, G_col, P_col)
        x = x.permute(0, 5, 1, 3, 2, 4).contiguous()
        # (B, C, G*P, G*P) = (B, C, H, W)
        x = x.reshape(B, C, G * P, G * P)
        return x

    def forward(self, x: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        # x: (B, C, H, W), t: (B,) long

        # 1) patch + 位置编码
        tokens = self.patch_embed(x) + self.pos_embed    # (B, N, D)

        # 2) time embedding, 一次性算好供所有 block 复用
        t_emb = self.time_embed(t)                       # (B, D)

        # 3) Transformer 主体
        for blk in self.blocks:
            tokens = blk(tokens, t_emb)

        # 4) 输出头 + 还原成图像
        patches = self.final(tokens, t_emb)              # (B, N, P*P*C)
        return self.unpatchify(patches)                  # (B, C, H, W)
