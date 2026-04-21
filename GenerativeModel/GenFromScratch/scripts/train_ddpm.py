"""
DDPM 统一训练脚本 (UNet / DiT 可切换)

backbone 由 config 里的 `backbone` 字段决定 (`unet` 或 `dit`).
其它部分 (扩散过程 / EMA / 采样 / 日志 / checkpoint) 与 backbone 完全无关,
因此不需要为每个 backbone 维护一份独立脚本.

用法:
    python3 scripts/train_ddpm.py --config configs/ddpm_unet_cfg.yaml
    python3 scripts/train_ddpm.py --config configs/ddpm_dit_cfg.yaml

产出 (在 <output_dir_prefix>_<时间戳>/ 目录下):
    - tb_logs/                 TensorBoard scalar + image
    - <原 config>.yaml         本次训练的配置快照
    - samples_epoch###.png     每 save_every 个 epoch 的采样 (EMA 权重)
    - checkpoint_epoch###.pt   包含 model / ema / epoch / config

训练目标 (DDPM, 与 backbone 无关):
    loss = E_{t, ε, x0} [ || ε - ε_θ(x_t, t) ||² ]
其中 x_t = √(ᾱ_t) x0 + √(1 - ᾱ_t) ε, ε ~ N(0,I), t ~ Uniform{0,...,T-1}.
"""

import argparse
import os
import shutil
import sys
from datetime import datetime

import yaml
import torch
import torch.nn as nn
from torch.optim import Adam
from torch.nn.utils import clip_grad_norm_
from tqdm import tqdm

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from datasets.celeba import get_dataloader
from models.ddpm import DiT, GaussianDiffusion, UNet
from utils.ema import EMA
from utils.tensorboard_logger import TensorboardLogger
from utils.visualization import save_image_grid


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def build_backbone(cfg: dict) -> nn.Module:
    """
    根据 cfg["backbone"] 装配 UNet 或 DiT. 对外接口都是 model(x_t, t) -> noise_pred,
    所以 GaussianDiffusion / EMA / 采样循环完全不需要感知具体结构.
    """
    name = cfg["backbone"]
    if name == "unet":
        unet_cfg = cfg["unet"]
        return UNet(
            image_size=cfg["image_size"],
            in_channels=cfg["image_channels"],
            out_channels=cfg["image_channels"],
            base_channels=unet_cfg["base_channels"],
            channel_mult=unet_cfg["channel_mult"],
            num_res_blocks=unet_cfg["num_res_blocks"],
            attn_resolutions=unet_cfg["attn_resolutions"],
            time_emb_dim=unet_cfg["time_emb_dim"],
            num_heads=unet_cfg["num_heads"],
            dropout=unet_cfg["dropout"],
        )
    if name == "dit":
        dit_cfg = cfg["dit"]
        return DiT(
            image_size=cfg["image_size"],
            in_channels=cfg["image_channels"],
            out_channels=cfg["image_channels"],
            patch_size=dit_cfg["patch_size"],
            hidden_size=dit_cfg["hidden_size"],
            depth=dit_cfg["depth"],
            num_heads=dit_cfg["num_heads"],
            mlp_ratio=dit_cfg["mlp_ratio"],
        )
    raise ValueError(f"Unknown backbone: {name!r} (expected 'unet' or 'dit')")


def build_diffusion(cfg: dict) -> GaussianDiffusion:
    diffusion_cfg = cfg["diffusion"]
    return GaussianDiffusion(
        T=diffusion_cfg["T"],
        beta_start=diffusion_cfg["beta_start"],
        beta_end=diffusion_cfg["beta_end"],
    )


@torch.no_grad()
def sample_with_ema(
    ema: EMA,
    base_model: nn.Module,
    diffusion: GaussianDiffusion,
    n: int,
    image_size: int,
    device: torch.device,
) -> torch.Tensor:
    """
    用 EMA 权重独立采样 n 张图. 不会影响 base_model 的原始权重, 方便训练继续
    """
    sampling_model = ema.clone_model(base_model).to(device)
    shape = (n, 3, image_size, image_size)
    samples = diffusion.p_sample_loop(sampling_model, shape)
    return samples.clamp(-1.0, 1.0)


def save_checkpoint(
    path: str,
    epoch: int,
    model: nn.Module,
    ema: EMA,
    cfg: dict,
) -> None:
    """把 model / ema 权重 + 元信息写入一个 .pt 文件."""
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "ema_state_dict": ema.state_dict(),
        "config": cfg,
    }, path)


