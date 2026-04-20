"""
DDPM + UNet 训练脚本

未来 DiT 骨干会对应独立的 train_ddpm_dit.py, 通过"不同脚本"区分 backbone,
而不是在一个脚本里用 --backbone flag 切换.

用法:
    python3 scripts/train_ddpm_unet.py --config configs/ddpm_cfg.yaml

产出 (在 logs/ddpm_<时间戳>/ 目录下):
    - tb_logs/            TensorBoard scalar + image
    - ddpm_cfg.yaml       本次训练的配置快照
    - samples_epoch###.png  每 save_every 个 epoch 的采样 (EMA 权重)
    - checkpoint_epoch###.pt  包含 model / ema / optimizer / epoch / config

训练目标 (DDPM):
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
from torch.optim import Adam
from torch.nn.utils import clip_grad_norm_
from tqdm import tqdm

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from datasets.celeba import get_dataloader
from models.ddpm import GaussianDiffusion, UNet
from utils.ema import EMA
from utils.tensorboard_logger import TensorboardLogger
from utils.visualization import save_image_grid


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def build_unet(cfg: dict) -> UNet:
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


def build_diffusion(cfg: dict) -> GaussianDiffusion:
    d = cfg["diffusion"]
    return GaussianDiffusion(T=d["T"], beta_start=d["beta_start"], beta_end=d["beta_end"])


@torch.no_grad()
def sample_with_ema(
    ema: EMA,
    base_model: UNet,
    diffusion: GaussianDiffusion,
    n: int,
    image_size: int,
    device: torch.device,
) -> torch.Tensor:
    """
    用 EMA 权重独立采样 n 张图. 不会影响 base_model 的原始权重,
    方便训练继续.
    """
    sampling_model = ema.clone_model(base_model).to(device)
    shape = (n, 3, image_size, image_size)
    samples = diffusion.p_sample_loop(sampling_model, shape)
    return samples.clamp(-1.0, 1.0)


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default=os.path.join(PROJECT_ROOT, "configs", "ddpm_cfg.yaml"),
    )
    parser.add_argument(
        "--resume",
        type=str,
        default=None,
        help="可选: 从 checkpoint 路径继续训练",
    )
    args = parser.parse_args()

    cfg = load_config(args.config)

    # --- 输出目录 ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{cfg['output_dir_prefix']}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy2(args.config, os.path.join(output_dir, os.path.basename(args.config)))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
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
    unet = build_unet(cfg).to(device)
    diffusion = build_diffusion(cfg).to(device)
    ema = EMA(unet, decay=cfg["ema_decay"])
    optimizer = Adam(unet.parameters(), lr=cfg["lr"])

    n_params = sum(p.numel() for p in unet.parameters())
    print(f"UNet params: {n_params:,}  ({n_params / 1e6:.2f} M)")

    # --- 恢复训练 (可选) ---
    start_epoch = 1
    global_step = 0
    if args.resume is not None:
        ckpt = torch.load(args.resume, map_location=device)
        unet.load_state_dict(ckpt["model_state_dict"])
        ema.load_state_dict(ckpt["ema_state_dict"])
        optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        start_epoch = ckpt["epoch"] + 1
        global_step = ckpt.get("global_step", 0)
        print(f"Resumed from {args.resume}: epoch {start_epoch - 1}, step {global_step}")

    # --- 训练循环 ---
    for epoch in range(start_epoch, cfg["epochs"] + 1):
        unet.train()
        epoch_loss = 0.0

        pbar = tqdm(dataloader, desc=f"Epoch {epoch}/{cfg['epochs']}")
        for x0 in pbar:
            x0 = x0.to(device, non_blocking=True)

            loss = diffusion.compute_loss(unet, x0)

            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            grad_norm = clip_grad_norm_(unet.parameters(), cfg["grad_clip"])
            optimizer.step()
            ema.update(unet)

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
        if epoch % cfg["save_every"] == 0 or epoch == 1:
            print(f"  -> Sampling {cfg['n_sample']} images with EMA weights...")
            samples = sample_with_ema(
                ema=ema,
                base_model=unet,
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
            torch.save({
                "epoch": epoch,
                "global_step": global_step,
                "model_state_dict": unet.state_dict(),
                "ema_state_dict": ema.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "config": cfg,
            }, ckpt_path)
            print(f"     Saved {ckpt_path}")

    logger.close()
    print(f"\nTraining complete. Logs: {output_dir}/tb_logs/")


if __name__ == "__main__":
    train()
