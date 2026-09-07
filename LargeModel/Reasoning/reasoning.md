# Reasoning：推理与上下文适应

这里按研究主题归类，**不代表这些方法只涉及推理、不涉及训练**。Reasoning（推理能力）也不同于 inference（模型运行、生成输出的阶段）。

## 概念地图

| 概念 | 关注什么 | 训练与推理的关系 |
| --- | --- | --- |
| [CoT](CoT.md) | 用中间文字步骤推进求解 | 可以用提示词引导，也可以通过训练学习；生成步骤发生在推理阶段。 |
| [Latent reasoning](LatentReasoning.md) | 用连续隐藏表示推进中间推理 | 通常需要配套训练方法或架构。 |
| [Recurrent depth](RecurrentDepth.md) | 共享计算模块在深度方向重复执行 | 训练时学习迭代计算；推理时可以调整循环次数。 |
| [Test-time scaling](TestTimeScaling.md) | 给当前任务更多推理计算预算 | 是计算资源分配思路，不限定模型如何训练。 |
| [In-context learning（ICL）](InContextLearning.md) | 从当前上下文中的示例等信息适应任务 | 标准 ICL 不在当前任务上更新模型权重；这种能力来自此前训练。 |
| [Recursive self-improvement（RSI）](../Agent/RSI.md) | 改进系统自身，并让新版继续参与改进 | 可涉及训练，也可改进 Agent 代码与流程；属于更广的系统层概念。 |

这些不是互斥分类：few-shot CoT 可以使用 ICL；增加 CoT 步骤或 recurrent depth 可以实现 test-time scaling；recurrent depth 是实现 latent reasoning 的一种方式。

ICL 不等于 reasoning：学习输出格式也属于上下文适应，不一定需要复杂推理。为方便比较，暂放在本目录；如果以后建立 Learning / Adaptation 专题，可以迁移并保留链接。

## 三种变化不要混淆

- **训练**：通常通过优化更新参数，使能力可以跨任务保留。
- **推理 / ICL**：通常固定参数，改变当前隐藏状态、上下文或计算量。
- **RSI**：系统的改进被保留，并反馈到下一轮自我改进中；不是单次回答多想几步。

各概念的代表论文见对应笔记。
