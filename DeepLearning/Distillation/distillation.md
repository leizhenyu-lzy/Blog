# Distillation

## Table of Contents

- [Distillation](#distillation)
  - [Table of Contents](#table-of-contents)
- [Distilling the Knowledge in a Neural Network - Hinton](#distilling-the-knowledge-in-a-neural-network---hinton)
- [大模型语境](#大模型语境)

---


# Distilling the Knowledge in a Neural Network - Hinton

知识蒸馏


# 大模型语境

大模型语境下，开源 指 开放模型权重

一个模型的 训练数据 使用了 另一个模型的输出数据

常见形式：
1. teacher 给 prompt 生成 response，student 用这些数据继续训练
2. teacher 给 soft label / logits，student 拟合输出分布
3. teacher 生成 CoT / 推理轨迹，student 学习中间推理过程
4. teacher 作为偏好来源，构造 SFT / DPO / RLHF 数据

目的：
1. 用自家大模型 蒸馏出 不同尺寸的小模型，以满足不同延迟 / 成本 / 部署需求
2. 用一个模型 蒸馏出 不同架构的其他模型，尝试迁移推理能力
3. 把 闭源大模型的能力，迁移到 可私有部署的 开源模型 上
4. 提升 小模型 在特定任务上的表现，而不必从头训练大模型

常见说法：
1. data distillation : teacher 产出训练样本
2. response distillation : student 学 最终回答
3. reasoning distillation : student 学 推理链 / 中间步骤
4. self-distillation : 同一家族大模型蒸馏出更小版本，或模型蒸馏自己生成的数据

注意
1. 蒸馏 不等于简单抄答案，核心是把 teacher 的能力 压缩到 student
2. 如果 student 只学最终答案，可能学到 结果，但未必学到 推理过程
3. 蒸馏效果 受 teacher 质量、数据覆盖度、数据清洗质量 影响很大
4. 蒸馏后的模型 往往更便宜、更快，但能力上限通常仍低于 teacher


