"""
DDPM 扩散过程 — 与 backbone 完全解耦

核心思想:
    前向过程 (q): 逐步给图片加高斯噪声, 直到变成纯噪声
    反向过程 (p): 训练一个网络预测噪声, 逐步去噪还原图片

与 backbone 的接口约定:
    model(x_t, t) -> noise_pred
    - x_t: (B, C, H, W) 加噪后的图片
    - t:   (B,) 时间步 (整数, 0 ~ T-1)
    - 返回: (B, C, H, W) 预测的噪声

参考: Ho et al. 2020 "Denoising Diffusion Probabilistic Models"
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class GaussianDiffusion(nn.Module):
    """
    高斯扩散过程

    前向过程 q(x_t | x_0):
        x_t = sqrt(ᾱ_t) * x_0 + sqrt(1 - ᾱ_t) * ε,  ε ~ N(0, I)

        ᾱ_t (alpha_bar) 是 α 的累积乘积, 控制信噪比:
            t=0   -> ᾱ≈1, x_t ≈ x_0          (几乎没有噪声)
            t=T-1 -> ᾱ≈0, x_t ≈ ε            (几乎纯噪声)

    反向过程 p(x_{t-1} | x_t):
        用网络预测噪声 ε_θ(x_t, t), 然后:
            μ_θ = (1/√α_t) * (x_t - (β_t / √(1-ᾱ_t)) * ε_θ)
            x_{t-1} = μ_θ + σ_t * z,  z ~ N(0, I)  (t>0 时加噪, t=0 时不加)

    训练目标:
        L = E_{t, x_0, ε} [ ||ε - ε_θ(x_t, t)||² ]
        随机采样 t 和噪声 ε, 让网络预测噪声, 用 MSE 优化
    """

    def __init__(
        self,
        T: int = 1000,
        beta_start: float = 1e-4,
        beta_end: float = 2e-2,
    ):
        super().__init__()
        self.T = T

        # --- 预计算所有常量，用 register_buffer 管理 ---
        # register_buffer: 不参与梯度计算, 但随 model.to(device) 自动迁移
        # 也会被 state_dict 保存/加载

        # β_t: 噪声方差, 从 beta_start 线性增长到 beta_end
        betas = torch.linspace(beta_start, beta_end, T)
        alphas = 1.0 - betas
        # ᾱ_t = α_1 * α_2 * ... * α_t (累积乘积)
        alpha_bars = torch.cumprod(alphas, dim=0)  # cumulate product

        self.register_buffer("betas", betas)
        self.register_buffer("alphas", alphas)
        self.register_buffer("alpha_bars", alpha_bars)

        # 前向加噪用的系数
        self.register_buffer("sqrt_alpha_bars", torch.sqrt(alpha_bars))
        self.register_buffer("sqrt_one_minus_alpha_bars", torch.sqrt(1.0 - alpha_bars))

        # 反向去噪用的系数 (对应采样公式中 μ_θ 的两个部分)
        # μ_θ = (1/√α_t) * (x_t - (β_t/√(1-ᾱ_t)) * ε_θ)
        self.register_buffer("sqrt_reciprocal_alphas", torch.sqrt(1.0 / alphas))
        self.register_buffer(
            "noise_coeff",
            betas / torch.sqrt(1.0 - alpha_bars),
        )

        # 后验方差 σ²_t = β_t * (1 - ᾱ_{t-1}) / (1 - ᾱ_t)
        # t=0 时没有 ᾱ_{t-1}, 设为 β_0 (不会被用到, 因为 t=0 不加噪)
        alpha_bars_prev = F.pad(alpha_bars[:-1], (1, 0), value=1.0)
        posterior_variance = betas * (1.0 - alpha_bars_prev) / (1.0 - alpha_bars)
        self.register_buffer("posterior_variance", posterior_variance)

    def q_sample(
        self,
        x0: torch.Tensor,
        t: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        """
        前向加噪: 一步到位从 x_0 得到 x_t (不需要逐步加噪)

        x_t = √(ᾱ_t) * x_0 + √(1 - ᾱ_t) * ε

        Args:
            x0: (B, C, H, W) 原始干净图片
            t:  (B,) 时间步

        Returns:
            x_t:   (B, C, H, W) 加噪后的图片
            noise: (B, C, H, W) 本次采样的噪声 ε (训练时作为 ground truth)
        """
        noise = torch.randn_like(x0)

        sqrt_alpha_bar = self.sqrt_alpha_bars[t][:, None, None, None]
        sqrt_one_minus_alpha_bar = self.sqrt_one_minus_alpha_bars[t][:, None, None, None]

        x_t = sqrt_alpha_bar * x0 + sqrt_one_minus_alpha_bar * noise
        return x_t, noise

    @torch.no_grad()
    def p_sample(
        self,
        model: nn.Module,
        x_t: torch.Tensor,
        t: torch.Tensor,
    ) -> torch.Tensor:
        """
        反向去噪一步: 从 x_t 得到 x_{t-1}

        μ_θ = (1/√α_t) * (x_t - (β_t/√(1-ᾱ_t)) * ε_θ(x_t, t))
        x_{t-1} = μ_θ + σ_t * z   (t > 0)
        x_{t-1} = μ_θ              (t = 0, 最后一步不加噪)
        """
        noise_pred = model(x_t, t)

        sqrt_reciprocal_alpha = self.sqrt_reciprocal_alphas[t][:, None, None, None]
        noise_c = self.noise_coeff[t][:, None, None, None]

        # μ_θ = (1/√α_t) * (x_t - (β_t/√(1-ᾱ_t)) * ε_θ)
        mean = sqrt_reciprocal_alpha * (x_t - noise_c * noise_pred)

        if (t == 0).all():
            return mean

        # t > 0 时添加噪声
        sigma = torch.sqrt(self.posterior_variance[t])[:, None, None, None]
        z = torch.randn_like(x_t)
        return mean + sigma * z

    @torch.no_grad()
    def p_sample_loop(
        self,
        model: nn.Module,
        shape: tuple,
    ) -> torch.Tensor:
        """
        完整生成过程: 从纯噪声 x_T 逐步去噪到 x_0

        x_T -> x_{T-1} -> ... -> x_1 -> x_0

        Args:
            model: backbone 网络, 接口 model(x_t, t) -> noise_pred
            shape: 生成图片的 shape, 如 (16, 3, 64, 64)

        Returns:
            x_0: (B, C, H, W) 生成的图片
        """
        device = self.betas.device
        b = shape[0]

        # 从纯噪声开始
        x_t = torch.randn(shape, device=device)

        for i in reversed(range(self.T)):
            t = torch.full((b,), i, device=device, dtype=torch.long)
            x_t = self.p_sample(model, x_t, t)

        return x_t

    def compute_loss(
        self,
        model: nn.Module,
        x0: torch.Tensor,
    ) -> torch.Tensor:
        """
        训练损失: L = E_{t, ε} [ ||ε - ε_θ(x_t, t)||² ]

        步骤:
            1. 随机采样时间步 t ~ Uniform(0, T-1)
            2. q_sample 加噪得到 x_t, 同时返回噪声 ε
            3. 用网络预测噪声 ε_θ = model(x_t, t)
            4. MSE(ε, ε_θ)
        """
        b = x0.shape[0]
        device = x0.device

        t = torch.randint(0, self.T, (b,), device=device, dtype=torch.long)
        x_t, noise = self.q_sample(x0, t)
        noise_pred = model(x_t, t)

        return F.mse_loss(noise_pred, noise)
