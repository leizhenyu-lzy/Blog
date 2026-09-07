# CoT：Chain of Thought，思维链

**在最终答案之前，生成一系列中间求解步骤。** 中间步骤通常以文字 token 表示，供后续生成继续使用。

```text
问题 → 拆解条件 → 中间计算 / 推导 → 答案
```

## 训练与推理

- **CoT prompting**：在提示中提供带求解步骤的示例，或要求逐步求解；不必为当前任务更新权重。
- **能力训练**：也可以通过包含推理过程的数据、监督微调或强化学习等方法提升多步求解能力；CoT 这个词本身不指定训练算法。
- **推理阶段**：生成中间 token 需要计算；延长有效求解过程可以是一种 test-time scaling，但文字越长不一定越正确。

## 和其他概念的区别

- few-shot CoT 同时使用 [ICL](InContextLearning.md)：模型从上下文示例中获得解题模式。
- CoT 用离散文字表达中间步骤；[latent reasoning](LatentReasoning.md) 可以直接在连续隐藏表示中继续计算。
- 用户看不到的文字思维链，仍然可能是 token 序列；“不展示”不等于“连续 latent reasoning”。

代表论文：[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)。
