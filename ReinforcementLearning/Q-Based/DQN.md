# DQN (Deep Q-Network)

由 DeepMind 在 2015 年提出，用于在 Atari(雅达利) 游戏环境中训练 AI 代理

Value-Based

在 Q-Learning 上的改进
1. 神经网络 Q网络 代替 Q表
2. Experience Replay : Off-Policy，从经验库中学习
3. Fixed Q-Targets

Q-Learning 的问题
1. 状态空间过大，无法用 Q 表存储
2. Q 值更新不稳定


DQN 结构
1. 输入 : 状态 s
2. **输出 : 每个动作 a 的 Q 值**
3. 采用 CNN 处理图像输入（如 Atari 游戏）

DQN 的 更新 公式 和 Q-Learning 一致

<img src="Pics/dqn001.png" width=600>

DQN 采用 两套 Q网络，解决 训练不稳定
1. 主 Q网络(Online Q-Network) : 用于选择动作并学习 (Q估计)
   1. 主 Q网络 负责训练，每次更新时，它不会影响 目标 Q网络
2. 目标 Q网络(Target Q-Network) : 用于计算 固定 Q 目标 (Q显示)
   1. 它的参数 固定一段时间(隔一定步数同步 主Q网络) 再更新



