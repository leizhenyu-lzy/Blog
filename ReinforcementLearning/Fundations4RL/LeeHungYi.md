# 李宏毅 - Deep Reinforcement Learning - 2018

[李宏毅 - Deep Reinforcement Learning - 2018](https://www.youtube.com/playlist?list=PLJV_el3uVTsODxQFgzMzPLa16h6B8kWM_)

`Policy Gradient` -> `On-Policy/Off-Policy` -> `Add Constraint`

On-Policy : 只能用当前策略收集的数据
1. PPO(Proximal Policy Optimization)
2. A2C(Advantage Actor-Critic)

Off-Policy : 允许使用旧数据，数据效率更高
1. DQN(Deep Q-Network)
2. DDPG(Deep Deterministic Policy Gradient)
3. SAC(Soft Actor-Critic)

Add Constraint : 约束优化




---

## Table of Contents

- [李宏毅 - Deep Reinforcement Learning - 2018](#李宏毅---deep-reinforcement-learning---2018)
  - [Table of Contents](#table-of-contents)

---





# DRL Lecture 1: Policy Gradient (Review)

Basic Components
1. Actor (只能调整 Actor 的 Policy)
2. Env (Pre-Defined, Cannot Control)
3. Reward Function (Pre-Defined, Cannot Control)
4. 图示
   1. <img src="Pics/lhy001.png" width=500>
   2. Trajectory : state & action
   3. 应该用到了 Markov 假设

Policy $\pi$ is a network with parameter $\theta$
1. input : observation
2. output : action

执行完 action 会得到 reward

对于 episode : 需要 maximize total reward





从 On-Policy 到 Off-Policy












# DRL Lecture 2: Proximal Policy Optimization (PPO)

default RL algorithm at OpenAI




# DRL Lecture 3: Q-learning (Basic Idea)




# DRL Lecture 4: Q-learning (Advanced Tips)




# DRL Lecture 5: Q-learning (Continuous Action)




# DRL Lecture 6: Actor-Critic




# DRL Lecture 7: Sparse Reward




# DRL Lecture 8: Imitation Learning





















