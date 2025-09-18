# GAN - Generative Adversarial Network


[Understanding GANs (Generative Adversarial Networks) - YouTube(DeepBean)](https://www.youtube.com/watch?v=RAa55G-oEuk)

类似 counterfeiter(伪造文件的人) & police(警察)
1. 前者 : Generative Model
2. 后者 : Discriminator

对抗学习框架 Adversarial Learning Framework
1. <img src="Pics/gan001.png" width=600>
2. Discriminator 区分 Real/Generated Samples
3. Generator 试图 欺骗 Discriminator，最终实现 生成真实图像，得到 Generative Model

Motivation
1. 对于 输入数据 x，希望训练模型，获取 data space 中的 target distribution
2. <img src="Pics/gan002.png" width=400>
3. generative model 能够，通过 从 distribution 中 采样，生成 novel sample
4. <img src="Pics/gan003.png" width=500>
5. Dataset D : data space 中的 点集，理解为 这些点 是 从 underlying 分布 $p^*(x)$  中进行抽取，是 Ground Truth Generative Procedure，但是 该 Procedure 是未知的
6. 只能使用 $p(\theta)$ 来近似 $p^*(x)$
7. Generative Model 的目的就是 优化 $\theta$

