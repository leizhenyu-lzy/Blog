import torch
import torch.nn as nn


class Encoder(nn.Module):
    """
    VAE Encoder: image -> latent space (mu, log_var)

    使用 4-2-1 卷积 (kernel=4, stride=2, padding=1) 逐层下采样:
        (B, 3, 64, 64)
        -> (B, 32, 32, 32) -> (B, 64, 16, 16)
        -> (B, 128, 8, 8) -> (B, 256, 4, 4)
        -> Flatten -> (B, 4096)
        -> Linear -> mu (B, latent_dim), log_var (B, latent_dim)

    4-2-1 卷积 (from DCGAN):
        output_size = (input_size - 4 + 2*1) / 2 + 1 = input_size / 2
        精确减半，无信息丢失，且转置卷积时不会产生棋盘效应
    """

    def __init__(
        self,
        image_size: int = 64,
        latent_dim: int = 128,
        in_channels: int = 3,
        hidden_channels: list[int] = None,
    ):
        super().__init__()

        if hidden_channels is None:
            hidden_channels = [32, 64, 128, 256]

        assert all(
            hidden_channels[i] <= hidden_channels[i + 1]
            for i in range(len(hidden_channels) - 1)
        ), f"Encoder hidden_channels should be non-decreasing: {hidden_channels}"

        channels = [in_channels] + hidden_channels  # assemble in_channels & hidden_channels

        layers = []
        for i in range(len(hidden_channels)):
            layers.append(
                nn.Conv2d(channels[i], channels[i + 1], kernel_size=4, stride=2, padding=1)
            )
            if i > 0:  # 第一层不加 BN (DCGAN 惯例: 输入已 normalize, BN 会破坏输入分布信息)
                layers.append(nn.BatchNorm2d(channels[i + 1]))
            layers.append(nn.ReLU(inplace=True))

        self.conv = nn.Sequential(*layers)

        # 每层 4-2-1 卷积将空间尺寸减半
        # 例: image_size=64, n_downsample=4 -> end_size=4, 即卷积后变成 4x4
        n_downsample = len(hidden_channels)
        end_size = image_size // (2 ** n_downsample)
        self.flatten_dim = channels[-1] * end_size * end_size

        self.fc_to_mu = nn.Linear(self.flatten_dim, latent_dim)
        self.fc_to_log_var = nn.Linear(self.flatten_dim, latent_dim)

    def forward(self, x: torch.Tensor):
        """
        Args:
            x: (B, 3, 64, 64), 值域 [-1, 1]
        Returns:
            mu:      (B, latent_dim)
            log_var: (B, latent_dim), 输出 log(sigma^2) 而非 sigma, log_var 可正可负, 数值更稳定
                     e^log_var = sigma^2
        """
        h = self.conv(x)             # (B, 256, 4, 4)
        h = h.view(h.size(0), -1)    # (B, 4096)
        mu = self.fc_to_mu(h)           # (B, latent_dim)
        log_var = self.fc_to_log_var(h)  # (B, latent_dim)
        return mu, log_var
