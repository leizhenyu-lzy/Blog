"""
VAE 训练脚本

用法:
    python3 scripts/train_vae.py --config configs/vae_cfg.yaml
"""

import argparse
import sys
import os

import yaml
import torch
from torch.optim import Adam
from tqdm import tqdm

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from datasets.celeba import get_dataloader
from models.vae.vae import VAE
from utils.visualization import save_image_grid
from utils.tensorboard_logger import TensorboardLogger


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str,
                        default=os.path.join(PROJECT_ROOT, "configs", "vae_cfg.yaml"))
    args = parser.parse_args()
    cfg = load_config(args.config)

    output_dir = cfg["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

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
    vae = VAE(
        image_size=cfg["image_size"],
        latent_dim=cfg["latent_dim"],
        encoder_hidden_channels=cfg.get("encoder_hidden_channels"),
        decoder_hidden_channels=cfg.get("decoder_hidden_channels"),
    ).to(device)
    print(f"VAE params: {sum(p.numel() for p in vae.parameters()):,}")

    optimizer = Adam(vae.parameters(), lr=cfg["lr"])

    # --- 固定采样: 跟踪训练过程 ---
    fixed_latent = torch.randn(cfg["n_fixed_latent"], cfg["latent_dim"], device=device)
    fixed_recon_x = next(iter(dataloader))[:cfg["n_fixed_samples"]].to(device)

    # --- 训练循环 ---
    global_step = 0
    for epoch in range(1, cfg["epochs"] + 1):
        vae.train()
        epoch_loss = 0.0
        epoch_rec_loss = 0.0
        epoch_kl_divergence = 0.0

        pbar = tqdm(dataloader, desc=f"Epoch {epoch}/{cfg['epochs']}")
        for x in pbar:
            x = x.to(device)

            x_hat, mu, log_var = vae(x)
            losses = VAE.loss_function(x, x_hat, mu, log_var, kl_weight=cfg["kl_weight"])

            optimizer.zero_grad()
            losses["loss"].backward()
            optimizer.step()

            epoch_loss += losses["loss"].item()
            epoch_rec_loss += losses["rec_loss"].item()
            epoch_kl_divergence += losses["kl_loss"].item()
            global_step += 1

            pbar.set_postfix({
                "loss": f"{losses['loss'].item():.4f}",
                "rec": f"{losses['rec_loss'].item():.4f}",
                "kl": f"{losses['kl_loss'].item():.4f}",
            })

            if global_step % cfg["log_every"] == 0:
                logger.log_scalar("loss/total", losses["loss"].item(), global_step)
                logger.log_scalar("loss/reconstruction", losses["rec_loss"].item(), global_step)
                logger.log_scalar("loss/kl_divergence", losses["kl_loss"].item(), global_step)

        # epoch 平均
        n_batches = len(dataloader)
        avg_loss = epoch_loss / n_batches
        avg_rec_loss = epoch_rec_loss / n_batches
        avg_kl_divergence = epoch_kl_divergence / n_batches
        print(f"Epoch {epoch} | Loss: {avg_loss:.4f} | Rec: {avg_rec_loss:.4f} | KL: {avg_kl_divergence:.4f}")

        logger.log_scalar("epoch/loss", avg_loss, epoch)
        logger.log_scalar("epoch/reconstruction", avg_rec_loss, epoch)
        logger.log_scalar("epoch/kl_divergence", avg_kl_divergence, epoch)

        # --- 定期保存 ---
        if epoch % cfg["save_every"] == 0 or epoch == 1:
            vae.eval()
            with torch.no_grad():
                # 固定 z -> 生成
                generated = vae.decoder(fixed_latent)
                logger.log_image("generation/fixed_latent", generated, step=epoch)
                save_image_grid(generated,
                                os.path.join(output_dir, f"generated_epoch{epoch:03d}.png"))

                # 固定真实图片 -> 重建对比 (上排原图, 下排重建)
                recon_x_hat, _, _ = vae(fixed_recon_x)
                comparison = torch.cat([fixed_recon_x, recon_x_hat], dim=0)
                logger.log_image("reconstruction/comparison", comparison,
                                 step=epoch, nrow=cfg["n_fixed_samples"])
                save_image_grid(comparison,
                                os.path.join(output_dir, f"recon_epoch{epoch:03d}.png"),
                                nrow=cfg["n_fixed_samples"])

            torch.save({
                "epoch": epoch,
                "global_step": global_step,
                "model_state_dict": vae.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "config": cfg,
            }, os.path.join(output_dir, f"checkpoint_epoch{epoch:03d}.pt"))
            print(f"  -> Saved checkpoint & images (epoch {epoch})")

    logger.close()
    print(f"Training complete. Logs: {output_dir}/tb_logs/")


if __name__ == "__main__":
    train()
