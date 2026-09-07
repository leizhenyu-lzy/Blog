# Test-Time Scaling：推理时扩展计算

**在模型回答当前任务时投入更多计算，争取提高结果质量。** 它是一种计算预算分配思路，不是一种特定网络结构。

| 方式 | 直观理解 |
| --- | --- |
| 更充分的顺序推理 | 单条求解路径多做几步计算、检查或修正。 |
| 多候选采样与选择 | 尝试多个答案，再投票、使用验证器或评分器选择。 |
| 搜索 | 探索多条中间路径，根据反馈继续或剪枝。 |
| 更多 latent 计算 | 例如增加 recurrent depth 的循环次数。 |

## 与训练的关系

- **Train-time scaling**：增加训练数据、训练计算等，改变训练得到的模型。
- **Test-time scaling**：给当前问题增加推理计算，典型设置下不更新模型权重。
- 这不代表模型无需训练：模型和验证器可能都需要训练，才能有效利用额外推理预算。

预算可以按任务难度分配。关键是“额外计算是否有用”，而不是单纯增加 token 数量；效果通常会遇到收益递减，也受延迟、成本和答案选择能力约束。

代表论文：[Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314)。

相关：[CoT](CoT.md)、[Recurrent depth](RecurrentDepth.md)。