def load_checkpoint(
    path: str,
    model: nn.Module,
    ema: EMA,
    device: torch.device,
) -> int:
    """
    从 .pt 文件把权重装回 `model` 和 `ema` (inplace).

    返回: 保存时的 epoch 索引 (0-based). 便于调用方打印或做后续判断.
    """
    ckpt = torch.load(path, map_location=device)
    model.load_state_dict(ckpt["model_state_dict"])
    ema.load_state_dict(ckpt["ema_state_dict"])
    return ckpt["epoch"]


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="config path, eg: configs/ddpm_unet_cfg.yaml 或 configs/ddpm_dit_cfg.yaml",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    backbone = cfg["backbone"]

    # --- 输出目录 ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{cfg['output_dir_prefix']}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy2(args.config, os.path.join(output_dir, os.path.basename(args.config)))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device:     {device}")
    print(f"Backbone:   {backbone}")
    print(f"Output dir: {output_dir}")

    logger = TensorboardLogger(output_dir)

    # --- 数据 ---
    dataloader = get_dataloader(
        data_root=cfg["data_root"],
        image_size=cfg["image_size"],
        batch_size=cfg["batch_size"],
        num_workers=cfg["num_workers"],
    )
    print(f"Dataset: {len(dataloader.dataset):,} images, {len(dataloader)} batches/epoch")

    # --- 模型 ---
    model = build_backbone(cfg).to(device)
    diffusion = build_diffusion(cfg).to(device)
    ema = EMA(model, decay=cfg["ema_decay"])
    optimizer = Adam(model.parameters(), lr=cfg["lr"])

    n_params = sum(p.numel() for p in model.parameters())
    print(f"{backbone.upper()} params: {n_params:,}  ({n_params / 1e6:.2f} M)")

    # --- 训练循环 ---
    # epoch 0-based; global_step = 已完成的 batch (optimizer.step) 次数, 也 0-based
    total_epochs = cfg["epochs"]
    global_step = 0
    for epoch in range(total_epochs):
        model.train()
        epoch_loss = 0.0

        pbar = tqdm(dataloader, desc=f"Epoch {epoch}/{total_epochs}")
        for x0 in pbar:
            x0 = x0.to(device, non_blocking=True)  # non_blocking=True: CPU→GPU 拷贝不阻塞 Python 主线程

            loss = diffusion.compute_loss(model, x0)

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            grad_norm = clip_grad_norm_(model.parameters(), cfg["grad_clip"])
            optimizer.step()
            ema.update(model)

            epoch_loss += loss.item()
            global_step += 1

            pbar.set_postfix({
                "loss": f"{loss.item():.4f}",
                "grad_norm": f"{grad_norm.item():.2f}",
            })

            if global_step % cfg["log_every"] == 0:
                logger.log_scalar("loss/step", loss.item(), global_step)
                logger.log_scalar("grad_norm", grad_norm.item(), global_step)

        avg_loss = epoch_loss / max(1, len(dataloader))
        print(f"Epoch {epoch} | avg loss: {avg_loss:.4f}")
        logger.log_scalar("loss/epoch", avg_loss, epoch)

        # --- 定期采样 + 保存 ---
        # 第 0/save_every/2*save_every/... 个 epoch 结束后存; 最后一个 epoch 强制存
        is_last = (epoch == total_epochs - 1)
        if epoch % cfg["save_every"] == 0 or is_last:
            print(f"  -> Sampling {cfg['n_sample']} images with EMA weights...")
            samples = sample_with_ema(
                ema=ema,
                base_model=model,
                diffusion=diffusion,
                n=cfg["n_sample"],
                image_size=cfg["image_size"],
                device=device,
            )
            sample_path = os.path.join(output_dir, f"samples_epoch{epoch:03d}.png")
            save_image_grid(samples, sample_path, nrow=8)
            logger.log_image("samples/ema", samples, step=epoch, nrow=8)
            print(f"     Saved {sample_path}")

            ckpt_path = os.path.join(output_dir, f"checkpoint_epoch{epoch:03d}.pt")
            save_checkpoint(ckpt_path, epoch, model, ema, cfg)
            print(f"     Saved {ckpt_path}")

    logger.close()
    print(f"\nTraining complete. Logs: {output_dir}/tb_logs/")


if __name__ == "__main__":
    train()
