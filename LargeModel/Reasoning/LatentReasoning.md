# Latent Reasoning：潜在空间推理

**让中间推理通过连续隐藏表示推进，不要求每一步都转换成文字 token。**

```text
文字 CoT：问题 → 中间文字 token → 更多文字 token → 答案
Latent reasoning：问题 → 隐藏状态更新 → 隐藏状态更新 → 答案
```

普通神经网络本来就有隐藏状态；这个研究方向更强调利用隐藏状态进行额外、多步的求解计算，而不是把所有隐藏层计算都叫作 latent reasoning。

## 常见实现思路

- **连续状态反馈**：例如 Coconut，把上一阶段的隐藏状态作为后续输入的一部分，允许连续的 latent 步骤。
- **循环深度**：例如 [recurrent depth](RecurrentDepth.md)，反复执行共享模块来更新内部表示。

两者不是同一个具体架构，但都可以在不逐步生成文字的情况下推进计算，也可以和文字推理混合。

## 是否涉及训练？

通常需要配套训练。Coconut 使用分阶段训练，逐步以 latent 步骤替代显式推理步骤；recurrent-depth 模型则学习循环模块的计算。

潜在收益是减少对语言表达的依赖；实际速度、计算成本与效果取决于实现，不能直接认为“不输出文字就一定更省算力”。

代表论文：[Training Large Language Models to Reason in a Continuous Latent Space（Coconut）](https://arxiv.org/abs/2412.06769)、[Recurrent Depth / Huginn](https://arxiv.org/abs/2502.05171)。
