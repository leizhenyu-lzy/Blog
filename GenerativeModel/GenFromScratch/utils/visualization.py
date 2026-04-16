import torch
import torchvision
from pathlib import Path

from datasets.celeba import denormalize


def save_image_grid(
    images: torch.Tensor,
    path: str,
    nrow: int = 8,
):
    """
    将一批图片保存为网格图。

    Args:
        images: (B, C, H, W) tensor，值域 [-1, 1]
        path: 保存路径
        nrow: 每行显示几张图
    """
    images = denormalize(images.clamp(-1, 1))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    torchvision.utils.save_image(images, path, nrow=nrow)
