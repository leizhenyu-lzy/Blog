# GenFromScratch 实现计划

## 核心原则

**一步步迭代实现**：每个 Step 完成后停下来，一起验证理解和代码正确性，再继续下一步。

**统一数据集抽象**：`datasets/celeba.py` 提供一个通用的 `CelebADataset` 类，所有模型 (VAE / DDPM-UNet / DDPM-DiT / 未来的 Flow Matching) 共享同一份数据加载代码。

## 项目结构

```
GenFromScratch/
├── readme.md
├── requirements.txt
│
├── datasets/
│   ├── __init__.py
│   └── celeba.py              # 统一数据集类，所有模型共享
│
├── models/
│   ├── __init__.py
│   ├── vae/
│   │   ├── __init__.py
│   │   ├── encoder.py
│   │   ├── decoder.py
│   │   └── vae.py
│   ├── ddpm/
│   │   ├── __init__.py
│   │   ├── unet.py
│   │   ├── dit.py
│   │   └── diffusion.py       # 扩散过程逻辑，与 backbone 解耦
│   └── flow_matching/         # 预留
│       └── __init__.py
│
├── train_vae.py
├── train_ddpm.py              # DDPM 统一训练脚本 (backbone 由 config["backbone"] 决定)
├── sample_ddpm.py             # DDPM 统一采样脚本 (未来)
│
└── utils/
    ├── __init__.py
    ├── visualization.py
    └── ema.py
```

## 统一数据集设计

`datasets/celeba.py` 中的 `CelebADataset` 和工厂函数 `get_dataloader()`:

- 输入参数: `data_root`, `image_size` (默认 64), `batch_size`, `num_workers`
- 预处理 pipeline: `Resize(image_size)` -> `CenterCrop(image_size)` -> `ToTensor()` -> `Normalize([0.5]*3, [0.5]*3)` (映射到 [-1, 1])
- 返回标准 `DataLoader`，所有 train 脚本只需 `from datasets.celeba import get_dataloader`
- 也提供 `denormalize()` 工具函数 (从 [-1,1] 还原到 [0,1]，用于可视化)

## 迭代实现步骤

### Step 0: 项目骨架 + 统一数据集 `[x]`

创建目录结构、`requirements.txt`、`datasets/celeba.py`、`utils/visualization.py`。

验证点: 能 `get_dataloader()` 加载数据，取一个 batch，可视化几张图确认预处理正确。

### Step 1: VAE Encoder `[ ]`

`models/vae/encoder.py` — 4-2-1 卷积链 (3->32->64->128->256)，flatten + Linear 输出 `mu` 和 `log_var`。

验证点: 输入 `(B, 3, 64, 64)` -> 输出 `mu: (B, latent_dim)`, `log_var: (B, latent_dim)`，打印每层 shape 确认。

### Step 2: VAE Decoder `[ ]`

`models/vae/decoder.py` — Linear + reshape + ConvTranspose2d (4-2-1) 上采样，Tanh 输出。

验证点: 输入 `(B, latent_dim)` -> 输出 `(B, 3, 64, 64)`，与 Encoder 对称，确认维度匹配。

### Step 3: VAE 整体模型 + Loss `[ ]`

`models/vae/vae.py` — 组合 Encoder + Decoder，实现 reparameterization trick 和 loss 计算。

关键代码:

- `z = mu + exp(0.5 * log_var) * epsilon`
- `kl_loss = -0.5 * sum(1 + log_var - mu^2 - exp(log_var))`
- `rec_loss = MSE(x, x_hat)`

验证点: forward pass 不报错，loss 值合理 (初始阶段 rec_loss 较大，kl_loss 较小)。

### Step 4: VAE 训练 `[ ]`

`train_vae.py` — 训练循环 + checkpoint 保存 + 每 N epoch 生成图片。

验证点: loss 持续下降，生成的人脸虽模糊但可辨认。

### Step 5: Diffusion 核心逻辑 `[ ]`

`models/ddpm/diffusion.py` — 与 backbone 完全解耦的扩散过程。

关键实现:

- 线性 beta schedule: `beta_start=1e-4, beta_end=0.02, T=1000`
- 预计算所有常量: `alpha`, `alpha_bar`, `sqrt_alpha_bar` 等
- `q_sample(x0, t, noise)`: 前向一步到位加噪
- `p_sample(model, x_t, t)`: 单步去噪采样
- `p_sample_loop(model, shape)`: 完整生成 loop

验证点: 取一张真实图片，可视化不同 t 下的加噪效果 (t=0 清晰, t=500 半噪, t=999 纯噪声)。

### Step 6: UNet Backbone `[ ]`

`models/ddpm/unet.py` — Sinusoidal TimeEmbedding -> ResBlock (注入 time) -> SelfAttention -> DownBlock / MidBlock / UpBlock + Skip connections。

验证点: 输入 `(B, 3, 64, 64)` + `(B,)` timestep -> 输出 `(B, 3, 64, 64)` noise prediction，shape 正确。

### Step 7: DDPM 训练 + 采样 `[ ]`

`train_ddpm.py` (backbone=unet) + `sample_ddpm.py` + `utils/ema.py`

验证点: 训练 loss 下降，采样出的人脸逐渐清晰。

### Step 8: DiT Backbone `[ ]`

`models/ddpm/dit.py` — Patchify (4x4 -> 256 tokens) + Transformer blocks (AdaLN-Zero 注入 time) + Unpatchify。

验证点: 复用 `train_ddpm.py`, 切 `backbone: dit` + 独立的 `ddpm_dit_cfg.yaml`, 与 UNet 对比生成质量。

