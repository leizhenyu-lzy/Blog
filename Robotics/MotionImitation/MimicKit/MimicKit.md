# MimicKit: A Reinforcement Learning Framework for Motion Imitation and Control

[MimicKit - Github](https://github.com/xbpeng/MimicKit)

a suite of **motion imitation methods** for training **motion controllers**


Motion Imitation
1. **`DeepMimic`**
   1. tracking-based method
   2. precise replication of target reference motions
   3. **limitation** : inflexible, hard to perform new tasks
2. **`AMP`** (Adversarial Motion Priors)
   1. adversarial distribution-matching method
   2. imitate overall behavioral distribution(style) of dataset of motion clips
   3. no explicit tracking
   4. more versatility than DeepMimic
   5. **limitation** : more prone to converge to local optima (challenging/high-dynamic motions) than tracking-based method
3. **`ASE`** (Adversarial Skill Embeddings)
   1. train reusable generative controllers
   2. combine
      1. adversial imitation learning
      2. mutual infomation-base skill discovery objective
   3. learn latent skill embeddings, select skills from learned latent space
   4. ASE controller : latent space points -> diverse behaviors
   5. train task-specific higher-level controller to select skills from learned latent space
4. **`ADD`** (Adversarial Differential Discriminator)
   1. differential discriminator learn adaptive motion tracking objectives
   2. mitigate manual design & tune tracking reward functions for different characters/motions


RL
1. **`PPO`** (Proximal Policy Optimization)
   1. **on-policy**, sample inefficient
2. **`AWR`** (Advantage-Weighted Regression)
   1. **off-policy**

Tool
1. GMR


---

# Agent

# Model

# Environment

done flag (episode/env status)
1. `NULL` : not terminated
2. `FAIL` : terminate due to failure
3. `SUCC` : terminate due to complete task
4. `TIME` : terminate due to time limit


# Engine

control mode (depend on simulator)

IsaacGym
1. `none`
2. `pos` : PD controller 的 target rotations (1D-revolute / 3D-spherical)
3. `vel` : joint 的 target velocity
4. `torque` ： joint
5. `pd_1d` : best for robot only contains 1D revolute joints

---

#


