# Transformer


[Transformer论文逐段精读 - 李沐(B站)](https://www.bilibili.com/video/BV1pu411o7BE)

[王树森](https://www.bilibili.com/video/BV1dK411k74q)

[妹子](https://www.bilibili.com/video/BV1xoJwzDESD)

[Transformer 常见问题与回答总结 - 知乎](https://zhuanlan.zhihu.com/p/496012402?)

## Table of Contents

- [Transformer](#transformer)
  - [Table of Contents](#table-of-contents)
- [RethinkFun - B站](#rethinkfun---b站)
- [月来客栈 - B站](#月来客栈---b站)
  - [00 - 传统 注意力机制 \& 归一化](#00---传统-注意力机制--归一化)
  - [01 - 多头注意力机制原理](#01---多头注意力机制原理)
  - [02 - 位置编码 \& 编码解码 过程](#02---位置编码--编码解码-过程)
  - [03 - 网络结构 \& 自注意力 实现](#03---网络结构--自注意力-实现)
  - [04 - Transformer 实现过程](#04---transformer-实现过程)
  - [05 - 基于 Transformer 的 翻译模型](#05---基于-transformer-的-翻译模型)
  - [06 - 基于 Transformer 的 对联生成模型](#06---基于-transformer-的-对联生成模型)
- [DeepBean - YouTube](#deepbean---youtube)


---

# RethinkFun - B站

[大模型修炼之道 : Transformer : Attention is all you need - B站](https://www.bilibili.com/video/BV1FH4y157ZC/)

只使用 attention 机制，解决 seq2seq 问题，最早 Google 用于 翻译问题

String -> Token -> Token ID -> Embedding Vectors


**Tokenize**
1. 使用 已有字典 对句子 分词 (最长匹配优先)
   1. 构建字典的时候也会有特殊的方法，考虑 token 的常用程度 和 字典大小
      1. BPE(Byte Pair Encoding)
      2. WordPiece
      3. SentencePiece
      4. Unigram
2. 转为 Token ID (lookup table)


**Embedding**
1. 对每个 token 分配一个 **可学习的 参数向量**(高维空间)
2. 每个维度 代表 某种**语义**
3. 向量之间的相对关系(向量相减) 也有一定语义
4. 传统 embedding 问题 : 学习完成后 embedding 固定，不能根据上下文进行调整
   1. 同一个词不同含义但是 embedding 相同
   2. <img src="Pics/rethinkfun003.png" width=600>
5. 不同阶段
   1. 预训练阶段 : embedding 随机初始化，和模型一起训练
   2. 微调阶段 : 使用预训练好的 embedding，继续和模型一起微调

**Self-Attention**
1. 通过 token 之间 彼此的注意力，让 token 根据上下文，更新自己的 embedding
2. 每个 token 有初始的 embedding，通过 3个 **线性层** 映射，得到 3个 向量
   1. Q : 向其他 token 查询
   2. K : 对查询应答
   3. V : 更新其他 token embedding
3. <img src="Pics/rethinkfun004.png" width=600>
4. **相似性匹配** Q & K 点积(自己的 Q & K 也会点积)，不同 token 组成 相似度向量，Softmax，加权求和
   1. $V_s = [Q_4 * K_1, Q_4 * K_2, Q_4 * K_3, Q_4 * K_4]$，再 softmax 转为 概率，再和 V向量 进行对应相乘


有时候会为了补齐不同长度的句子，而使用 `<PAD>`，训练的时候，也有对应的 mask 来过滤


**MultiHead Self-Attention**
1. 类似 CNN 每层 可以指定多个 卷积核
2. Self-Attention 可以指定多个 Head，**多次线性映射**，得到多组 Q & K & V，不同组的向量 拼接起来，通过 矩阵运算 加速计算
3. **实际上 总特征数不变**，平均分给多个 head (相当于头变小了)，再 **concat** 得到完整的
4. <img src="Pics/rethinkfun005.png" width=700>
5. K 转置 就是为了 和 Q 点乘，得到 更新 百分比
6. 除以 $\sqrt{d_k}$($d_k$ 是 **特征向量维度**)，均值不变，调整方差(保证为1)
   1. 原始的 Q & K 向量，每个维度都服从 标准正态分布(均值为 0，方差为 1)
   2. 当2个 独立的 服从标准正态分布的 随机变量 相乘时，积的方差是 1
   3. 点积(Dot Product) 是将 $d_k$ 个这样的乘积 加在一起
   4. 只要 不相关/独立，方差是可加的，$d_k$ 个方差为 1 的数加起来，总方差就变成了 $d_k$
8. feature size 必须整除 头的数量
9. <img src="Pics/rethinkfun006.png" width=700>

==P.S. : `@` 运算符在 PyTorch 中 只在最后2个维度 进行矩阵乘法，前面的维度作为 batch 维度进行广播==

**Layer Normalization** - [个人笔记](../../DeepLearning/D2L/d2l.md#28-batch-normbn--layer-normln)
1. 统计每个 Token 的 mean & var(对每个 Token 独立计算)，进行标准化
2. 加入 很小 $\epsilon$ 防止 ÷0
3. **每个特征维度** 都有 可学习参数 $\gamma$ & $\beta$
4. <img src="Pics/rethinkfun007.png" width=600>
5. `torch.nn.Parameter` 用来把一个 Tensor 注册成 `nn.Module` 的可学习参数
6. Layer Norm 位置
   1. Post-LN(原版) : 先 MHA + Dropout，然后 Residual Add，再 Norm (Add & Norm)
   2. Pre-LN (常用) : 先 Norm，然后 MHA + Dropout，再 Residual Add
7. 原始 Transformer 里，用到 LayerNorm 的地方
   1. Encoder Layer 中 (每层 2 个)
      1. Self-Attention 后 : LayerNorm(x + Attention(x))
      2. FFN 后 : LayerNorm(x + FFN(x))
   2. Decoder Layer 中 (每层 3 个)
      1. Masked Self-Attention 后 : LayerNorm(x + MaskedAttn(x))
      2. Cross-Attention 后 : LayerNorm(x + CrossAttn(x))
      3. FFN 后 : LayerNorm(x + FFN(x))
   3.  是否有 最后再整体加一个 LayerNorm ?
      1. 原始论文 `Attention is All You Need` 里，没有在整个 Encoder/Decoder 输出最后再加一个额外的 LayerNorm
      2. 很多后来的实现(一些开源库)会在
         1. 整个 Encoder 堆叠的输出后，再加一层 LayerNorm
         2. 整个 Decoder 堆叠的输出后，再加一层 LayerNorm


**Residual Connection** 残差连接 : 避免梯度消失，尤其是网络层数变深

**Feed Forward Network** : linear + relu + dropout + linear

MHA & FFN 都配合一个 Residual 残差连接

Encoder **输入 & 输出** 维度一致，可以多个 block 叠加，原文是 6个

**Position Encoding**
1. Attention 机制 **没有考虑位置关系**，只是 weighted-sum (eg : 我打他 ≠ 他打我)
2. **不能使用 离散的 绝对位置编码**，模型没法处理 推理句子的 token 数 **>** 训练句子 token 数 的情况
3. 位置编码维度 和 原始编码维度 一致
4. 可以将 离散编码 转为 **连续编码**，周期变换，低维度变化快，高维度变化慢 (有点类似于 二进制 的连续化版本)
   1. 三角函数 sin/cos 可以调整 频率
   2. 频率高的 三角函数作为 低维度，频率低的 三角函数作为 高维度
   3. <img src="Pics/rethinkfun001.png" width=500>
   4. 实际上 Transformer 使用的是 **==sin/cos 交替编码==**，2个相邻维度$(2i, 2i+1)$ 看为一组，使用同一个频率
   5. <img src="Pics/rethinkfun002.png" width=500>
   6. 好处 : 仅和 **相对位置** 有关，和 绝对位置 无关
5. $sin/cos(\omega t)$ 中，pos 相当于 t，feature 维度 $i$ 控制 角频率 $\omega$
6. <img src="Pics/rethinkfun008.png" width=600>
7. 随着维度增加，角频率变小，对应 高维 频率低

完整的序列是 : `['<bos>', 'I', 'like', 'to', 'eat', 'apple', '<eos>']`
1. Decoder Input  : `['<bos>', 'I', 'like', 'to', 'eat', 'apple']`
2. Decoder Output : `['I', 'like', 'to', 'eat', 'apple', '<eos>']`

**Mask Attention**
1. 一次性 对所有位置进行训练
2. 推理时，还是需要 一个个的 token 进行输出
3. mask 为1 的位置，表示可以看到 token，可以进行 attention 计算
4. 让每个 token 只关注 **自己** & **之前** 的tokens
5. attention 正常计算，在 **softmax 之前**，将 mask 为0 的位置 替换为 **很大的负值**
6. Mask 的尺寸
   1. 随着你 每一批(Batch) 数据的最大长度 $L$ 动态变化的
   2. Mask 的最大上限 是 模型设计的 最大上下文窗口，也不能超过 Max Position Embeddings 最大位置编码长度
7. **隐式增广** : 当你把一整句话喂给模型时，模型在内部实际上通过 Causal Mask (因果掩码) 同时学习了所有可能的切分

**Cross Attention**
1. `Encoder 的 K & V` + `Decoder 的 Q`
2. Encoder 的输出(Encoder Output) 会被 广播(Broadcast) 给 Decoder 的每一层，Decoder 每一层，使用的是 相同的 Encoder Output
3. 经过 Linear 将 输出维度 映射到 字典大小，再 Softmax

**单向 & 双向 Attention**
1. **Encoder** 的 Self-Attention 双向注意力，前面的 token 可以看到后面的 token，所有 token 之间可以相互匹配
2. **Decoder** 的 Self-Attention 单向注意力，带 Causal/Look-Ahead Mask，前面的 token 不能看到后面的 token，只能看到自己及之前的 token

Encoder & Decoder 不改变数据尺寸

在推理(Inference) 阶段，**Decoder** 中数据的形状(Sequence Length 维度)确实是在不断变化的
1. Self-Attention : Q、K、V 的长度都会随着生成的词数同步增加
2. Cross-Attention : Q 的长度会增加，但 K 和 V 的长度永远固定，等于原文长度
3. 也就是生成长文本越到后面越慢的原因(每次计算的矩阵都变大)
4. 模型的参数量(Model Parameters) 不变，参数矩阵只负责处理特征维度，不关心序列长度

**Word Selection**
1. linear / Projection Layer
   1. 输入尺寸 : `(1, L, d)`
   2. linear 尺寸 : `(d vocab_size)`
   3. 输出尺寸 : `(1, L, vocab_size)`
      1. 包含了过去 10 个位置每一个位置的预测结果，但在推理预测下一个词时，我们只关心最后一个位置
2. softmax

**Seq Length ($L$) 长度的影响**
1. Q/K/V 矩阵 : 随着 input 长度 $L$，线性增长 (如果 特征维度 不变)
2. Attention Score 矩阵 : softmax 是针对 归一化的 $Q K^T$，因此 随着 input 长度 $L$，平方增长

**不同任务**
1. **自回归生成**(Auto-regressive Generation) - 这里仅考虑 最经典的 Encoder-Decoder 架构，不考虑 Decoder-Only
   1. Encoder 读全文
   2. Decoder 给个 `<bos>` 信号开始
   3. Loop 拿着结果接着续写
2. **代码补全**(Code Completion)
   1. 使用 FIM (Fill-In-the-Middle)，把代码切成 Prefix, Middle, Suffix
   2. 把 Prefix + Suffix 给 Encoder (或作为 Prompt)，让 Decoder 生成 Middle


[Source Code - Github](https://github.com/hkproj/pytorch-transformer/blob/main/model.py)


---

# 月来客栈 - B站

[月来客栈 - B站合集](https://space.bilibili.com/392219165/lists/4900590?type=season)

## 00 - 传统 注意力机制 & 归一化

硬注意力 : one-hot 编码

软注意力 : 概率分布

BatchNorm 批量归一化
1. 靠近 input  的 layer，对应的 **梯度小**，权重更新慢
2. 靠近 output 的 layer，需要根据 靠近 input 的 layer 的变换，前向传播，重新适应数据分布
3. 解决方法 : 添加一层归一化层，是的每一层 input 的分布都尽可能接近 标准正太分布


## 01 - 多头注意力机制原理

## 02 - 位置编码 & 编码解码 过程

## 03 - 网络结构 & 自注意力 实现

## 04 - Transformer 实现过程

## 05 - 基于 Transformer 的 翻译模型

## 06 - 基于 Transformer 的 对联生成模型




---

# DeepBean - YouTube

[Transformers, Simply Explained | Deep Learning -  - YouTube(DeepBean)](https://www.youtube.com/watch?v=UPhaYex4zZk)

解决 旧架构(eg : RNN) 中的问题
1. Long-Range : information 难以保持 很多步 timestamps
2. Parallel   : 需要类似自回归方式，难以并行(train & inference)
   1. RNN /LSTM /GRU : 训练 & 推理 都无法并行
   2. Transformer
      1. 推理 inference : 无法并行
         1. 要 一个词接一个词 地生成，整体流程是自回归的，无法在时间维度上并行
         2. 使用 因果掩码(causal mask)，保证位置 t 只能看到 ≤ t 的 token
         3. 序列内并行(注意力计算、前馈层 等)，时间步串行(每轮产生一个或一批 新token，再喂回模型)
      2. 训练 training : 可以并行
         1. 采用 teacher forcing，完整目标序列已知
         2. 因果掩码阻断未来信息
         3. 可以并行计算 Loss

Basic Idea : **Self-Attention**
1. 序列中的 每一个单词 都根据一定的 注意力分数 和 另一序列的单词 相连
2. 自注意力机制，两个序列相同
3. <img src="Pics/transformer003.png" width=500>


Operation
1. Inference
   1. <img src="Pics/transformer001.png" width=500>
2. Training
   1. <img src="Pics/transformer024.png" width=500>
3. input  ： 包含 开始token(`<START>`) & 结束token(`<END>`)
4. output :
5. 模型被分为两个部分
   1. Encoder : 利用 self-attention 机制 得到 input 的 abstract representation
   2. Decoder : 利用 representation 一次一个字的输出句子
      1. 开始接收 开始token(`<START>`)
      2. 结合 Encoder 输出 得到 Decoder 输出
      3. 将其最后一个词 append 给 output
      4. output 再传入 decoder
      5. 不断循环直到 结束token(`<END>`)


Architecture
1. <img src="Pics/transformer002.png" width=700>
2. Word/Token Embedding
   1. 语义相近的组成 cluster
   2. String -> Token -> Token ID -> Embedding Vectors
      1. 前两步 不受训练影响
      2. <img src="Pics/transformer004.png" width=500>
      3. Token 不必是单词，可以是 words / sub-words / letters(对于非自然语言用途)
      4. Tokenization 使用 **lookup table** 完成
         1. <img src="Pics/transformer005.png" width=500>
         2. embedding vector 的实际数据是 训练中学习的，不需要 pre-trained embedding
      5. 特殊 Tokens : `<START>`, `<END>`, `<UNK>`(unknown), `<PAD>`(保证相同序列长度)
3. Positional Encoding
   1. 对于 RNN，位置信息 隐式提供，token 按顺序输入模型，但是 **transformer 的 token 是 并行输入**
   2. <img src="Pics/transformer006.png" width=400>
   3. 参数
      1. `pos` : token 在序列中的位置 (Position index)
      2. `i`   : 向量维度索引 (Dimension index)
   4. 位置编码和原始编码 长度一致，直接相加
   5. 生成 位置编码的函数 可以学习，论文中使用硬编码
      1. <img src="Pics/transformer007.png" width=400>
      2. 注意 : 上面的 公式和原文有所出入，以原文为准
         1. <img src="Pics/transformer030.png" width=400>
      3. <img src="Pics/transformer008.png" width=500>
   6. <img src="Pics/transformer009.png" width=500>
4. Encoder (Multi-Head Attention & FeedForward 多组堆叠)
   1. Self-Attention : Query Sequence = Context Sequence (Query Token -> Context Token)
      1. <img src="Pics/transformer011.png" width=187> <img src="Pics/transformer010.png" width=250>
      2. Attention 可以理解为 Query 通过匹配 Key 访问 Value
      3. <img src="Pics/transformer012.png" width=350>
      4. <img src="Pics/transformer013.png" width=320>
   2. 归一化
      1. <img src="Pics/transformer014.png" width=370>
      2. 第2个公式中，常数 $a$ 约掉
      3. 除以 $\sqrt{d_k}$ 的原因
         1. 点积的方差 随着 维度增长 而变大
            1. 以 $\mathcal{N}(0,1)$ 为例，假设 query & key 的每个维度 都服从 标准正态分布
            2. 每一维度乘积 $q_i · k_i$ 的 均值为0，方差为1 (独立正态乘积)
            3. 总点积 $s = q · k = \sum_{i=1}^{d} q_i · k_i$，均值为0 方差为$d_k$
         2. 大数值进入 softmax 会 过度尖锐，反向传播时梯度几乎只流向极少几个位置
         3. 通常不会计算 `<PAD>` token
   3. 矩阵形式
      1. <img src="Pics/transformer015.png" width=370>
      2. 对于 self-attention，**seq_len_q = seq_len_k = seq_len_val**
      3. <img src="Pics/transformer016.png" width=400>
      4. Softmax 是 Per-Query，也就是 按行 softmax
   4. Attention HeatMap & Mask
      1. <img src="Pics/transformer017.png" width=400>
      2. softmax 中 不考虑 `<PAD>` token，在 softmax 前，使用 掩码矩阵，element-wise 乘法，注意 mask 的值 是 1/$-\infty$
      3. <img src="Pics/transformer018.png" width=500>
   5. 整体流程
      1. <img src="Pics/transformer019.png" width=500>
      2. 其中，Q、K、V 矩阵是通过 将 Embedding X 分别通过 线性层/矩阵变换 得到的，所以 只需要 X 作为输入
      3. <img src="Pics/transformer020.png" width=200> <img src="Pics/transformer021.png" width=317>
   6. Multi-Head
      1. 多头 对应 不同的 Linear，可以 捕捉不同方面
      2. 使用 `concat` 形成一个大矩阵
      3. 通过 线性层，再和 输入 X 进行 element-wise 相加，得到输出 Y
      4. <img src="Pics/transformer022.png" width=500>
      5. 没有硬性限制 Multi-Head 必须不同，但 参数随机初始化 + 训练动力学(Dropout、LayerNorm、Mini-Batch) + 输出融合层的梯度需求，会自然驱动它们走向差异化
   7. 原文 n_heads = 8，n_encoders = 6
5. Decoder
   1. 整体结构和 Encoder 类似，但有**关键区别**
   2. Causal/Look-Ahead Mask
      1. 确保 Query Token 不能去匹配 Context Sequence 中 更后面的 Token
         1. <img src="Pics/transformer023.png" width=400>
      2. 在训练阶段 模拟 推理时可见的信息范围，防止未来信息泄漏
      3. 同时结合 Padding Mask & Causal Mask
         1. <img src="Pics/transformer025.png" width=500>
      4. 整体流程
         1. <img src="Pics/transformer026.png" width=500>
   3. Cross-Attention
      1. 和 Self-Attention 基本类似，只是 **Q、K、V 来源不同**
         1. Q : Target Sequence，去检索 Encoder Output 中的 有用信息
         2. K、V : Encoder 得到的 abstract representation，长度固定
      2. 注意 K、V、Q 的位置
      3. <img src="Pics/transformer027.png" width=500>
   4. 原文 n_heads = 8，n_decoders = 6
6. Word Selector
   1. <img src="Pics/transformer028.png" width=500>
   2. 从 Decoder 接收 abstract representation，通过 Linear & Softmax(Normalize，可解释为概率)，得到 Score Matrix

Limitation
1. Cross-Entropy 无法得到 错误程度
   1. <img src="Pics/transformer029.png" width=500>
2. Sequence Length 和 Vocab Size 限制


相关 Embedding 补充
1. 在原生 Transformer 训练流程中，词向量默认随机初始化，和模型其他部分一起端到端学习
2. 若你想在一个下游任务上使用通用语料训练好的 GloVe、word2vec、fastText 向量，也可以把 embedding 矩阵初始化为这些值，然后继续 fine-tune
3. LLM(GPT、BERT)本身就是 "预训练模型"，早期阶段也把 词向量随机初始化，经过海量语料训练后才成为 预训练词向量，下游再做微调时，这些 embedding 已经带有丰富的语义



BatchNorm & LayerNorm



