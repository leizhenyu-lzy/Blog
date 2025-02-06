# Diffusion Model 扩散模型

- [Diffusion Model 扩散模型](#diffusion-model-扩散模型)
- [简介](#简介)
- [原理](#原理)
- [Denoising Diffusion Probabilistic Models(DDPM)](#denoising-diffusion-probabilistic-modelsddpm)
- [Diffusion Model - 李宏毅](#diffusion-model---李宏毅)
  - [浅谈 生成模型 Diffusion Model 原理](#浅谈-生成模型-diffusion-model-原理)
  - [Stable Diffusion、DALL-E、Imagen 背后共同的套路](#stable-diffusiondall-eimagen-背后共同的套路)
  - [Diffusion Model 原理剖析](#diffusion-model-原理剖析)
- [补 : VAE(Variational Auto-Encoder) 变分自编码器](#补--vaevariational-auto-encoder-变分自编码器)
- [补 : 信息量 + 香农熵 + 交叉熵 + KL散度](#补--信息量--香农熵--交叉熵--kl散度)



# 简介

功能
1. 文生图
2. 模仿
3. 抠图填充
4. 图像扩展

模仿 物理(热力学) 扩散现象(熵增，混乱)

inspired by non-equilibrium thermodynamics

给图片增加噪声(正向扩散)，变的混乱(图像收敛于噪声的分布，即高斯分布)

<img src="Pics/diffusion002.png" width=700>

训练模型将其变为有序的样子(逆向扩散)

将 逐渐变的混乱的过程 分解为 多个状态

使用 **马尔科夫链(Markov Chain)** 描述整个加噪声过程(无记忆性)，后一个图片仅依赖前一个图片

使用 信息熵(Information Entropy) 衡量 图片混乱程度
1. $$\mathbf{H}(\mathbf{U})=-\sum_{i=1}^{n} p_{i} \log _{2} p_{i}$$
2. 信息熵可以理解为一个 随机变量的平均信息量，也被称为香农熵
3. 在 不确定性较高的 系统中，信息熵较高，因为需要更多的信息来确定系统的状态
4. 在 确定性较高的 系统中，信息熵较低
5. 指导 神经网络 将混乱图片 变得有序

<img src="Pics/diffusion001.png" width=400>

给图像去噪的过程

扩散模型 相比 变分自编码器 可以将图片更好的打乱，避免过拟合现象



# 原理

<img src="Pics/diffusion003.png" width=600>

<img src="Pics/diffusion004.png" width=600>

<img src="Pics/diffusion005.png" width=600>

单步加噪公式

可以逐层展开，推导 多步等效 公式

$\beta$ 为 预定义的超参数(随 t 增加 而 增大)



<img src="Pics/diffusion006.png" width=600>

<img src="Pics/diffusion007.png" width=600>

<img src="Pics/diffusion008.png" width=600>






# Denoising Diffusion Probabilistic Models(DDPM)

[【较真系列】讲人话-Diffusion Model全解 - B站视频](https://www.bilibili.com/video/BV19H4y1G73r/)

[【大白话01】一文理清 Diffusion Model 扩散模型 | 原理图解+公式推导](https://www.bilibili.com/video/BV1xih7ecEMb/?vd_source=d5863bac06474ffc8562eab966db3af7)
1. [配套PDF](./DDPM_tutorial_by_ZhangXin.pdf)

前向过程，向图像加噪，


---

# Diffusion Model - 李宏毅

[Diffusion Model - 李宏毅 - YouTube](https://www.youtube.com/playlist?list=PLJV_el3uVTsNi7PgekEUFsyVllAJXRsP-)

## 浅谈 生成模型 Diffusion Model 原理

Denoising Diffusion Probabilistic Models(DDPM)

反复使用 同一个 denoise model，输入 step (denoise 到第几步)

denoise model
1. <img src="Pics/lhy001.png" width=500>
2. input 有 noise 的图片，预测 noise，减去 noise (可能 predict noise 简单)


Forward Process (Diffusion Process)
1. input image + 从 gaussian distribution 中 sample 的 noise
2. 对于 noise predictor
   1. 加入 noise 的 image & step步骤数 是 input (对于 text2image 还需 文字描述)
   2. noise 是 GroundTruth output


Text-to-Image
1. 需要 文字&图片 成对资料
2. [LAION-5B: A NEW ERA OF OPEN LARGE-SCALE MULTI-MODAL DATASETS](https://laion.ai/blog/laion-5b)
3. 在 denoise 的 各个 step 中 input 相同的 text
   1. <img src="Pics/lhy002.png" width=500>
4. Predictor 中 加入 text
   1. <img src="Pics/lhy003.png" width=500>

## Stable Diffusion、DALL-E、Imagen 背后共同的套路

Stable Diffusion、DALL-E、Imagen 背后共同的套路
1. 结构
   1. <img src="Pics/lhy004.png" width=500>
   2. Text Encoder (GPT/BERT)
      1. text encoder 对结果 影响大，很重要，相比之下 diffusion model 的大小 影响小
      2. 指标
         1. FID(Fréchet Inception Distance)
            1. <img src="Pics/lhy008.png" width=600>
            2. 越小越好，smaller is better
            3. 使用 CNN 模型 输出的 representation
            4. 需要 sample 很多 image
         2. CLIP Score (Contrastive Language-Image Pre-Training)
            1. Image Encoder & Text Encoder
   3. Generation Model
      1. 和 diffusion model 不同，noise 不是加在图片上，而是加在 中间产物上
      2. 依然是 predict noise
      3. <img src="Pics/lhy010.png" width=600>
   4. Decoder
      1. 一般不需要 文字 信息
      2. 训练，根据中间产物划分
         1. 小图 : 使用 原图 & down-sampling 作为数据集
         2. latent representation(人类看不懂的小图) : 需要 训练 auto-encoder，将 input 转为 latent
            1. <img src="Pics/lhy009.png" width=500>
2. 3个 Module 分开训练，再组合
3. eg :
   1. Stable Diffusion
      1. <img src="Pics/lhy005.png" width=700>
   2. DALL-E (生成模型 : Auto-Regressive / Diffusion)
      1. <img src="Pics/lhy006.png" width=700>
   3. Imagen
      1. <img src="Pics/lhy007.png" width=700>


## Diffusion Model 原理剖析

公式推导论文 - [Understanding Diffusion Models: A Unified Perspective](https://arxiv.org/pdf/2208.11970)


Forward Process (add noise)

Reverse Process (denoise)

**VAE** vs **Diffusion Model**

<img src="Pics/lhy011.png" width=600>

<!-- <img src="Pics/lhy012.png" width=700> -->

**Training**
1. <img src="Pics/lhy013.png" width=500>
2. $x_0$ sample clean image
3. $\epsilon$ sample a noise
4. weighted sum $\bar{α}_1, ..., \bar{α}_T$
   1. t 越大 $α$ 越小 (原图比例少，噪声比例大)
5. 想象中是逐步加入 noise，而实际上 是一步到位，一次加好
   1. <img src="Pics/lhy014.png" width=500>



**Sampling**
1. sample 一个 全是噪音的 图 $x_T$
2. <img src="Pics/lhy015.png" width=700>



图像生成model本质的共同目标
1. <img src="Pics/lhy016.png" width=600>
2. 从 简单的 distribution sample 出 vector (latent variable)
3. 通过 network $G(z) = x$，可能加入 condition(text 等)
4. 得到 Image


Maximum Likelihood Estimation
1. <img src="Pics/lhy017.png" width=600>
2. Network 参数 为 $\theta$
3. $P_{\theta}(x)$ : Network $\theta$ 的 distribution
   1. 具体图像 $x_i$ 的 概率值 $P_{\theta}(x_i)$ 难以计算
4. $P_{data}(x)$ : 真实 数据分布 distribution

Maximum Likelihood 相当于 Minimize KL Divergence
1. <img src="Pics/lhy018.png" width=700>


**VAE** : Compute $P_\theta(x)$
1. <img src="Pics/lhy019.png" width=600>
2. 大多数情况很难通过给定的 latent $z$ 得到 与原图 $x_i$(从 dataset 中 sample 出) 完全一致的 输出 $G(x)$
3. 即 大部分的条件概率 $P_\theta(x|z)$ 的值 都是 0
4. 解决方案 : $G(z)$ 代表 Mean of Gaussian (联想二维高斯分布)
   1. $$p(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$
   2. 显然 正比于 距离的平方
5. Lower Bound of $\log P(x)$ - 通过 最大化 Lower Bound 来 最大化 原函数
   1. 使用 KL散度 恒非负 性质
   2. <img src="Pics/lhy020.png" width=600>


z 的 引入 可能需要查看 VAE encoder-decoder - TODO



**DDPM** : Compute $P_\theta(x)$
1. <img src="Pics/lhy021.png" width=700>
2. 起始点是一个完全由噪声构成的图像，模型通过多个去噪步骤还原图像
3. 每一步的去噪由模型参数化的条件概率 $P_\theta(x_{t-1} | x_t)$ 控制
4. 对 $x_1 ~ x_T$ 进行多元积分 得到 $P_\theta(x_0)$

Lower Bound (DDPM 和 VAE 中的推导类似)
1. <img src="Pics/lhy022.png" width=700>

q 是 概率分布

$q(x_t |x_{t-1})$
1. $\beta _1 : \beta _T$ 是事先定义的
2. <img src="Pics/lhy023.png" width=700>

$q(x_t | x_0)$
1. 不需要逐步加噪 得到 $x_t$，可以直接得到
2. 一次性加噪
   1. <img src="Pics/lhy024.png" width=600>
   2. <img src="Pics/lhy025.png" width=600>
   3. 红框内 二者等价
      1. 考虑独立高斯分布特性
      2. $a \epsilon_1 + b \epsilon_2 \sim \mathcal{N}(0, a^2 \sigma_1^2 + b^2 \sigma_2^2)$
      3. $ (1 - \beta_2) \beta_1 + \beta_2 = 1 - (1 - \beta_1)(1 - \beta_2)$
   4. <img src="Pics/lhy026.png" width=600>
   5. <img src="Pics/lhy029.png" width=700>
   6. <img src="Pics/lhy037.png" width=400>
   7. 相当于是 train 的时候 输入 $t$ & $x_t$



可以计算
1. $q(x_t | x_0)$
2. $q(x_{t-1} | x_0)$
3. $q(x_t | x_{t-1})$
4. **链式法则** : $q(a,b,c) = q(a | b, c) q(b, c) = q(a | b, c) q(b | c) q(c)$



**DDPM** : Lower Bound of $\log P(x)$ (需要 **maximize**)
1. <img src="Pics/lhy030.png" width=1000>
2. KL散度 项 (第2项) 与 Network 无关
   1. $P(x_T)$ 是从 Gaussian Distribution 中 sample
   2. $q(x_T|x_0)$ 是 diffusion process/forward process，是人工定义的
3. $P(x_{t-1} | x_t)$ 是模型可以控制的 (denoise process)
4. $q(x_{t-1} | x_t, x_0)$ : 有 $x_0$ 和 进行t次加噪的结果 $x_t$，但不知道中间过程，求 $x_{t-1}$ 的分布
5. 第3项 (整体需要 maximum 则 第3项本身因为有符号，所以需要最小)
   1. <img src="Pics/lhy027.png" width=600>
   2. 计算 $q(x_{t-1} | x_t, x_0)$ 时，使用了 Markov 假设
   3. 经过下图推导可以知道，$q(x_{t-1} | x_t, x_0)$ 仍然是一个 gaussian distribution
      1. <img src="Pics/lhy028.png" width=1000>
   4. mean & variance
      1. <img src="Pics/lhy031.png" width=600>
   5. 两个 Gaussian Distribution 的 KL Divergence 公式
      1. <img src="Pics/lhy032.png" width=1000>
   6. 捷径 : 想要 minimize
      1. $q(x_{t-1} | x_t, x_0)$ : gaussian distribution，并且 mean & variance 固定，与 network 无关(人工设定的 diffusion process)
      2. $P_\theta(x_{t-1} | x_t)$ : 由 denoise model 的 network 决定，variance 固定(不考虑，都是定值)，只剩 mean 不固定
      3. 因此想要使得 两者的 KL散度 最小，需要 让 二者的 mean 接近 (denoise model 和 理论 denoise 结果)
         1. <img src="Pics/lhy033.png" width=600>
   7. 首先从 database 取 $x_0$，使用 该 $x_0$ sample 出 $x_t$ (本身 $x_t$ 服从正态分布)
   8. denoise model 输入 t & $x_t$，希望 输出的 mean 和 $q(x_{t-1} | x_t, x_0)$ 的 mean 接近
      1. <img src="Pics/lhy034.png" width=700>
   9. mean 还可以继续化简，使用 $x_t$ 表示 $x_0$
      1. <img src="Pics/lhy035.png" width=700>
      2. 实际需要 output(network predict) 其实只有 $\epsilon$ ($\alpha$ 是常数 Hyper-Parameter)
      3. <img src="Pics/lhy036.png" width=400>
      4. 显然，在得到 mean of gaussian 后，又添加了 noise/variance，达到 sample 效果
         1. 如果 选择 mean of gaussian 相当于 选择 概率密度 最大的可能
         2. 猜测 : 对于 LLM，如果下一词 只选择 概率最大的，则会导致反复说同样的语段
         3. diffusion model 相当于是 多步的 Auto-Regressive，Auto-Regressive 本身会加 noise/variance


Diffusion Model 用于 语音合成
1. 相当于 2d -> 1d，从完全随机的序列中 denoise
2. WaveGrad

Diffusion Model 用于 Text
1. Difficulty : 文字离散，因此 难以 加噪 & 去噪
2. Solution
   1. 在 word embedding / latent representation 加 noise
      1. Diffusion-LM, DiffuSeq
   2. 不加 Gaussian Noise
      1. DiffusER : Diffusion via Edit-based Reconstruction

为什么 Diffusion Model 有效
1. 一步到位 -> 查分多步
2. Mask-Predict 思想 : 使用 mask 替代 部分位置(低分位置)，再进行 predict

---

# 补 : VAE(Variational Auto-Encoder) 变分自编码器

AE(Auto-Encoder) 自编码器
1. **自** 表示 自训练
2. 隐藏层 神经元数量少，过滤输入，特征提取，高度压缩
   1. <img src="Pics/diffusion009.png" width=300>


VAE(Variational Auto-Encoder)
1. variation 就是分布 (将输入映射到一个分布上，而非固定变量)
2. <img src="Pics/diffusion010.png" width=600>
3. bottle neck 被分解为两个向量
   1. 均值向量
   2. 方差向量
4. 损失函数
   1. <img src="Pics/diffusion011.png" width=500>
   2. 重建损失 : 与 AE 的 Loss 一致
   3. KL 散度 ： 描述 学习的分布 & 高斯分布 的 相似性
5. 与强化学习结合，进行环境的潜在空间表示


GMM - TODO



---

# 补 : 信息量 + 香农熵 + 交叉熵 + KL散度

**信息量 (Amount of Information)**
1. 小概率事件，信息量大 | 大概率事件，信息量小
2. 独立事件，信息量可以相加
3. $$I(x) = \log _2 (\frac{1}{p(x)}) = - \log _2 (p(x))$$


**香农熵 (Shannon Entropy)** - 对于单个分布
1. 概率分布的期望信息量
2. $$H(p) = \sum_i p_i \log _2(\frac{1}{p_i}) = -\sum_i p_i \log_2(p_i)$$
3. 概率密度越均匀，也就是越随机，熵越大
4. 概率密度越集中，也就是越确定，熵越小 (小概率事件 : 大信息量 × 小概率)

**交叉熵 (Cross-Entropy)** - 对于两个分布 求差异
1. p **真实分布** & q **预测/拟合分布**
2. $$H(p, q) = \sum_i p_i \log _2(\frac{1}{q_i}) = -\sum_i p_i \log_2(q_i)$$
3. 如果真实分布是 p，用 q 来描述数据时，所需的平均编码代价是多少
4. 用 q 模型去解释 p 数据时的效率和准确性
5. $H(p,q)$ ==不等于== $H(q,p)$
6. 在深度学习中，分类模型 (eg : Softmax 分类器) 输出的是预测分布 q(x)，真实标签对应一个分布 p(x) (通常是独热编码)，交叉熵损失函数用于量化预测分布 q 和真实分布 p 的差异
   1. 对于 语义分割模型，相当于是 对 每个 pixel 都求 cross-entropy (每个 pixel 都是一个 softmax 得到的 概率分布 **结合** 实际的 one-hot ground-truth) 再进行 平均
7. 交叉熵越**小**，说明 预测分布 q 越 **接近** 真实分布 p
   1. 对于 $\sum_i p_i \log _2(\frac{1}{q_i})$，显然，当 $p_i$ 大 时，需要 $q_i$ 同时也大(分布接近)，否则 $\log _2(\frac{1}{q_i})$ 将会较大，使得 大概率 × 大信息量

**KL 散度 (KL Divergence)** - $D_{KL}(p||q)$
1. p **真实分布** & q **预测/拟合分布**
2. **$D_{KL}(p||q)$(前向散度)** ==不等于== **$D_{KL}(q||p)$(反向散度)**
3. $$D_{KL}(p||q) = E_p[log\frac{p}{q}] = \sum p \log \frac{p}{q}$$
   1. 比值 + 对数 + 期望
4. 前向散度 用于 监督学习，反向散度 用于 强化学习/变分推断
5. 分布相似时，两种散度都很小
6. 性质
   1. KL散度 恒 非负 $D_{KL}(p||q) \geq 0$ (Gibbs Inequality 吉布斯不等式)
      1. 当且仅当，p=q 时，$D_{KL}(p||q) = 0$
   2. KL散度 不对称，不是一个严格的距离度量
7. 模型训练中，最小化 KL散度 等价于 最小化 交叉熵，因为 只有预测分布 $q_\theta$ 才与模型有关，真实分布 $p$，与模型参数无关，因此一般没有 KL散度 损失函数，直接 交叉熵 损失函数

交叉熵 & KL 散度(Kullback-Leibler Divergence) 关系
1. $$D_{KL}(p||q) = H(p, q) - H(p) = \sum_i p_i \log _2(\frac{1}{q_i}) - \sum_i p_i \log _2(\frac{1}{p_i}) = \sum_i p_i \log _2(\frac{p_i}{q_i})$$
