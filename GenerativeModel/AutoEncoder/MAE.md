# MAE : Masked Autoencoders Are Scalable Vision Learners

[MAE - Github](https://github.com/facebookresearch/mae)

[MAE 论文逐段精读【论文精读】 - B站(李沐)](https://www.bilibili.com/video/BV1sq4y1q77t)

---

MAE，基于 ViT，可以看作是 BERT(NLP 任务，完形填空) 的 CV 版本

MAE 是一种思想，不是只能使用 ViT

Auto 表示 self(自)，**用输入本身作为监督信号**

scalable self-supervisied

Core Design : 更好 更快(只能看到 $\frac{1}{4}$)
1. asymmetric(非对称) encoder-decoder
   1. encoder 只对 visible 的 patch 编码
   2. decoder 轻量
2. mask 高比例(75%) 得到 自监督任务，有挑战性的任务 迫使 模型学习 representation


实际使用时，不需要 decoder，使用 encoder 即可，也不需要 掩码

representation learning 通过 encoder 得到表征

CV & NLP 区别
1. NLP : 词 是 语义的单元
2. CV  : patch 虽然含有一定语义信息，但不是语义的 segment(可能是 多个物体叠加/物体的某个部分)



encoder 只需要处理 visible

decoder 同时要处理 visible & mask token
1. 所有 token 都需要加上 position encoding，包括 visible & mask
   1. visible 虽然加过一次 position encoding，但是 两套位置编码 各自服务于各阶段的注意力
2. mask token 最开始是 同一个可学习向量

只对 mask 部分计算 MSE，没有盖住的部分，输入已经看到对应像素信息

可见位置的 预测值 本身不进损失，但参与计算，从而让梯度通过自注意力回流到可见 token 与编码器(要为 完整序列 Token 构造 Q & K & V)

可选的 Normalization，每一个块内的像素变成 : 均值为0 & 方差为1

效果对比
1. ViT
2. ViT + strong regularization
3. MAE 方法 pretrain ViT + fine-tuning


Figure8 比较 并不公平，IN1K & JFT300M 类别差别大，并且最终 eval 在 IN 验证集


