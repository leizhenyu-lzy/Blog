# Vector Quantization

把 **连续表征**（音频 / 图像 encoder 输出的 embedding）离散化成 **token** 的一类方法
1. 和 `tokenizer.md` 的 BPE 同一抽象层级（连续信号 → 离散 token），只是模态不同
2. ⚠️ 区分 `Quant/` 的**模型权重量化**(FP32→INT8)：那是压缩权重加速推理，这里是 codebook 离散化，只是中文都叫"量化"

家族
1. Codebook 码本 系 : VQ-VAE → RVQ
2. LookUp-Free 系 : FSQ / LFQ / BSQ
3. 经典 ANN 系 : PQ
4. 软量化 系 : Gumbel-Softmax / dVAE
5. 音频专用变体 : SpeechTokenizer / Mimi

为什么要离散化
1. **接自回归 / 掩码 Transformer** : LLM 只吃离散 token，图像/音频先量化才能进 GPT 式模型生成
2. **压缩 (codec)** : 一段信号用少量 codebook 索引表示，比特率可控
3. **跨模态统一** : 文本/音频/图像都变 token，喂进同一个 Omni 模型

代价
1. 量化**有损**，离散化引入误差
2. `argmin` 最近邻查找**不可导**，反传需技巧(STE)


---


# VQ-VAE

确立 连续 -> 离散 token 的范式

可学习 codebook + 最近邻查找 + 直通估计(STE)反传

**核心** : 用可学习码本 $E=\{e_1,...,e_K\}$，把 encoder 输出的连续向量**就近替换**成码本里某个向量

流程
1. Encoder : $x \rightarrow z_e(x)$（连续向量）
2. **量化(最近邻)** : $k=\arg\min_j \|z_e(x)-e_j\|_2$，取 $z_q(x)=e_k$
3. Decoder : $z_q(x) \rightarrow \hat{x}$ 重建
4. 序列里最终存的是**索引 $k$**（整数 token），不是向量

**直通估计 (Straight-Through Estimator, STE)**
1. `argmin` 不可导，前向用 $z_q$，反传时**直接把 $z_q$ 的梯度拷给 $z_e$**
2. 代码 : `z_q = z_e + (z_q - z_e).detach()`，前向值是 $z_q$，梯度走 $z_e$

**损失函数** : 三部分（sg = stop gradient）
1. **重建损失** : $\|x-\hat{x}\|^2$，管 encoder/decoder
2. **码本损失** : $\|sg[z_e]-e\|^2$，把**码本向量**拉向 encoder 输出
3. **承诺损失(commitment)** : $\beta\|z_e-sg[e]\|^2$，让 **encoder 输出**别乱跑、贴住码本（$\beta$ 常取 0.25）

$$L = \|x-\hat{x}\|^2 + \|sg[z_e]-e\|^2 + \beta\|z_e-sg[e]\|^2$$

**训练老大难 : 码本坍缩 (codebook collapse)**
1. 现象 : 只有少数码字反复被命中，大部分"死掉"，等于浪费词表
2. 根因 : 死码字拿不到梯度 → 更新不了 → 永不被选中（恶性循环）
3. 对策
   1. **EMA 更新码本** : 不用码本损失，改用 encoder 输出的指数滑动平均更新码字，更稳
   2. **码本重置 (reset)** : 把长期没命中的死码字重新初始化到当前 batch 的某个 encoder 输出
   3. **k-means 初始化** : 首个 batch 做 k-means 初始化，别纯随机
   4. **低维码本 + L2 归一化** (improved VQGAN) : 投到低维再算距离并归一化，利用率显著提升

衍生
1. **VQ-VAE-2** : 层次化多尺度码本
2. **VQGAN** : VQ-VAE + 对抗 loss + 感知 loss，图像 tokenizer 经典（MaskGIT / Parti 基础）


# RVQ

VQ-VAE 单码本容量不够、码率低

多级码本级联，每一级量化上一级的残差，比特率可叠加

**核心** : coarse → fine 逐级细化，每级只量化上一级留下的**残差**
1. $r_0 = z$
2. 第 1 级 : $q_1 = VQ_1(r_0)$，残差 $r_1 = r_0 - q_1$
3. 第 2 级 : $q_2 = VQ_2(r_1)$，残差 $r_2 = r_1 - q_2$
4. ... 共 $N_q$ 级，每级各有**独立码本**
5. 最终 : $\hat{z} = \sum_{i=1}^{N_q} q_i$

特点
1. **比特率可叠加** : 每多一级码本就多 $\log_2 K$ 比特，码率随级数线性可控
2. **Quantizer Dropout** : 训练时随机只用前几级 → 一个模型支持**可变比特率**（前几级=低码率粗糙版）
3. **音频 codec 事实标准** : SoundStream / EnCodec / DAC 全是 RVQ
4. 图像版叫 **RQ-VAE**（残差量化 + RQ-Transformer）


