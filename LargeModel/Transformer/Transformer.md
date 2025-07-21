[Transformers, Simply Explained | Deep Learning -  - YouTube(DeepBean)](https://www.youtube.com/watch?v=UPhaYex4zZk)

[李沐](https://www.bilibili.com/video/BV1pu411o7BE)

[王树森](https://www.bilibili.com/video/BV1dK411k74q)

[妹子](https://www.bilibili.com/video/BV1xoJwzDESD)


解决 旧架构(eg : RNN) 中的问题
1. Long-Range : information 难以保持 很多步 timestamps
2. Parallel   : 需要类似自回归方式，难以并行(train & inference)

Basic Idea : **Self-Attention**
1. 序列中的 每一个单词 都根据一定的 注意力分数 和 另一序列的单词 相连
2. 自注意力机制，两个序列相同
3. <img src="Pics/transformer003.png" width=500>



Operation
1. <img src="Pics/transformer001.png" width=700>
2. input  ： 包含 开始token(`<START>`) & 结束token(`<END>`)
3. output :
4. 模型被分为两个部分
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
         2. embeding vector 的实际数据是 训练中学习的，不需要 pre-trained embedding
      5. 特殊 Tokens : `<START>`, `<END>`, `<UNK>`(unknown), `<PAD>`(保证相同序列长度)
3. Positional Encoding
   1. 对于 RNN，位置信息 隐式提供，token 按顺序输入模型，但是 **transformer 的 token 是 并行输入**
   2. <img src="Pics/transformer006.png" width=400>
   3. `pos` : token 在序列中的位置 (Position index)
   4. `i`   : 向量维度索引 (Dimension index)
   5. 位置编码和原始编码 长度一致，直接相加
   6. 生成 位置编码的函数 可以学习，论文中使用硬编码
   7. <img src="Pics/transformer007.png" width=400>
   8. <img src="Pics/transformer008.png" width=500>
   9. <img src="Pics/transformer009.png" width=500>
4. Encoder
5. Decoder
6. Word Selector



在原生 Transformer 训练流程中，词向量默认和模型其他部分一起端到端学习

若你想在一个下游任务上使用通用语料训练好的 GloVe、word2vec、fastText 向量，也可以把 embedding 矩阵初始化为这些值，然后继续 fine-tune

位置编码不是词向量，但和词向量同维度，相加后作为模型的实际输入

LLM(GPT、BERT)本身就是“预训练模型”，早期阶段也把词向量随机初始化，经过海量语料训练后才成为“预训练词向量”。下游再做微调时，这些 embedding 已经带有丰富的语义

