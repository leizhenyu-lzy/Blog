# Recurrent Depth：循环深度

**同一个共享参数的模块，在深度方向反复处理隐藏表示。** 可以理解为反复经过同一组计算层，逐步更新内部状态。

```text
普通堆叠：输入 → 不同参数的层 1 → 层 2 → 层 3 → 输出
循环深度：输入 → 编码 → 共享模块循环 R 次 → 解码输出
```

简化表达：

$$h_{r+1}=F_\theta(h_r,x)$$

这里循环的是深度方向的计算，不是传统 RNN 沿序列时间步的循环。它也不是 Agent 在外部反复调用一个普通模型。

## 是否涉及训练？

**涉及。** 以 Huginn 为例，模型需要用这种循环架构训练，学会让共享模块不断更新有用的隐藏状态。论文说“不需要专门的推理训练数据”，不等于“不需要训练”。

- 训练阶段：学习参数 $\theta$，使循环计算有效。
- 推理阶段：通常固定 $\theta$，调整循环次数 $R$；变化的是隐藏状态和计算量。
- 不能假设把普通 Transformer 的某一层临时多跑几次，就能得到同样效果。

## 与其他概念的关系

它是实现 [latent reasoning](LatentReasoning.md) 的一种架构方法；增加循环次数是一种 [test-time scaling](TestTimeScaling.md)。有效计算深度增加，但独立参数量不随循环次数增加。

更多循环通常增加延迟，也不保证效果持续提升。它没有在每次推理中改写自己，因此不等于 [RSI](../Agent/RSI.md)。

代表工作：[Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach（Huginn）](https://arxiv.org/abs/2502.05171)。
