# ViT



[ICLR Oral Presentation](https://iclr.cc/virtual/2021/oral/3458)

[Transformer 个人笔记](../Transformer/Transformer.md)


## Table of Contents

- [ViT](#vit)
  - [Table of Contents](#table-of-contents)
- [VIT(Vision Transformer) 深度讲解 - B站(RethinkFun)](#vitvision-transformer-深度讲解---b站rethinkfun)



---

# VIT(Vision Transformer) 深度讲解 - B站(RethinkFun)

[VIT(Vision Transformer) 深度讲解 - B站(RethinkFun)](https://www.bilibili.com/video/BV15RDtYqE4r/)

结论
1. Transformer 模型 可以不做改动 来解决 CV 问题 (ViT 证明 transformer 架构的 通用性)
2. 小规模数据上 略输 CNN，中等或者大规模数据集上 表现 相当于/优于 CNN
3. 在计算效率上，训练同等精度的模型，Transformer 比 CNN 更有优势

图像 转为 Token序列
1. ViT 论文名 : image = 16×16 words
2. 图片 按固定大小 分为 **patch**，作为 语义单元，不按照单个 pixel
   1. 防止 序列过大，计算复杂度过大
   2. 单个 pixel 只有 RGB 值，语义信息太少，用大向量 embedding 浪费
3. H×W×C 个 patch -> flatten




---

[ViT论文逐段精读【论文精读】 - B站(bryanyzhu)](https://www.bilibili.com/video/BV15P4y137jb)

挑战 2012年 AlexNet 以来，CNN 在 CV 中的 统治地位

在足够多的数据上进行 pre-train，可以不使用 CNN，直接使用 NLP 的 Transformer 解决问题

打破 CV & NLP 在模型方面的壁垒，在 multi-modality 方面也挖坑