### Step 9: Flow Matching (预留) `[ ]`

预留 `models/flow_matching/`，待学完理论后实现。与 VAE/DDPM 共享 `datasets/` 和 `utils/`。

## 后续扩展 (低优先级, 按推荐顺序排列) `[ ]`

> 所有扩展共享已有的 `GaussianDiffusion` / `EMA` / `datasets` / `utils`。除非特别注明，训练不用从头重来。

### Ext 1: DDIM 采样加速 `[ ]`  难度 ⭐⭐

不改模型权重, 只加一个新的采样函数.

- `models/ddpm/diffusion.py` 加 `ddim_sample(model, shape, num_steps=50)` 方法
- 确定性 ODE solver, 支持任意跳步 (20/50/100 步)
- 直接复用已训练好的 UNet / DiT ckpt
- 新增 `scripts/sample_ddpm.py` 统一采样脚本 (支持 DDPM / DDIM 切换, 接收 `--ckpt` 路径)

验证点: DDIM 50 步的采样质量接近 DDPM 1000 步, 单次采样耗时从 ~80s 降到 ~4s.

### Ext 2: SDEdit (img2img) `[ ]`  难度 ⭐

不改模型权重、不改训练, 只在采样循环里换起点.

- `sample_ddpm.py` 加 `--mode sdedit --ref <image>` + `--t_start <int>` 选项
- 前向加噪 `q_sample(x_ref, t_start)` 作为去噪起点, 从 `t_start` 往 0 跑 `p_sample_loop`
- 可视化 `t_start ∈ {100, 300, 500, 800}` 的不同改动幅度

验证点: `t_start=500` 生成的人脸保留原图结构但换表情/风格.

### Ext 3: Inpainting `[ ]`  难度 ⭐

同样只改采样.

- 加 `--mode inpaint --ref <image> --mask <image>` 选项
- 每步 `p_sample` 后把已知区域重置成 `q_sample(x_ref, t-1)` 再进下一步
- 评估边界协调度, 若不好再上 RePaint 的 resampling trick

验证点: 给一张人脸遮住嘴巴, 能生成合理的嘴型, 其它部位保持不变.

### Ext 4: Class-Conditional 生成 `[ ]`  难度 ⭐⭐  *需要重训模型*

- `datasets/celeba.py` 扩展: 读 `list_attr_celeba.csv`, `__getitem__` 返回 `(x, y)`
  - 简化起见, 选 1-3 个高区分度属性 (eg. `Smiling`, `Male`, `Eyeglasses`), 组合成单一离散类别 (2-8 类)
- UNet / DiT 加 `nn.Embedding(num_classes + 1, emb_dim)`, forward 多吃 `y`
  - `y_emb` 与 `t_emb` 同路注入 (UNet 的 ResBlock time_mlp / DiT 的 AdaLN-Zero)
- 训练时 `y_emb` 直接用真实标签 (暂不做 CFG dropout, 下一步加)
- 新增 `configs/ddpm_unet_cond_cfg.yaml` / `ddpm_dit_cond_cfg.yaml`

验证点: 指定 `y = Smiling_yes` 生成微笑脸, `y = Smiling_no` 生成不笑, 肉眼可辨差异.

### Ext 5: Classifier-Free Guidance (CFG) `[ ]`  难度 ⭐⭐⭐  *依赖 Ext 4*

在 Ext 4 的基础上加两处:

- **训练**: `compute_loss` 以 `p_uncond = 0.1` 概率把 `y` 替换为 `NULL_ID` (= `num_classes`)
- **采样**: 新增 `cfg_sample_loop(model, shape, y, w)`, 每步两次 forward (或 batch 翻倍一次 forward):
    ε̃ = (1+w) · ε(x, y) - w · ε(x, null)

验证点: 对比 `w ∈ {0, 1, 3, 7.5}` 的生成效果, `w` 增大时条件匹配度提升, 多样性下降. 同一个 `(x_T, y)`  seed 下, `w` 滑块能给出 "从无条件到强条件" 的连续变化序列.

### Ext 6: DPM-Solver (进阶采样) `[ ]`  难度 ⭐⭐

DDIM 的 2-3 阶 ODE solver 版本, 10-20 步达到 DDIM 50 步质量.

- `models/ddpm/diffusion.py` 加 `dpm_solver_sample` (或者直接 copy diffusers 的实现)
- 前置依赖: Ext 1 (DDIM) 已有

验证点: 20 步采样质量不输 DDIM 50 步, 对部署场景更友好.

### Ext 7: Text-Conditional (Stable Diffusion 风) `[ ]`  难度 ⭐⭐⭐⭐⭐  *性价比低*

CelebA 本身没文本描述, 需要外部配对数据 (COCO / LAION 子集).
- 集成预训练文本 encoder (CLIP text / T5-small), 冻结权重
- UNet 加 cross-attention 层 (或 DiT 换成 MMDiT 把 text token 和 image token concat)
- 训练数据、模型规模、硬件需求都远超前面几项, 不作为本项目目标, 仅留作概念记录.

## 关键设计决策

- **图像尺寸**: 64x64，DiT patch_size=4 产生 256 个 token
- **统一数据接口**: 所有 train 脚本通过 `get_dataloader(data_root, image_size, batch_size)` 获取数据
- **backbone 解耦**: `diffusion.py` 不关心具体网络结构，只要求 `model(x_t, t) -> noise_pred`
- **EMA**: DDPM 阶段引入，VAE 不需要
