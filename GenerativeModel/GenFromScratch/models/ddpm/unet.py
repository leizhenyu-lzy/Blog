"""
DDPM UNet backbone (tiny version)

与 diffusion.py 解耦, 对外接口约定:
    model(x_t, t) -> noise_pred
    - x_t: (B, in_channels, H, W)
    - t:   (B,) long
    - 返回: (B, out_channels, H, W)

结构概览 (默认 image_size=64, base_channels=32, channel_mult=[1,2,2,2]):
    分辨率:   64 -> 32 -> 16 -> 8
    通道:     32 -> 64 -> 64 -> 64

    Time embedding:
        Sinusoidal(base) -> Linear -> SiLU -> Linear   (time_emb_dim=128)

    Down path, 4 stages, 每个 stage:
        num_res_blocks 个 ResBlock (每个 ResBlock 内部注入 time)
        [AttnBlock, 仅当 当前分辨率 ∈ attn_resolutions]
        Downsample (最后一个 stage 除外)

    Mid:
        ResBlock -> AttnBlock -> ResBlock

    Up path, 镜像 4 stages, 每个 stage:
        num_res_blocks + 1 个 ResBlock (每个 block 先 concat 一个 skip, 再 ResBlock)
        [AttnBlock, 若启用]
        Upsample (最顶层 stage 除外)

    Head:
        GroupNorm -> SiLU -> Conv3x3(base_channels -> out_channels)

Skip 机制:
    Down 每做一次 ResBlock / Downsample, 将输出压栈; init_conv 的输出也作为第一个 skip 压栈。
    Up 每个 ResBlock 之前, 从栈顶 pop 一个 skip 与当前特征沿通道 concat 后再进 ResBlock。
    总 skip 数 = 1 (init) + num_res_blocks*num_stages + (num_stages-1)
              = (num_res_blocks+1) * num_stages  (正好被 up path 消耗光)
"""

import math
from typing import List

import torch
import torch.nn as nn
import torch.nn.functional as F


class SinusoidalTimeEmbedding(nn.Module):
    """
    正余弦时间步编码: 整数 t (B,) -> 连续向量 (B, dim)

    频率集合 (对数均匀分布, 恰好覆盖 [1, 1/10000]):
        ω_k = exp(-log(10000) / (half-1) * k),   k = 0, 1, ..., half-1

    输出排列 (DDPM 官方 & 主流扩散库的 concat 写法, 而非 Transformer 原论文的 sin/cos 交替):
        emb[t, k]        = sin(t * ω_k),  k = 0..half-1
        emb[t, half + k] = cos(t * ω_k),  k = 0..half-1

    为什么 concat 也可以 (不必严格 sin/cos 交替):
        两种排列信息完全等价 —— 频率集合相同, 每个频率的 sin/cos 都有;
        区别只在维度顺序。下游是 nn.Linear (全连接), 对输入维度顺序不敏感,
        权重会自动学到正确组合。Concat 版更简洁、少一次 reshape,
        是 DDPM 官方代码与 Diffusers / lucidrains 的统一写法。

    为什么分母是 (half-1) 而不是 half:
        想让频率从 ω_0 = 1 (k=0) 精确覆盖到 ω_{half-1} = 1/10000 (k=half-1),
        需要 freq_log * (half-1) = log(10000) => freq_log = log(10000) / (half-1)。
        若用 half 作分母, 最高频会停在 1/10000^((half-1)/half), 差一步到不了 1/10000 边界。
    """

    def __init__(self, dim: int):
        super().__init__()
        # dim > 2: 保证 half > 1, 避免 half-1 = 0 除零;
        # 同时实践中 time_emb 维度都远大于 2, 不影响真实使用
        assert dim % 2 == 0 and dim > 2, (
            f"dim must be even and > 2 for sin/cos embedding, got {dim}"
        )
        self.dim = dim

    def forward(self, t: torch.Tensor) -> torch.Tensor:
        # t: (B,) long, return (B, dim)
        half = self.dim // 2
        freq_log = math.log(10000) / (half - 1)  # half - 1: 让 频率 freqs 精确覆盖 [1, 1/10000]
        freqs = torch.exp(
            -freq_log * torch.arange(half, device=t.device, dtype=torch.float32)
        )
        args = t.float()[:, None] * freqs[None, :]          # (B, half)
        return torch.cat([torch.sin(args), torch.cos(args)], dim=-1)  # (B, dim)


