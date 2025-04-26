
[RSL_RL - Github](https://github.com/leggedrobotics/rsl_rl)

PyTorch 的强化学习算法实现

核心是 Proximal Policy Optimization(PPO)

结合了 Actor-Critic 架构

适用于多个环境并行训练(num_envs)的情况

并支持循环神经网络(RNN)作为策略网络





**ppo.py**

Surrogate loss 训练 Actor（策略网络） 的目标




**utils.py**




**actor_critic.py**
1. Actor 输出 action 均值
2. action 标准差 单独学习
3. Critic 输出 状态价值函数，参与 后续 GAE



**rollout_storage.py**

















