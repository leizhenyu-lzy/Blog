"""
DiT backbone 自检脚本.

用法:
    python3 scripts/verify_dit.py
    python3 scripts/verify_dit.py --config configs/ddpm_dit_cfg.yaml

做四件事:
    1) 构造 DiT, 打印参数量
    2) 造一个随机 batch, 前向跑一次, 确认输出形状 = 输入形状
    3) 造一个 GaussianDiffusion, 调 compute_loss 端到端反向一次,
       确认所有参数都有梯度流 (排查"有模块没接入计算图"的低级错误)
    4) 抽查 AdaLN-Zero 初始化是否正确:
       - 初始 adaLN_mlp 输出 = 0
       - 初始 DiTBlock(tokens, t_emb) == tokens (identity)
       - 初始 FinalLayer 输出全 0
"""

import argparse
import os
import sys

import torch
import yaml

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from models.ddpm import DiT, GaussianDiffusion
from models.ddpm.dit import DiTBlock, FinalLayer


def build_dit(cfg: dict) -> DiT:
    d = cfg["dit"]
    return DiT(
        image_size=cfg["image_size"],
        in_channels=cfg["image_channels"],
        out_channels=cfg["image_channels"],
        patch_size=d["patch_size"],
        hidden_size=d["hidden_size"],
        depth=d["depth"],
        num_heads=d["num_heads"],
        mlp_ratio=d["mlp_ratio"],
    )


def build_diffusion(cfg: dict) -> GaussianDiffusion:
    d = cfg["diffusion"]
    return GaussianDiffusion(T=d["T"], beta_start=d["beta_start"], beta_end=d["beta_end"])


def test_forward_shape(dit: DiT, cfg: dict, device: torch.device):
    print("\n[1/4] Forward shape check")
    B = 2
    C = cfg["image_channels"]
    S = cfg["image_size"]
    x = torch.randn(B, C, S, S, device=device)
    t = torch.randint(0, cfg["diffusion"]["T"], (B,), device=device)

    with torch.no_grad():
        y = dit(x, t)

    assert y.shape == x.shape, f"output shape {y.shape} != input {x.shape}"
    print(f"    input  = {tuple(x.shape)}")
    print(f"    output = {tuple(y.shape)}  ✓")


def test_param_count(dit: DiT):
    print("\n[2/4] Parameter count")
    total = sum(p.numel() for p in dit.parameters())
    trainable = sum(p.numel() for p in dit.parameters() if p.requires_grad)
    print(f"    total     : {total:>12,}  ({total / 1e6:.2f} M)")
    print(f"    trainable : {trainable:>12,}  ({trainable / 1e6:.2f} M)")

    # 按 top-level 模块展开
    print("    breakdown:")
    for name, m in dit.named_children():
        n = sum(p.numel() for p in m.parameters())
        print(f"       {name:<15}{n:>12,}")


def test_backward(dit: DiT, diffusion: GaussianDiffusion, cfg: dict, device: torch.device):
    print("\n[3/4] End-to-end backward (compute_loss + backward)")
    dit.train()
    B = 2
    C = cfg["image_channels"]
    S = cfg["image_size"]
    x0 = torch.randn(B, C, S, S, device=device)

    loss = diffusion.compute_loss(dit, x0)
    loss.backward()
    print(f"    loss = {loss.item():.6f}")

    # 检查是否所有 require_grad 的参数都有梯度
    no_grad = [n for n, p in dit.named_parameters() if p.requires_grad and p.grad is None]
    if no_grad:
        print(f"    WARNING: {len(no_grad)} params without grad:")
        for n in no_grad[:5]:
            print(f"       - {n}")
    else:
        n_with_grad = sum(1 for p in dit.parameters() if p.grad is not None)
        print(f"    all {n_with_grad} parameters receive gradient  ✓")


def test_zero_init(dit: DiT, device: torch.device):
    """AdaLN-Zero 的核心: 初始 DiTBlock/FinalLayer 应该对输入做 identity / 输出全 0."""
    print("\n[4/4] AdaLN-Zero initialization")
    dit.eval()

    D = dit.blocks[0].attn.num_heads * dit.blocks[0].attn.head_dim
    B, N = 2, dit.num_patches
    tokens = torch.randn(B, N, D, device=device)
    t_emb = torch.randn(B, D, device=device)

    # 单个 block 的 AdaLN 输出应该全 0 (因为 adaLN_mlp 的输出层 zero-init)
    with torch.no_grad():
        block: DiTBlock = dit.blocks[0]
        adaLN_out = block.adaLN_mlp(t_emb)
        assert torch.allclose(adaLN_out, torch.zeros_like(adaLN_out)), (
            "adaLN_mlp should output all-zero at init"
        )
        print(f"    block.adaLN_mlp(t_emb) max |·| = {adaLN_out.abs().max().item():.2e}  ✓")

        # 整个 block 应该是 identity
        out = block(tokens, t_emb)
        diff = (out - tokens).abs().max().item()
        assert diff < 1e-5, f"block is not identity at init, diff = {diff}"
        print(f"    block(tokens, t_emb) - tokens  max |·| = {diff:.2e}  ✓")

        # FinalLayer 应该输出全 0
        final: FinalLayer = dit.final
        out = final(tokens, t_emb)
        diff = out.abs().max().item()
        assert diff < 1e-5, f"FinalLayer is not zero at init, max |·| = {diff}"
        print(f"    final(tokens, t_emb)           max |·| = {diff:.2e}  ✓")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default=os.path.join(PROJECT_ROOT, "configs", "ddpm_dit_cfg.yaml"),
    )
    args = parser.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    print(f"Config: {args.config}")

    dit = build_dit(cfg).to(device)
    diffusion = build_diffusion(cfg).to(device)

    test_forward_shape(dit, cfg, device)
    test_param_count(dit)
    test_backward(dit, diffusion, cfg, device)
    test_zero_init(dit, device)

    print("\nAll checks passed.\n")


if __name__ == "__main__":
    main()
