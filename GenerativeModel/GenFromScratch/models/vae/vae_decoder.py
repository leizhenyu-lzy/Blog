import torch
import torch.nn as nn


class Decoder(nn.Module):
    """
    VAE Decoder: latent vector -> 重建图像

    Encoder 的镜像结构，使用 4-2-1 转置卷积逐层上采样:
        (B, latent_dim)
        -> Linear -> (B, 256 * 4 * 4) -> Reshape -> (B, 256, 4, 4)
        -> (B, 128, 8, 8) -> (B, 64, 16, 16) -> (B, 32, 32, 32)
        -> (B, 3, 64, 64)

    ConvTranspose2d(4,2,1):
        output_size = (input_size - 1) * 2 - 2*1 + 4 = input_size * 2
        精确翻倍，与 Encoder 的 Conv2d(4,2,1) 对称
    """

    def __init__(
        self,
        image_size: int = 64,
        latent_dim: int = 128,
        out_channels: int = 3,
        hidden_channels: list[int] = None,
    ):
        super().__init__()

        # Encoder hidden_channels 递增: [32, 64, 128, 256]
        # Decoder hidden_channels 递减: [256, 128, 64, 32]
        # 调用方直接传入递减序列，不做隐式反转
        if hidden_channels is None:
            hidden_channels = [256, 128, 64, 32]

        assert all(
            hidden_channels[i] >= hidden_channels[i + 1]
            for i in range(len(hidden_channels) - 1)
        ), f"Decoder hidden_channels should be non-increasing: {hidden_channels}"

        n_upsample = len(hidden_channels)
        # Decoder 起始特征图的空间尺寸，上采样 n 次后还原到 image_size
        # 例: image_size=64, n_upsample=4 -> start_size=4, 即从 4x4 开始上采样
        self.start_size = image_size // (2 ** n_upsample)
        self.start_channels = hidden_channels[0]
        self.fc_from_latent = nn.Linear(latent_dim, self.start_channels * self.start_size * self.start_size)

        layers = []
        for i in range(len(hidden_channels) - 1):  # Attention : last
            layers.append(
                nn.ConvTranspose2d(
                    hidden_channels[i], hidden_channels[i + 1],
                    kernel_size=4, stride=2, padding=1,
                )
            )
            layers.append(nn.BatchNorm2d(hidden_channels[i + 1]))
            layers.append(nn.ReLU(inplace=True))

        # 最后一层: 还原到图片通道数, Tanh 输出 [-1, 1]
        # 不加 BN (输出层不做归一化，保留原始值域)
        layers.append(
            nn.ConvTranspose2d(
                hidden_channels[-1], out_channels,
                kernel_size=4, stride=2, padding=1,
            )
        )
        layers.append(nn.Tanh())

        self.deconv = nn.Sequential(*layers)

    def forward(self, z: torch.Tensor):
        """
        Args:
            z: (B, latent_dim)
        Returns:
            x_hat: (B, 3, image_size, image_size), 值域 [-1, 1]
        """
        h = self.fc_from_latent(z)  # (B, 256 * 4 * 4)
        h = h.view(h.size(0), self.start_channels, self.start_size, self.start_size)
        x_hat = self.deconv(h)
        return x_hat
