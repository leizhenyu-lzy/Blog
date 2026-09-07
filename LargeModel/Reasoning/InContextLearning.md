# In-Context Learning（ICL）：上下文学习

**模型从当前输入中的示例等信息适应任务，而不为该任务更新权重。** 最典型的是 few-shot：给几组输入输出示例，再让模型处理新输入。

```text
苹果 → 水果
胡萝卜 → 蔬菜
香蕉 → ?
```

模型根据上下文推断任务和输出模式。这里只是一个直观示例，不代表模型原本不知道这些类别。

## 为什么叫 learning，却不反向传播？

“学习”指行为随上下文发生适应，不一定指梯度更新。

$$\text{ICL：}y\sim p_\theta(y\mid\text{示例},x),\quad\theta\text{ 固定}$$

$$\text{Fine-tuning：}\theta\rightarrow\theta',\quad y\sim p_{\theta'}(y\mid x)$$

ICL 依赖此前训练得到的能力；示例改变本次计算中的状态，而不是标准意义上的模型参数。移除示例后，不能假设这种适应已永久写入模型。

## 算什么？

更适合归为 **推理阶段的任务适应 / 学习现象**，不是一种特定推理算法，也不是 RSI。

| 相邻概念 | 与 ICL 的关系 |
| --- | --- |
| Prompting | 提示设计的范围更广；few-shot 示例是引导 ICL 的常见方式。 |
| CoT | 关注中间求解步骤；few-shot CoT 同时用到 ICL。 |
| RAG | 关注从哪里检索上下文；检索资料可辅助回答，但不是所有 RAG 都是从示例学习任务。 |
| Fine-tuning | 会更新参数；标准 ICL 不更新。 |
| Memory | 关注信息如何跨会话存取；保存示例不等于把它训练进权重。 |

为了和 CoT、推理时适应对照，暂放在 Reasoning 目录；**ICL 不必涉及复杂 reasoning**，例如模仿标签格式也可以发生上下文适应。

代表论文：[Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165)。
