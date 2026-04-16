"""
统一的 TensorBoard 日志模块，供 VAE / DDPM / Flow Matching 训练脚本复用。
只提供最基本的 log_scalar / log_image / close，组合逻辑由调用方自行处理。

用法:
    logger = TensorboardLogger("outputs/vae")
    logger.log_scalar("loss/total", 0.5, step=100)
    logger.log_image("generation", images_tensor, step=1, nrow=8)
    logger.close()
"""

import torch
import torchvision
from torch.utils.tensorboard import SummaryWriter
from pathlib import Path

from datasets.celeba import denormalize


class TensorboardLogger:

    def __init__(self, output_dir: str, sub_dir: str = "tb_logs"):
        self.log_dir = str(Path(output_dir) / sub_dir)
        self.writer = SummaryWriter(log_dir=self.log_dir)

    def log_scalar(self, tag: str, value: float, step: int):
        self.writer.add_scalar(tag, value, step)

    def log_image(self, tag: str, images: torch.Tensor, step: int, nrow: int = 8):
        """
        将一批图片 (B, C, H, W) 以网格形式写入 TensorBoard。
        输入值域 [-1, 1]，内部自动 denormalize 到 [0, 1]。
        """
        grid = torchvision.utils.make_grid(
            denormalize(images.clamp(-1, 1)), nrow=nrow
        )
        self.writer.add_image(tag, grid, global_step=step)

    def close(self):
        self.writer.close()
