# KV Cache (键值缓存)

## Table of Contents
- [KV Cache (键值缓存)](#kv-cache-键值缓存)
  - [Table of Contents](#table-of-contents)
- [基础原理](#基础原理)
- [Flash Attention](#flash-attention)
- [Residual Attention](#residual-attention)

---

# 基础原理

针对 自回归生成(next token prediction)，对于 BERT 双向注意力 意义不大

只在 Inference 阶段 使用，Training 阶段 有全局视野 但使用 Causal Mask 限制 当前 token 只能看到前面的 token

KV Cache 针对 Decoder 侧
1. Cross-Attention 处 : Encoder 得到的 K 和 V 是固定不变的，直接缓存起来
2. Masked Self-Attention 处 : Decoder 每生成一个新词，K 和 V 会被加入到缓存池里，不断变长

核心公式
1. $\text{Attention}(Q, K, V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V$

整体推理流程
1. Q K^T 再 softmax 得到 注意力权重矩阵
2. 注意力权重矩阵 和 V 矩阵相乘得到 输出 logits
3. logits 通过 Linear & Softmax 得到 next token 的概率分布

反向思考
1. 要得到 最后一行的 logits，只需要 **注意力分数矩阵 最后一行** 的 结果，对 **V 的所有行** 进行加权求和
2. 要得到 **注意力分数矩阵 最后一行** 的 结果，只需要 **Q 的最后一行** 和 **K^T 的 所有列** 相乘

简化后(空间换时间)
1. 只需要 最新的 Q & 所有的 K & V，而 旧的 K V 已经在上一轮 计算过，可以直接复用
2. 后续 只需要 计算 最新的 Q K V，把 新的 K V 和 旧的 K V 拼接起来，得到 完整的 K V

**注意点**
1. 位置编码 : 通过 KV Cache 缓存的 token 数量，得到正确的 位置编码
2. ==每层 attention layer 都有自己独立的 KV Cache==

KV Cache 大小的计算 : 2(K & V) * layer * batch_size * seq_len * head_num * head_dim * element_bytes
1. 层数 : decoder blocks
2. 批量大小 : 普通个人电脑上 batchsize = 1
3. 序列长度 : Prompt 长度 + 已经生成的 token 数量，不断变长
   1. 由于无法预估 生成文本的长度，所以 序列长度 不能提前确定，需要动态计算
   2. 按照 max_length 会造成 显存浪费
   3. **PagedAttention** : 把 KV Cache 切成一个个固定大小的 Block
4. 元素字节数 : float32 是 4 字节，通过 量化 可以减少 显存占用(INT4 / FP8)


K Cache & V Cache 是**分开存放**的 (K 需要转置 而 V 不需要)

==KV Cache 必须为模型的 每个Layer 分别存储一份 独立的缓存==

显存带宽问题 : KV Cache 存放在 GPU 显存中，计算时 需要 移动至 计算单元(CUDA kernel)，KV Cache 越大，移动数据的时间成本 越高



# Flash Attention

# Residual Attention

