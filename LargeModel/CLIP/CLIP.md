# CLIP - Contrastive Language Image Pre-Training

[CLIP - Github](https://github.com/openai/CLIP)

[CLIP 解读 - B站](https://www.bilibili.com/video/BV1SL4y1s7LQ)



结构总览
1. <img src="Pics/clip002.png">
2. 架构
   1. 最小配置 : 文本分支 = Transformer，图像分支 = ResNet
   2. 流行配置 : 文本分支 = Transformer，图像分支 = ViT (两边都是 Transformer，端到端更统一)
3. Pre-Training
   1. $T_1,\dotsm,T_N$ & $I_1, \dotsm, I_N$ 中，每个元素 长度都为 d，代表 N 对 text-image pair 得到的 embedding 结果
      1. 主对角线(蓝色) 代表 正样本，共 $N$ 个
      2. 非对角线(白色) 代表 负样本，共 $N^2 - N$ 个
4. Zero-Shot Prediction
   1. 利用 prompt template 生成文本，**摆脱 categorical label 的限制**(无需定死的标签)
   2. 用 各个{类别}文本 和 图片 计算 cosine similarity

对比学习 需要 大量数据
















相关应用
1. [StyleCLIP: Text-Driven Manipulation of StyleGAN Imagery (ICCV 2021 Oral) - Github](https://github.com/orpatashnik/StyleCLIP)
2. [CLIPDraw: Synthesize drawings to match a text prompt! - Github](https://github.com/kvfrans/clipdraw)
