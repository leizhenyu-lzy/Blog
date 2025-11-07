# 莫烦Python - 强化学习

[莫烦Python - 强化学习](https://www.bilibili.com/video/BV13W411Y75P)

[强化学习科普 - 莫烦Python](https://space.bilibili.com/243821484/lists/1607999?type=series)

## Table of Contents

- [莫烦Python - 强化学习](#莫烦python---强化学习)
  - [Table of Contents](#table-of-contents)
- [简介 \& 概念](#简介--概念)
  - [Monte-Carlo Tree Search (MCTS)](#monte-carlo-tree-search-mcts)
  - [Overfitting](#overfitting)
- [分类](#分类)
  - [是否是 Model-Based](#是否是-model-based)
  - [概率/价值](#概率价值)
  - [更新方式](#更新方式)
  - [在线/离线](#在线离线)
- [DDPG (Deep Deterministic Policy Gradient)](#ddpg-deep-deterministic-policy-gradient)
- [A3C (Asynchronous Advantage Actor-Critic)](#a3c-asynchronous-advantage-actor-critic)
- [经验回放](#经验回放)

---

# 简介 & 概念

分类
1. <img src="Pics/mofan001.png" width=800>

分数导向性




通过价值选择行为
1. Q-Learning(表格)
2. Sarsa(表格)
3. Deep Q Network(网络)

直接选择行为
1. Policy Gradient

想象环境并从中学习
1. Model-Based RL


rollout(展开/模拟)
1. 指 从当前状态开始，按照策略(policy)执行动作，并观察环境反馈(reward)，直到达到终止条件
2. 收集数据、评估策略、估算未来回报



## Monte-Carlo Tree Search (MCTS)

Monte-Carlo Tree Search (MCTS)
1. 用于决策过程的搜索算法，能够在有限计算资源下高效搜索最优决策
2. 基本目标是构建一个**搜索树**，并通过 模拟(rollout) 来评估不同决策的质量，从而选择最优动作
3. **四个步骤**
   1. 选择 (Expansion/Tree Traversal)
      1. 从根节点 Root 开始，连续向下选择子节点至叶子节点 L，使用一种选择子节点的方法，让游戏树向最优的方向扩展
   2. 扩展 (Node Expansion)
      1. 除非任意一方的输赢使得游戏在 L 结束，否则创建一个或多个子节点并选取其中一个节点 C
   3. 模拟 (Rollout/Random Simulation)
      1. 如果 该节点没有被 访问过，则 rollout，否则 创建一个新 节点，并 rollout
      2. 再从节点C开始，用随机策略进行游戏
      3. 除非 到了 terminal state，否则 选择 random available actions，并 simulate
   4. 反向传播 (BackPropagation)
      1. 使用随机游戏的结果，更新从 C 到 Root 的路径上的节点信息
4. 根据 **大数定理**，当采样数量足够大，采样样本 可以无限近似表示 原分布
5. 随机采样作为近似估计，大量自博弈，寻找最有可能走的节点，记录自博弈结果，并更新相关数据
6. **UCB/UCT**(Upper Confidence Bound for Trees)
   1. UCT 是 MCTS 里应用 UCB 的方法，专门用于决策树搜索
   2. **$$UCB(s, a) = \frac{Q(s, a)}{N(s, a)} + c \sqrt{\frac{\ln N(s)}{N(s, a)}}$$**
   3. 其中
      1. **$Q(s, a)$**：动作 $a$ 在状态 $s$ 下的 **累积奖励总和**
      2. **$N(s, a)$**：动作 $a$ 在状态 $s$ 下的 **访问次数**
         1. 显然 对于 没有访问过的($N(s, a)$ = 0)，UCB score 是无穷大
      3. **$N(s)$**：状态 $s$ 的 **总访问次数** (所有子节点访问次数的总和 / 父节点的访问次数)
      4. **$c$**：探索因子(通常设为 **$\sqrt{2}$**)，用于控制 **探索(Exploration)** 的程度
   4. 第一项 : (偏向于选择当前表现最好的动作)，可以理解为胜率
   5. 第二项 : (偏向于选择访问次数较少的动作)，可以理解为一个随次数衰减的函数，因此更倾向于选择没怎么被统计过的节点，避免**胜率高&置信度低**的问题
7. 每次选择 UCT 值最高的节点进行 自博弈，访问次数最高的节点就是最佳节点
8. Reference
   1. [蒙特卡洛方法 - B站视频](https://www.bilibili.com/video/BV1hV4y1Q7TR)
   2. [Monte Carlo tree search - Wiki](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
   3. [Monte Carlo Tree Search - YouTube](https://www.youtube.com/watch?v=UXW2yZndl7U) - Good
   4. [](https://www.bilibili.com/video/BV1s5411D7JT) - TODO
9. Images
   1. <img src="Pics/mofan002.png" width=500>
   2. 判断是否为 leaf & 判断是否初次访问
   3. <img src="Pics/mofan003.png" width=1000>
   4. ~~ 表示 rollout

## Overfitting

强化学习 同样会遇到 **过拟合 Overfitting** 问题
1. 训练过程中过度适应特定环境或特定任务，导致泛化能力下降
2. 过度拟合某些固定状态，而忽略更广泛的探索(过度依赖历史经验/依靠某些特定动作模式)
3. 解决方案
   1. Domain Randomization
      1. 随机改变地面摩擦力、坡度、障碍物
      2. 随机 push
   2. Data Augmentation
      1. 加入 噪声 & 观测误差
   3. Exploration
      1. 增加 Entropy Bonus
      2. 随机初始化
   4. 正则化 Regularization
      1. 权重衰减
      2. Dropout(RL 中较少使用)
      3. Batch Normalization/Layer Normalization
   5. Early Stop
   6. Transfer Learning










# 分类

## 是否是 Model-Based

用模型(Model)表示环境

不理解环境 (Model-Free RL)
1. 只能一步步等待真实世界的反馈
2. 不需要知道 环境的 状态转移概率
3. 算法
   1. Q-Learning
   2. Sarsa
   3. Policy Gradients

理解环境 (Model-Based RL)
1. 建立模型，模拟环境的反馈 (虚拟环境)
2. 可以预判环境的反馈，选择最好的


## 概率/价值

基于概率 (Policy-Based RL)
1. 最直接，通过分析环境，直接输出各个行动概率，根据概率采取行动，每种行动都有可能被选中
2. 对于连续的可以使用一个概率分布
3. 算法
   1. **Policy Gradient**
   2. PPO

基于价值 (Value-Based RL)
1. 输出所有动作的价值，选择最高价值的动作
2. 无法处理连续的动作
2. 算法
   1. Q-Learning
   2. Sarsa

结合两种优势，建立 Actor-Critic
1. Actor  : 基于概率做动作
2. Critic : 对于动作给出价值


## 更新方式

回合更新(Monte-Carlo Update)(Episodic Update)
1. 需要等待整体结束
2. 算法
   1. 基础版 Policy Gradient
   2. Monte-Carlo Learning

单步更新(Temporal-Difference Update)(Truncated Mini-Batch Updates)
1. 每一步都更新，更有效率
2. 算法
   1. Q-Learning
   2. Sarsa
   3. 升级版 Policy Gradient


## 在线/离线

<img src="Pics/mofan019.png" width =700>

在线学习(On-Policy)
1. 必须本人在场，学习
2. 算法
   1. Sarsa
   2. Sarsa(lambda)
   3. A2C
   4. PPO(Proximal Policy Optimization)

离线学习(Off-Policy)
1. 可以观察别人的经历，可以 experience replay
2. 算法
   1. Q-Learning
   2. Deep Q Network
   3. DDPG
   4. SAC


---






---








---

[PG & PPO - 个人笔记](./PPO.md)




---




# DDPG (Deep Deterministic Policy Gradient)

DDPG 由 DeepMind 在 2016 年提出

是 Actor-Critic 结构的一个变种，结合了 DQN 和 DPG（Deterministic Policy Gradient）




# A3C (Asynchronous Advantage Actor-Critic)

DeepMind 在 2016 年提出

异步 的 Actor-Critic 算法


核心思想
1. Actor-Critic 结构
   1. Actor  负责生成策略
   2. Critic 估计值函数
2. Advantage 函数
3. 异步更新
   1. 多个 Worker 线程在不同环境中收集数据，并异步更新全局网络






# 经验回放

经验回放 (Experience Replay)
1. 存储过去的经验，并在训练时随机采样
2. 训练数据可能由 不同时间步、不同策略 采样得到，数据是 非序列化的
3. **不适用于** on-policy(在线策略)，**适用于** off-policy(离线策略)
4. **核心思想** : 将智能体的交互经验存储在一个缓冲区(Replay Buffer)，并在训练时随机抽取一批样本进行学习



Replay Buffer 不等于 Rollout Storage

Rollout Storage
1. 每轮收集、每轮丢弃
2. 收集完后计算 GAE(Generalized Advantage Estimation)、优势函数
3. 存储 trajectory（step-by-step）数据
4. PPO 会重复训练多个 epoch，所以需要 mini_batch_generator

Replay Buffer
1. 数据长期保留，反复采样
2. 从 buffer 中采样 minibatch
3. 存储 单步 transition 或者 episode

