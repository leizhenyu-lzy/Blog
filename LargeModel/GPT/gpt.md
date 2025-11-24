# GPT (Generative Pre-Training)


[大模型修炼之道(二): GPT系列GPT1，GPT2，GPT3，GPT4 - B站视频(RethinkFun)](https://www.bilibili.com/video/BV1ZJ4m1K73s)

**==GPT-1==** : Improving Language Understanding by Generative Pre-Training
1. ==Decoder-Only==，目标是学习 好的语言模型，关注如何将句子 从左到右 流畅地生成
2. 动机
   1. NLP 每个任务都 需要大量标注数据，模型 不能 复用(运用到其他任务)
   2. CV 领域得益于 ImageNet 数据集，可以 预训练 模型，下游 子任务 微调
   3. OpenAI 要做 NLP 领域的 预训练模型
3. 难点
   1. 没有像 ImageNet 那样大量的标注数据
      1. 解决 没有标注数据 问题 -> 使用 语言模型 自回归方式 训练模型 (给文本，预测下一个词)
   2. 模型架构如何设计，方便轻微修改，来应用到下游任务
      1. 架构选择 -> RNN / Transformer (相比 RNN 更好 记住 训练数据中的 模式)
4. 模型结构
   1. <img src="Pics/gpt001.png" width=400>
   2. 无需 Cross-Attention (没有 Encoder)
   3. **可学习的** ==Position & Token Embedding==
   4. 2 Outputs
      1. Text Prediction : 自回归任务
      2. Task Classifier : 下游微调任务，预训练不使用
5. **预训练**
   1. 语言模型似然函数
      1. $$L_1(u) = \sum_{i} \log P(u_i|u_{i-k}, \dots, u_{i-1}; \Theta)$$
      2. 使用 前面连续 k个 tokens 预测下一个 token
      3. 文本整体概率 : 所有 tokens 概率乘积 等价于 概率$\log$求和
      4. 优化 参数 $\theta$ 最大化 似然函数
   2. 得到下一个词的概率
      1. $$h_0 = U W_e + W_p$$
         1. $h_0$ (Hidden State 0)
         2. $U$ (Input Tokens) : 模型的输入序列(要预测下一个词的上下文)
         3. $W_e$ (Token Embedding Matrix) : 词嵌入矩阵，将输入的词元 $U$ 转换为其向量表示
            1. rows = vocab_size
            2. cols = $d_{model}$，feature size，GPT-1 是 768
         4. $U W_e$ 得到的是词元向量表示，通过 **Lookup** 的方式来完成，并不是矩阵乘法
         5. $W_p$ (Position Embedding Matrix)
      2. $$h_l = \text{decoder\_block}(h_{l-1}) \quad \forall l \in [1, n]$$
         1. $h_l$ (Hidden State $l$)
         2. $\text{decoder\_block}(\cdot)$ : 解码器块，GPT-1 模型中的一个 Transformer 解码器层
         3. $n$个 解码器层，GPT-1 中 $n=12$
      3. $$P(u) = \text{softmax}(h_n W_e^T)$$
         1. $P(u)$ : 最终计算出的下一个词元 $u$ 在整个词汇表上的概率分布
         2. $h_n$ (Final Hidden State)
         3. $W_e^T$ : 词嵌入矩阵 $W_e$ 的转置，**==共享权重==**
            1. input 处的 词元嵌入矩阵 $W_e$ & output 处的 线性层权重矩阵 $W_e^T$ 之间 **共享权重**
            2. 大幅减少模型参数 (后续 模型变大 Embedding 矩阵 参数占比小，也会独立训练 输出侧 权重矩阵)
            3. 更好的泛化能力，两个任务相互约束和辅助
            4. 平衡输入和输出，确保了输入和输出表示空间的一致性
         4. $\text{softmax}(\cdot)$ : 将最终的线性输出(logits) 转换为 概率分布
6. **微调**
   1. <img src="Pics/gpt002.png" width=800>
   2. OpenAI 给文本 加入 特殊 token，让模型知道 任务 不是 预测 下一 token
      1. `<Delim>`(分割), `<Start>`, `<Extract>`
   3. 绿色 Transformer 块，就是 pre-trained GPT-1
   4. **Tasks**
      1. Classification (分类) : 预测文本的类别
      2. Entailment (推理) : 预测 假设 是否 被 前提 蕴含
      3. Similarity (相似度) : 预测两个文本的 相似度得分，对称的(A $\sim$ B, B $\sim$ A)
      4. Multiple Choice (多选题) : 从 N 个选项中选择最正确的答案，最后接 softmax
   5. 兼顾 语言模型自回归 & 下游任务，给2个 任务的 Loss 分配不同权重
   6. GPT-1 的微调是 **全参数微调**
7. 训练数据
   1. BooksCorpus Dataset，7000本 未发表的书，800M Words
   2. Context Window : 512
   3. Batch Size : 32


GPT-1 类似 作家，BERT 类似 读者

<img src="Pics/gpt003.png" width=500>


**==BERT==** : Pre-training of Deep Bidirectional Transformers for Language Understanding
1. ==Encoder-Only==，目标是学习 好的上下文表示，通过 预测 被掩盖的词 & 句子关系 增强语义理解能力
2. 可以在一个序列中同时看到当前词之前和之后的所有信息，通过 MLM(Masked Language Modeling，随机掩盖一些词) & 标准的自注意力机制 实现





**==GPT-2==** : Language Models are Unsupervised Multitask Learners

**==GPT-3==** : Language Models are Few-Shot Learners

**==GPT-4==** : Technical Report


