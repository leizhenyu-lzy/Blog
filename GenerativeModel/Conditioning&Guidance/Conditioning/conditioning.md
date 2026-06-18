# Conditioning Mechanism


---

# AdaIN (Adaptive Instance Norm) - 2017

风格迁移，γ/β 思想起源

# FiLM (Feature-Wise Linear Modulation) - 2018

VQA Task


# AdaGN (Adaptive Group Norm) - 2021

在 U-Net diffusion 里提出 AdaGN，用于时间步条件

# AdaLN (Adaptive Layer Norm) - 2022

DiT 把 AdaGN 的思想移植到 Transformer，命名为 AdaLN，并提出 AdaLN-Zero

系统比较 conditioning 策略
1. in-context
2. cross-attention
3. AdaLN
4. AdaLN-Zero : 把生成 γ/β 的最后一层线性层初始化为 0，使得训练初期每个 block 是恒等映射，训练更稳定
