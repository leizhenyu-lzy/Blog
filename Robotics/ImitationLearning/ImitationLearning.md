# Imitation Learning

## Table of Contents

- [Imitation Learning](#imitation-learning)
  - [Table of Contents](#table-of-contents)
- [Online / Offline](#online--offline)
- [Introduction to Imitation Learning](#introduction-to-imitation-learning)
  - [01 - What is Imitation Learning](#01---what-is-imitation-learning)
  - [02 - Behavioral Cloning](#02---behavioral-cloning)
  - [03 - Adversarial Imitation Leaning](#03---adversarial-imitation-leaning)
  - [04 - Semi-Supervised Imitation Learning](#04---semi-supervised-imitation-learning)

---

# Online / Offline

离线学习 Offline-Learning (批处理学习 Batch-Learning)
1. **数据特点** : 所有训练数据 在模型开始训练前 就已经被收集好，并以一个固定的数据集(batch)的形式提供
2. **训练过程** : 模型在整个数据集上进行一次或多次完整的训练，直到收敛，训练完成，模型就被部署并用于推理，模型不会再从新的数据中学习
3. 优点 : 训练过程稳定可控，可以利用高性能计算设备进行大规模并行训练，易于复现和评估
4. 缺点 : 模型无法实时适应新的数据分布，如果数据分布随时间变化(eg : 市场趋势、用户行为)，模型性能会下降

在线学习 Online-Learning (迭代式 & 增量式 的学习模式)
1. **数据特点** : 数据是 流式地、连续地 到达，模型在接收到每个或每批新的数据点后立即进行更新
2. **训练过程** : 模型在每个时间步(time step)，接收新的数据点，基于这些数据更新自身的参数，过程是持续的
3. 优点 : 能够实时适应数据分布的变化，节省内存(不需要一次性加载所有数据)，适用于数据量巨大且无法一次性存储的场景
4. 缺点 : 训练过程 可能不稳定，容易受 异常数据点影响

eg :
1. VLA : 大规模的离线模仿学习
2. DAgger : 在线模仿学习

---

# Introduction to Imitation Learning

## 01 - What is Imitation Learning

[](https://www.bilibili.com/video/BV1RU4y167oA)

learning from expert's behavior **demonstration**

**Framework of Imitation Learning**
1. Markov Decision Processes (MDPs) : $\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{r}, \mathcal{\rho}, \mathcal{H})$
2. (finite) state space, action space




## 02 - Behavioral Cloning

## 03 - Adversarial Imitation Leaning

## 04 - Semi-Supervised Imitation Learning







