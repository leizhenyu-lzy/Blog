# RSI : Recursive Self-Improvement

**系统改进自身，保留有效改进，再让改进后的系统参与下一轮自我改进**

```text
系统 A → 提出改进 → 实现与评估 → 采用有效改进得到 A'
                                  ↓
                            A' 继续参与改进，得到 A''
```

修改内容
1. 模型层 : 训练数据、参数、训练算法或架构
2. Agent 层 : 自身代码、工具、策略和工作流程
3. 改进过程本身 : 实验设计、评估或寻找改进的方法


## 不要把所有循环都叫 RSI

| 情况 | 如何理解 |
| --- | --- |
| 修改当前答案、修当前项目的 bug | 任务内迭代，不足以说明系统自身得到改进。 |
| recurrent depth 多算几轮 | 固定参数下更新隐藏状态，不是系统自我改造。 |
| 把经验写入 memory | 可能是自适应的一部分；单独存记忆不足以证明 RSI。 |
| 改进自身 Agent，经评估后用新版继续改进自身 | 更符合 RSI 的反馈循环。 |

提出修改不等于已经提升；需要验证改进是否有效。递归循环也不保证持续变强或无限加速。

参考：[From Seed AI to Technological Singularity via Recursively Self-Improving Software](https://arxiv.org/abs/1502.06512)。相关概念见 [Reasoning 索引](../Reasoning/reasoning.md)。
