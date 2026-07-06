# Fast Foundation Stereo

Links
1. [Website](https://nvlabs.github.io/Fast-FoundationStereo/)
2. [Github](https://github.com/NVlabs/Fast-FoundationStereo)

---

#

加速策略
1. **knowledge distillation**
   1. 将混合 backbone 压缩成一个高效的 student backbone
   2. **Depth Anything V2** & **Side-Tuning CNN**
   3. hybrid 的 monocular & stereo priors
2. **block-wise neural architecture search**
   1. 在给定延迟预算下，自动搜索最优的 cost filtering 设计
   2. 指数级降低 搜索复杂度
3. **structured pruning**
   1. 去除 iterative refinement 模块中的冗余

自动 pseudo-labeling pipeline


---

# Knowledge Distillation

left-right image pairs

multi-level pyramid features

为了后续 cost volume construction & aggregation

Distill : **agnostic** to architecture
1. 不要求 student 和 teacher 长得一样，可以直接选成熟的 ImageNet pretrained backbone
2. Teacher
   1. DepthAnything V2
   2. Side-tuning CNN
3. Student
   1. EdgeNeXt-Small : Pre-Trained on ImageNet
   2. feature pyramid head，输出多尺度特征
4. 优于 Model Pruning
   1. pruning 原模型还是得保留 dual module，DepthAnything V2 底下是 ViT，ViT 本身就是主要计算瓶颈
   2. pruning 会导致精度下降，要把精度恢复回来，可能需要重新用 internet-scale 图像大规模训练


backbone 共享同一个权重，分别对左图和右图提取特征

---

# Cost Filtering Block-Wise Search