---


# FSQ

VQ 的老毛病：码本坍缩 / 利用率低 / 要辅助 loss

干脆扔掉可学习码本，每个维度量化到固定几个标量档位，codebook 变成隐式网格

**核心** : 把向量投到**很低的维度** $d$(如 3~6 维)，**每维**独立量化到固定的 $L$ 个标量档位
1. 每维先用有界函数(如 $\tanh$)压到固定范围
2. 再**四舍五入**到 $L$ 个档位（round 用 STE 反传）
3. **隐式码本** = 各维档位的笛卡尔积，大小 $=L_1\times L_2\times...\times L_d$
   1. 例 : 档位 `[8,5,5,5]` → $8\times5\times5\times5 = 1000$ 个码字
4. token 索引 = 各维档位组合编码出的整数

优点
1. **不会坍缩** : 网格每个点天然可达，利用率几乎 100%
2. **超简单** : 无码本损失、无承诺损失、无 EMA，只剩重建损失
3. 大码本下效果追平甚至超过 VQ


# LFQ (Lookup-Free Quantization)

MAGVIT-v2 提出，每维二值量化，隐式词表可以非常大

1. 每维量化到 $\{-1,+1\}$（二值），隐式码本 $2^d$，token 索引=二进制数
2. 可看成 **FSQ 每维只取 2 档**的特例，但 $d$ 一大词表就极大
3. 配**熵正则**鼓励码字利用率（防坍缩）
4. 是当下**图像 / 视频 tokenizer** 新主流之一


# BSQ (Binary Spherical Quantization)

先归一化到超球面再二值化

1. 先把向量 L2 归一化投到**超球面**，再对每维二值量化
2. 有界、好训，性质比裸二值更稳

**无码本派对比 (FSQ / LFQ / BSQ)** : 都属"不学显式码本、用隐式网格"这一派

| 方法 | 每维档位 | 隐式码本 | 备注 |
|---|---|---|---|
| FSQ | $L$ 个标量档位 (5、8…) | $\prod_i L_i$ | 最通用 |
| LFQ | 2 个 (二值 $\{-1,+1\}$) | $2^d$ | MAGVIT-v2 + 熵正则 |
| BSQ | 2 个 (先归一化超球面) | $2^d$ | 有界好训 |


---


# 经典 ANN 系 (PQ)

**Product Quantization** : 来自最近邻检索 (FAISS) 的经典量化
1. 把 $D$ 维向量**切成 $M$ 段子向量**，每段用各自小码本独立量化
2. 等效码本 $K^M$，但只需存 $M\times K$ 个码字
3. 和 RVQ 的关系（都是"多码本"近亲）
   1. **PQ** : 切**子空间**并行量化（维度上切分）
   2. **RVQ** : 对**残差**顺序量化（精度上细化）
   3. Additive / Group VQ 也属此类


# 软量化 系

**Gumbel-Softmax VQ / dVAE**
1. 不做硬最近邻，而在码本上输出**软分布**，用 Gumbel-Softmax 采样，温度逐步退火变硬
2. 好处 : 全程可导，绕开 STE
3. 代表 : **DALL-E v1 的 dVAE**


# 音频专用变体

**SpeechTokenizer / Mimi (Moshi)** : 在 RVQ 基础上把**第一级码本**用语义模型蒸馏
1. 第一层用 HuBERT / wav2vec **蒸馏**，token 偏"语义"；后续层补"声学细节"
2. 让离散音频 token 既能重建波形、又对 LLM 友好
3. 这正是 **Qwen-Omni** 这类模型音频 tokenizer 的设计思路出发点


---


# 参考

1. [VQ-VAE : Neural Discrete Representation Learning (2017)](https://arxiv.org/abs/1711.00937)
2. [VQ-VAE-2 (2019)](https://arxiv.org/abs/1906.00446) / [VQGAN : Taming Transformers (2020)](https://arxiv.org/abs/2012.09841)
3. [SoundStream : RVQ 音频 codec (2021)](https://arxiv.org/abs/2107.03312)
4. [EnCodec (2022)](https://arxiv.org/abs/2210.13438) / [DAC (2023)](https://arxiv.org/abs/2306.06546)
5. [FSQ : VQ-VAE Made Simple (2023)](https://arxiv.org/abs/2309.15505)
6. [MAGVIT-v2 : LFQ (2023)](https://arxiv.org/abs/2310.05737) / [BSQ (2024)](https://arxiv.org/abs/2406.07548)
