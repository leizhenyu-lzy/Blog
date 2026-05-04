# DeepSeek

[DeepSeek - B站视频(RethinkFun)](https://space.bilibili.com/18235884/lists/4906445?type=season)

## Table of Contents

- [DeepSeek](#deepseek)
  - [Table of Contents](#table-of-contents)
- [DeepSeek-MoE](#deepseek-moe)
  - [经典 MoE](#经典-moe)
  - [DeepSeek-MoE 改进](#deepseek-moe-改进)
- [DeepSeek-V2 MLA](#deepseek-v2-mla)
- [DeepSeek-V3 多token预测 MTP](#deepseek-v3-多token预测-mtp)
- [DeepSeek-GRPO](#deepseek-grpo)


---

# DeepSeek-MoE

2024/01 提出

## 经典 MoE

**Mixture-of-Experts**
1. 将 前馈网络(FFN) 稀疏化，改造 为 Router + 多个 expert FFNs
2. 模型权重 绝大部分集中在 FFN，而非 Attention 的 QKV 等
3. <img src="Pics/moe001.png" width=400>
4. <img src="Pics/moe002.png" width=300>



Router 用于选择 expert
1. 通常只是简单的 线性层
2. 输入维度 $D_{\text{model}}$，输出维度 $N_{\text{expert}}$
3. 一般是 **Top-K Routing**，方便做 Tensor 并行和 Buffer 预分配，硬件利用率最高，对分布式集群更友好


**==P.S.==**
1. experts 的选择是 ==token-wise==，而不是 sequence-wise
2. 每个 layer 都可以选择 不同的 experts


MoE 稀疏性(Sparsity) 带来的 特点
1. 计算量(FLOPs)
   1. 总参数量 接近 Dense-Large，但 FLOPs 远小于 Dense-Large Model
   2. 训练 & 推理 都接近 Dense-Small(实际激活的专家数量) Model
2. 硬件效率(Throughput)
   1. 由于 Router & Communication(All-to-All) Overhead
   2. 利用率 不如 Dense Model
3. 收敛速度
   1. 总参数大，样本效率(Sample Efficiency) 比 Dense-Small 高，收敛到目标 Loss 所需的 Token 数更少
   2. 即使 处理每个 Token 的时间比同规模 Dense-Small 慢，但 所需步数 少，成本更低
   3. Loss 曲线 更贴近 Dense-Large，因为 取决于 总参数量(知识容量)
4. 知识解耦
   1. MoE，理论上 不同的专家 会演化出 对不同领域的能力

技术挑战
1. **负载均衡(Load Balancing)**
   1. 马太效应 : 路由模块 偏心(Bias) 使得 能力弱的专家 能力越来越差 (难被 路由模块 选中，没有被激活 因此 停止学习)，训练过程不稳定
   2. 解决方案
      1. Noisy Top-K Routing，增加探索(Exploration)
      2. 设置 Token 容量(Token Capacity)
         1. 限制每个专家 处理的 Token 数量
         2. Top-K 中 跳过超过容量的(再重新归一化)，如果都 超过就跳过，信息 由 残差链接 传到下一层
         3. 由 GShard 和 Switch Transformer(ST-MoE) 引入
      3. 引入 辅助损失(auxiliary loss)，强制路由器均匀分配任务
         1. **理想** : $Loss_\text{balance} = \sum_{i=1}^{N_{\text{expert}}} (f_i)^2$
            1. $f_i$(实际负载频率) : 一个 batch 中，真实发送给专家 $i$ 的 Token 比例
            2. 如果 某个 expert 有很高的 frequency，则 Loss 很大，最优情况 就是 freq 一样，平分负载
            3. 问题
               1. top-k 或 argmax是 **不可导(Non-differentiable)**，无法 反向传播 & 梯度下降优化
         2. **实际** : $Loss_\text{balance} = \sum_{i=1}^{N_{\text{expert}}} f_i P_i$
            1. $P_i$(路由概率均值) : 一个 batch 中，Router 对专家 $i$ 分配概率的平均值
            2. $P_i = \frac{1}{T} \sum_{j=1}^{T} \text{Softmax}(\text{Router}(x_j))_i$ (T 是 token 数量)
            3. GShard 提出的
2. 通信开销(Communication Overhead)
   1. 分布式训练中，不同的 专家通常分布在不同的 GPU 上
3. 显存占用
   1. 为了能随时调用，所有专家都必须驻留在显存中
   2. 对硬件的 内存容量 要求 依然是 **参数总量**


## DeepSeek-MoE 改进

标题中 Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models - 让专家更专精

DeepSeekMoE 架构
1. <img src="Pics/moe002.png" width=700>
2. **观点** : 传统 MoE 专家数 太少，每个 专家还不够专精
3. **改进** : **细粒度专家(Fine-grained Experts)** + **共享专家(Shared Experts)**
   1. 细粒度专家 : 总专家数 翻倍，每个专家 参数量 减半，激活的专家数 也翻倍，总参数量不变
   2. 共享专家 : 每次都被激活，负责 基础通用能力


[如何系统的入门大模型？](https://www.zhihu.com/question/621550974/answer/3472996606)

[transformer的细节到底是怎么样的？](https://www.zhihu.com/question/362131975/answer/3369782613)

[MoE(Mixture-of-Experts)大模型架构的优势是什么？为什么？](https://www.zhihu.com/question/634844209/answer/3364787819)

[Mixture-of-Experts (MoE) 经典论文一览](https://zhuanlan.zhihu.com/p/542465517)

---

# DeepSeek-V2 MLA

2024/05 提出

FFN 上，继续保留 MoE 架构

Attention 上，提出 MLA (Multi-head Latent Attention)


**Low-Rank Compression** (注 : 下面的公式 使用 ==column vector==，和平时 row vector 不同)
1. KV Joint 压缩
   1. attention input (hidden state) $\mathbf{h}_t$ 通过 **降维矩阵**(Down-Projection) 压缩成 latent vector $\mathbf{c}_t^{KV}$
      1. $\mathbf{c}_t^{KV} = W^{DKV} \mathbf{h}_t$
      2. 压缩后维度 $d_c \ll d_h*n_h$
   2. 用 2个 **升维矩阵**(Up-Projection) **分别** 解压出 Key & Value
      1. $\mathbf{k}_t^C = W^{UK} \mathbf{c}_t^{KV}$
      2. $\mathbf{v}_t^C = W^{UV} \mathbf{c}_t^{KV}$
   3. **升维矩阵 可以被 权重吸收(Weight Absorption)**
      1. 分别 融合到 权重矩阵 $W^{Q}$ & $W^{O}$ 中
      2. 有了 融合后的 矩阵的权重，不需要 显式 计算出 keys & values
   4. 推理时，只 cache latent vector $\mathbf{c}_t^{KV}$，共 $d_c * n_\text{layer}$ 个 elements
2. Q 压缩 (呼应)
   1. 训练时，减少 activation memory
      1. 其实 Q & KV-Joint 压缩 都有该优势，只是 Q 压缩 对于 inference 减少 KV Cache 没有帮助
      2. 必须 结合 **激活重计算** 才能减少，否则是僧伽
      3. 只保留 latent，反向传播 用矩阵 重新算一下
   2. 呼应 KV Joint 压缩，先 降维再升维
      1. $\mathbf{c}_t^Q = W^{DQ} \mathbf{h}_t$
      2. $\mathbf{q}_t^C = W^{UQ} \mathbf{c}_t^Q$
3. KV 的 Joint 压缩维度 $d_c$ 和 Q 的压缩维度 $d_c^\prime$ **可以不同**
   1. KV 压缩 为了减少 KV Cache，必须 极限压缩
   2. Q 压缩 可以适当放松，给 Representation 留更多空间


**Decoupled RoPE(Rotary Position Embedding)**
1. RoPE


生成并应用 RoPE 到解耦的 Query 和 Key 上：$$[\mathbf{q}_{t,1}^R; \mathbf{q}_{t,2}^R; ...; \mathbf{q}_{t,n_h}^R] = \mathbf{q}_t^R = \text{RoPE}(W^{QR} \mathbf{c}_t^Q) \quad (14)$$$$\mathbf{k}_t^R = \text{RoPE}(W^{KR} \mathbf{h}_t) \quad (15)$$将内容特征 ($C$) 与位置特征 ($R$) 进行拼接：$$\mathbf{q}_{t,i} = [\mathbf{q}_{t,i}^C; \mathbf{q}_{t,i}^R] \quad (16)$$$$\mathbf{k}_{t,i} = [\mathbf{k}_{t,i}^C; \mathbf{k}_t^R] \quad (17)$$计算最终的 Attention 分数并求和得到输出（注意分母加上了位置维度的缩放因子 $d_h^R$）：$$\mathbf{o}_{t,i} = \sum_{j=1}^t \text{Softmax}_j \left( \frac{\mathbf{q}_{t,i}^T \mathbf{k}_{j,i}}{\sqrt{d_h + d_h^R}} \right) \mathbf{v}_{j,i}^C \quad (18)$$最后通过 $W^O$ 输出矩阵得到最终结果：$$\mathbf{u}_t = W^O [\mathbf{o}_{t,1}; \mathbf{o}_{t,2}; ...; \mathbf{o}_{t,n_h}] \quad (19)$$








降维方式，不同于 AE，必须是 纯线性，不能加 非线性激活函数

MLA 流程
1. 降维压缩(Down-Projection)
2. 存入缓存(KV Cache)
3. 升维解压(Up-Projection)

**权重吸收 (Weight Absorption)**

$K$ 是由压缩包 $c_t$ 乘以解压矩阵 $W_{UK}$ 得到的，即 $K = c_t \times W_{UK}$

$$\text{分数} = Q \times (c_t \times W_{UK})^T = Q \times W_{UK}^T \times c_t^T$$

矩阵乘法满足结合律，让 $(Q \times W_{UK}^T)$ 先算

$Q$ 是当前正在生成的 Token，无需 Cache

$W_{UK}^T$ 是一个静态的模型权重(训练完成后就固定)

旋转位置编码(RoPE) 无法压缩 : 位置信息很敏感，







---

# DeepSeek-V3 多token预测 MTP

2025/02 提出



提升推理效率 (工程层面)
1. 通信 & 计算 并行 (DBO, dual batch overlap)
   1. 把一个 Batch 拆成两个小 Batch
   2. 第一个 Batch 做 通信(All-to-All) 时，第二个 Batch 做 计算(Attention/FFN)
2. 大规模专家并行 (WideEP, wide-expert parallel)
   1. 当专家数量非常多且分布在很多卡上时，传统的专家并行(EP)导致单次通信的数据包太小，无法填满网络带宽
   2. 针对大规模集群重新设计的并行策略
   3. 优化 跨节点专家 排布方案，减少了跨节点(Inter-node)的通信量，优先在 NVLink 覆盖的机柜内完成数据交换


# DeepSeek-GRPO