class ResBlock(nn.Module):
    """
    ResBlock 空间尺寸不变，只改变通道

    DDPM 经典 ResBlock, 时间条件通过加法注入:

        h = Conv3x3( SiLU(GN(x)) )
        h = h + time_mlp(SiLU(t_emb))[:, :, None, None]      # 空间广播加
        h = Conv3x3( Dropout(SiLU(GN(h))) )
        return h + skip(x)                                    # in_ch != out_ch 时 skip 用 1x1 Conv
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        time_emb_dim: int,
        dropout: float = 0.0,
    ):
        super().__init__()
        self.group_norm1 = nn.GroupNorm(8, in_channels)
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, padding=1)

        self.time_mlp = nn.Linear(time_emb_dim, out_channels)

        self.group_norm2 = nn.GroupNorm(8, out_channels)
        self.dropout = nn.Dropout(dropout)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1)

        if in_channels != out_channels:
            self.skip = nn.Conv2d(in_channels, out_channels, 1)
        else:
            self.skip = nn.Identity()

    def forward(self, x: torch.Tensor, t_emb: torch.Tensor) -> torch.Tensor:
        h = self.conv1(F.silu(self.group_norm1(x)))
        # time_mlp(t_emb): (B, out_channels) -> 空间上广播加
        h = h + self.time_mlp(F.silu(t_emb))[:, :, None, None]  # None None 等价于 unsqueeze(-1).unsqueeze(-1)
        h = self.conv2(self.dropout(F.silu(self.group_norm2(h))))
        return h + self.skip(x)


class AttnBlock(nn.Module):
    """
    AttnBlock 空间尺寸不变，通道数不变，只改变注意力机制

    空间 self-attention: 把 (B, C, H, W) 展平成 H*W 个 C 维 token, 走多头点积注意力

    复杂度 O((H*W)^2 * C), 只应该在低分辨率处使用

    在特定分辨率有，down/up path 对称出现
    """

    def __init__(self, channels: int, num_heads: int = 4):
        super().__init__()
        assert channels % num_heads == 0, (
            f"channels ({channels}) must be divisible by num_heads ({num_heads})"
        )
        self.num_heads = num_heads
        self.head_dim = channels // num_heads
        self.scale = self.head_dim ** -0.5

        self.group_norm = nn.GroupNorm(8, channels)
        # conv2d : 每个 (h, w) 位置独立跑一个 Linear(C, 3C)
        self.qkv = nn.Conv2d(channels, channels * 3, 1)  # 1x1 卷积，把通道数分成 3 份，分别作为 Q、K、V
        self.proj = nn.Conv2d(channels, channels, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, C, H, W = x.shape
        h = self.group_norm(x)
        q, k, v = self.qkv(h).chunk(3, dim=1)  # 沿通道维 dim=1 把结果平均切成 3 份，各 (B, C, H, W)，qkv_out (B, 3*C, H, W)

        # (B, C, H, W) -> (B, num_heads, head_dim, H*W)
        def split_heads(t):
            return t.view(B, self.num_heads, self.head_dim, H * W)

        q, k, v = map(split_heads, (q, k, v))

        # Einstein Summation Convention (爱因斯坦求和约定):
        #   相同字母 → 对齐; 在输入里出现但输出里没有 → 沿该维求和消掉; 输出里出现 → 保留
        #
        # QK^T / √d: Q 的每个 token 和 K 的每个 token 两两点积
        #   q: (B, nh, hd, N)   k: (B, nh, hd, N)        # N = H*W; n ≠ m 表示两套独立 token 索引
        #   "bhdn,bhdm->bhnm": d 相同(点积求和消掉), n/m 保留(两两配对)
        #   → attn: (B, nh, N, N)
        attn = torch.einsum("bhdn,bhdm->bhnm", q, k) * self.scale
        attn = attn.softmax(dim=-1)  # 沿 m 维归一化: 每个 n 看所有 m 的权重和 = 1

        # attn · V: 用权重对 V 的各 token 加权求和
        #   attn: (B, nh, N, N)   v: (B, nh, hd, N)
        #   "bhnm,bhdm->bhdn": m 相同(加权求和消掉), n 保留(每个 query 输出一个向量), d 保留
        #   → out: (B, nh, hd, N) = (B, num_heads, head_dim, H*W)
        out = torch.einsum("bhnm,bhdm->bhdn", attn, v)
        out = out.reshape(B, C, H, W)                    # 合并多头 → (B, C, H, W)
        return x + self.proj(out)                        # Conv1x1 融合多头 + 残差


class Downsample(nn.Module):
    """stride-2 3x3 卷积下采样"""

    def __init__(self, channels: int):
        super().__init__()
        self.conv = nn.Conv2d(channels, channels, 3, stride=2, padding=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.conv(x)


class Upsample(nn.Module):
    """最近邻上采样 + 3x3 卷积 (避开 ConvTranspose 的棋盘效应)"""

    def __init__(self, channels: int):
        super().__init__()
        self.conv = nn.Conv2d(channels, channels, 3, padding=1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.interpolate(x, scale_factor=2, mode="nearest")
        return self.conv(x)


class UNet(nn.Module):
    def __init__(
        self,
        image_size: int = 64,
        in_channels: int = 3,  # RGB
        out_channels: int = 3,  # 一般 = in_channels, 需要预测 同形状的噪声
        base_channels: int = 32,  # 基础通道数
        channel_mult: List[int] = None,  # 每个 stage 通道倍率
        num_res_blocks: int = 2,  # 每个 stage 的 ResBlock 数量
        attn_resolutions: List[int] = None,  # 在哪些空间分辨率插入 self-attention
        time_emb_dim: int = 128,  # 在每个 ResBlock 里被加到特征图上
        num_heads: int = 4,
        dropout: float = 0.0,
    ):
        super().__init__()
        if channel_mult is None:
            channel_mult = [1, 2, 2, 2]
        if attn_resolutions is None:
            attn_resolutions = [16, 8]

        self.num_stages = len(channel_mult)  # 每个 stage 处理一种分辨率，stage 之间通过 Downsample 缩 2×
        self.num_res_blocks = num_res_blocks  # 每个 stage 的 ResBlock 数量

        # stage i 操作的通道数 & 分辨率
        stage_channels = [base_channels * m for m in channel_mult]
        stage_res = [image_size >> i for i in range(self.num_stages)]  # >> 右移运算符

        # --- Time embedding ---
        self.time_embed = nn.Sequential(
            SinusoidalTimeEmbedding(base_channels),
            nn.Linear(base_channels, time_emb_dim),
            nn.SiLU(),
            nn.Linear(time_emb_dim, time_emb_dim),
        )  # 每次 forward 调用，算出 time_emb_dim 维的 embedding，给所有 ResBlock 共用

        # --- Init conv ---
        self.init_conv = nn.Conv2d(in_channels, base_channels, 3, padding=1)

        # UNet 的 skip connection，encoder 每层的输出被传到对称位置的 decoder，和 decoder 特征 concat
        # 追踪 down path 中每个将要被压栈的 tensor 的通道数, 供 up path 构造用
        skip_channels: List[int] = [base_channels]          # init_conv 的输出

        # --- Down path ---
        # 每个 stage 存 (ModuleList(ResBlock, AttnOrIdentity), Downsample/Identity)
        self.down_stages = nn.ModuleList()
        ch_in = base_channels
        for i, ch_out in enumerate(stage_channels):
            use_attn = stage_res[i] in attn_resolutions  # 是否在当前 stage 插入 self-attention

            blocks = nn.ModuleList()
            for j in range(num_res_blocks):
                res_block = ResBlock(ch_in, ch_out, time_emb_dim, dropout)
                attn = AttnBlock(ch_out, num_heads) if use_attn else nn.Identity()
                blocks.append(nn.ModuleList([res_block, attn]))
                skip_channels.append(ch_out)  # ResBlock 的输出
                ch_in = ch_out

            # 最后一个 stage 不进行 Downsample
            is_last = (i == self.num_stages - 1)
            if not is_last:
                down_sample = Downsample(ch_out)
                skip_channels.append(ch_out)  # Downsample 的输出
            else:
                down_sample = nn.Identity()

            self.down_stages.append(nn.ModuleList([blocks, down_sample]))

        # --- Mid ---  UNet 的 瓶颈层 (bottleneck)
        # 纯粹是特征变换，不做任何形状变化，不改变 shape，没有 Downsample / Upsample
        # 永远有 attention，不参与 skip stack
        mid_ch = stage_channels[-1]
        self.mid_res1 = ResBlock(mid_ch, mid_ch, time_emb_dim, dropout)
        self.mid_attn = AttnBlock(mid_ch, num_heads)
        self.mid_res2 = ResBlock(mid_ch, mid_ch, time_emb_dim, dropout)

        # --- Up path (反向遍历 stage) ---
        self.up_stages = nn.ModuleList()
        ch_in_up = mid_ch                                    # mid 的输出通道
        for i in reversed(range(self.num_stages)):
            ch_out = stage_channels[i]
            use_attn = stage_res[i] in attn_resolutions

            blocks = nn.ModuleList()
            for j in range(num_res_blocks + 1):              # up path 每个 stage 比 down path 多 1 个 ResBlock
                skip_ch = skip_channels.pop()                # 对应 down path 最近一次压栈的通道
                res_block = ResBlock(
                    ch_in_up + skip_ch, ch_out, time_emb_dim, dropout  # 输入是 down path 的输出和 skip connection 的输出 concat
                )
                attn = AttnBlock(ch_out, num_heads) if use_attn else nn.Identity()
                blocks.append(nn.ModuleList([res_block, attn]))
                ch_in_up = ch_out

            is_top = (i == 0)  # 最顶层 stage 不进行 Upsample
            up_sample = Upsample(ch_out) if not is_top else nn.Identity()
            self.up_stages.append(nn.ModuleList([blocks, up_sample]))

        assert len(skip_channels) == 0, (
            f"Unmatched skip channels remaining: {skip_channels}"
        )

        # --- Head ---
        self.out_norm = nn.GroupNorm(8, base_channels)
        self.out_conv = nn.Conv2d(base_channels, out_channels, 3, padding=1)

    def forward(self, x_t: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x_t: (B, in_channels, H, W) 加噪后的图片, 值域 [-1, 1] (训练时) 或 随噪声分布 (采样时)
            t:   (B,) long, 时间步 0 ~ T-1
        Returns:
            (B, out_channels, H, W) 预测的噪声
        """
        t_emb = self.time_embed(t)                           # (B, time_emb_dim)

        h = self.init_conv(x_t)
        skips = [h]                                          # 压栈第一个 skip

        # Down path
        for i, (blocks, down_sample) in enumerate(self.down_stages):
            for res_block, attn in blocks:
                h = res_block(h, t_emb)
                h = attn(h)  # 如果 不需要 attention，则 attn 是 nn.Identity()
                skips.append(h)
            is_last = (i == self.num_stages - 1)
            if not is_last:
                h = down_sample(h)
                skips.append(h)

        # Mid
        h = self.mid_res1(h, t_emb)
        h = self.mid_attn(h)
        h = self.mid_res2(h, t_emb)

        # Up path
        for i, (blocks, up_sample) in enumerate(self.up_stages):
            stage_idx = self.num_stages - 1 - i              # 对应 down 阶段的 stage 下标
            is_top = (stage_idx == 0)
            for res_block, attn in blocks:
                h = torch.cat([h, skips.pop()], dim=1)
                h = res_block(h, t_emb)
                h = attn(h)
            if not is_top:
                h = up_sample(h)

        assert len(skips) == 0, f"Unconsumed skips at forward end: {len(skips)}"

        # Head
        h = F.silu(self.out_norm(h))
        return self.out_conv(h)
