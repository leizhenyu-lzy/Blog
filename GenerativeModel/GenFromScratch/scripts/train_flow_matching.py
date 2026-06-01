"""
Rectified Flow / Flow Matching 统一训练脚本 (UNet / DiT 可切换)

backbone 由 config 里的 `backbone` 字段决定 (`unet` 或 `dit`).
Flow Matching 过程 / EMA / 采样 / 日志 / checkpoint 与 backbone 解耦。

用法:
    python3 scripts/train_flow_matching.py --config configs/fm_unet_cfg.yaml
    python3 scripts/train_flow_matching.py --config configs/fm_dit_cfg.yaml

训练目标:
    x_t = (1 - t) noise + t x_data,  t ~ Uniform(0,1), noise ~ N(0,I)
    loss = || v_theta(x_t, t) - (x_data - noise) ||^2
"""

import argparse
import os
import shutil
import sys
from datetime import datetime

import torch
import torch.nn as nn
import yaml
from torch.nn.utils import clip_grad_norm_
from torch.optim import Adam
from tqdm import tqdm

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from datasets.celeba import get_dataloader
from models.ddpm import DiT, UNet
from models.flow_matching import RectifiedFlow
from utils.ema import EMA
from utils.tensorboard_logger import TensorboardLogger
from utils.visualization import save_image_grid


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def build_backbone(cfg: dict) -> nn.Module:
    """
    根据 cfg["backbone"] 装配 UNet 或 DiT. 对外接口都是 model(x_t, t) -> velocity.
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


def build_flow(cfg: dict) -> RectifiedFlow:
    flow_cfg = cfg["flow"]
    return RectifiedFlow(time_scale=flow_cfg["time_scale"])


@torch.no_grad()
def sample_with_ema(
    ema: EMA,
    base_model: nn.Module,
    flow: RectifiedFlow,
    n: int,
    image_channels: int,
    image_size: int,
    sample_steps: int,
    device: torch.device,
) -> torch.Tensor:
    """用 EMA 权重独立采样 n 张图."""
    sampling_model = ema.clone_model(base_model).to(device)
    shape = (n, image_channels, image_size, image_size)
    samples = flow.sample_loop(sampling_model, shape, num_steps=sample_steps)
    return samples.clamp(-1.0, 1.0)


def save_checkpoint(
    path: str,
    epoch: int,
    model: nn.Module,
    ema: EMA,
    cfg: dict,
) -> None:
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
        help="config path, eg: configs/fm_unet_cfg.yaml 或 configs/fm_dit_cfg.yaml",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)
    backbone = cfg["backbone"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{cfg['output_dir_prefix']}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy2(args.config, os.path.join(output_dir, os.path.basename(args.config)))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device:     {device}")
    print(f"Backbone:   {backbone}")
    print(f"Output dir: {output_dir}")

    logger = TensorboardLogger(output_dir)

    dataloader = get_dataloader(
        data_root=cfg["data_root"],
        image_size=cfg["image_size"],
        batch_size=cfg["batch_size"],
        num_workers=cfg["num_workers"],
    )
    print(f"Dataset: {len(dataloader.dataset):,} images, {len(dataloader)} batches/epoch")

    model = build_backbone(cfg).to(device)
    flow = build_flow(cfg).to(device)
    ema = EMA(model, decay=cfg["ema_decay"])
    optimizer = Adam(model.parameters(), lr=cfg["lr"])

    n_params = sum(p.numel() for p in model.parameters())
    print(f"{backbone.upper()} params: {n_params:,}  ({n_params / 1e6:.2f} M)")
    print(f"Sample steps: {cfg['sample_steps']}")

    total_epochs = cfg["epochs"]
    global_step = 0
    for epoch in range(total_epochs):
        model.train()
        epoch_loss = 0.0

        pbar = tqdm(dataloader, desc=f"Epoch {epoch}/{total_epochs}")
        for x_data in pbar:
            x_data = x_data.to(device, non_blocking=True)

            loss = flow.compute_loss(model, x_data)

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

        is_last = (epoch == total_epochs - 1)
        if epoch % cfg["save_every"] == 0 or is_last:
            print(
                f"  -> Sampling {cfg['n_sample']} images with EMA weights "
                f"({cfg['sample_steps']} Euler steps)..."
            )
            samples = sample_with_ema(
                ema=ema,
                base_model=model,
                flow=flow,
                n=cfg["n_sample"],
                image_channels=cfg["image_channels"],
                image_size=cfg["image_size"],
                sample_steps=cfg["sample_steps"],
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
