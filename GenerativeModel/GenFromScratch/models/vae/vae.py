import torch
import torch.nn as nn
import torch.nn.functional as F

from models.vae.vae_encoder import Encoder
from models.vae.vae_decoder import Decoder


class VAE(nn.Module):
    """
    VAE 整体: Encoder + Reparameterization Trick + Decoder

    训练时从 encoder 输出的分布中采样 (引入随机性, 平滑隐空间);
    推理/重建时可直接用 mu 作为 z (概率密度最大的点)。
    """

    def __init__(
        self,
        image_size: int = 64,
        latent_dim: int = 128,
        encoder_hidden_channels: list[int] = None,
        decoder_hidden_channels: list[int] = None,
    ):
        super().__init__()
        self.latent_dim = latent_dim
        self.encoder = Encoder(
            image_size=image_size,
            latent_dim=latent_dim,
            hidden_channels=encoder_hidden_channels,
        )
        self.decoder = Decoder(
            image_size=image_size,
            latent_dim=latent_dim,
            hidden_channels=decoder_hidden_channels,
        )

    @staticmethod
    def reparameterize(mu: torch.Tensor, log_var: torch.Tensor) -> torch.Tensor:
        """
        重参数化技巧: z = mu + sigma * epsilon
        将随机性转移到辅助噪声 epsilon 上, 使采样操作可导。

        epsilon ~ N(0, I), requires_grad=False
        sigma = exp(0.5 * log_var)
        """
        std = torch.exp(0.5 * log_var)  # sigma
        eps = torch.randn_like(std)  # epsilon ~ N(0, I)  # 每次调用 重新 随机 从 N(0,1) 采样，随机性只来自 epsilon
        return mu + std * eps

    def forward(self, x: torch.Tensor):
        """
        Args:
            x: (B, 3, H, W), 值域 [-1, 1]
        Returns:
            x_hat:   (B, 3, H, W), 重建图像
            mu:      (B, latent_dim)
            log_var: (B, latent_dim)
        """
        mu, log_var = self.encoder(x)
        z = self.reparameterize(mu, log_var)
        x_hat = self.decoder(z)
        return x_hat, mu, log_var

    @staticmethod
    def loss_function(
        x: torch.Tensor,
        x_hat: torch.Tensor,
        mu: torch.Tensor,
        log_var: torch.Tensor,
        kl_weight: float = 1.0,
    ) -> dict:
        """
        VAE Loss = Rec Loss + kl_weight * KL Loss

        Rec Loss: MSE(x, x_hat), 衡量重建质量
        KL  Loss: -0.5 * sum(1 + log_var - mu^2 - exp(log_var))
                  衡量 q(z|x) 与 先验 p(z) = N(0,I) 的距离

        两者博弈:
            - Rec Loss 希望不同样本映射到距离远的地方, 方差越小越好
            - KL Loss  强迫所有 q(z|x) 靠近 N(0,I), 保证隐空间连续可采样

        kl_weight (beta-VAE 的 beta):
            = 1.0  标准 VAE, 两项权重相等
            < 1.0  弱化正则, 重建更清晰, 但隐空间可能不连续, 生成多样性差
            > 1.0  强化正则, 隐空间更平滑/解耦, 但重建更模糊
                   beta-VAE 论文用 beta=4~10 来学习解耦的隐表示
            过大   导致后验坍塌 (posterior collapse): q(z|x) ≈ p(z), encoder 失效
        """
        rec_loss = F.mse_loss(x_hat, x, reduction='mean')  # per-pixel 平均

        # KL 闭式解 (两个高斯分布, 其中一个是标准正态)
        # per-dimension 平均: 对 latent_dim 求 mean, 对 batch 也求 mean
        # 这样 rec_loss 和 kl_loss 都是 per-element 级别的, kl_weight 的语义更清晰
        kl_loss = -0.5 * torch.mean(1 + log_var - mu.pow(2) - log_var.exp())
        # 原来的 sum 会导致，KL 项对参数的更新力度远大于 Rec 项，模型被过度推向 N(0,I)，重建质量被牺牲

        loss = rec_loss + kl_weight * kl_loss

        return {
            'loss': loss,
            'rec_loss': rec_loss,
            'kl_loss': kl_loss,
        }
