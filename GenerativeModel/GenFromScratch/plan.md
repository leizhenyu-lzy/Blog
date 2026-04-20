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
├── train_ddpm_unet.py         # DDPM + UNet backbone
├── train_ddpm_dit.py          # DDPM + DiT backbone (未来)
├── sample_ddpm_unet.py
├── sample_ddpm_dit.py         # (未来)
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

`train_ddpm_unet.py` + `sample_ddpm_unet.py` + `utils/ema.py`

验证点: 训练 loss 下降，采样出的人脸逐渐清晰。

### Step 8: DiT Backbone `[ ]`

`models/ddpm/dit.py` — Patchify (4x4 -> 256 tokens) + Transformer blocks (AdaLN-Zero 注入 time) + Unpatchify。

验证点: 新建独立的 `train_ddpm_dit.py` / `sample_ddpm_dit.py` (复用 `GaussianDiffusion` / `EMA` / data loader)，对比 UNet 的生成质量。

### Step 9: Flow Matching (预留) `[ ]`

预留 `models/flow_matching/`，待学完理论后实现。与 VAE/DDPM 共享 `datasets/` 和 `utils/`。

## 关键设计决策

- **图像尺寸**: 64x64，DiT patch_size=4 产生 256 个 token
- **统一数据接口**: 所有 train 脚本通过 `get_dataloader(data_root, image_size, batch_size)` 获取数据
- **backbone 解耦**: `diffusion.py` 不关心具体网络结构，只要求 `model(x_t, t) -> noise_pred`
- **EMA**: DDPM 阶段引入，VAE 不需要
