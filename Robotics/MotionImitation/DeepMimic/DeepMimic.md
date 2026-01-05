# DeepMimic : Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills

ACM SIGGRAPH 2018

[DeepMimic - Project Website](https://xbpeng.github.io/projects/DeepMimic/index.html)

---

# 00 - Abstract

character animation goal
1. combine
   1. `data-driven specification of behavior`(数据驱动的行为定义)
   2. `execute similar behavior in physical simulation`(物理仿真中的行为执行)
2. enable realistic response to perturbations & environmental variation

handle : key-framed motions & highly-dynamic actions(MoCap) & retargeted motions

motion clips define the desired style & appearance

multi-clips -> multi-skilled agents

motion-imitation objective + task objective


# 01 - Introduction

Current Problem : Generalization & Directability

Methods
1. Manually Designed Controllers
   1. limited by human insight
   2. difficult to articulate
   3. challenge to encode into controller
2. Kinematic Animation System
   1. must produce reference motions that are feasible to track
   2. difficulty in physical interaction & deviation
   3. limited ability to modify motion to achieve recovery / accomplish goal
   4. complex to implement
3. Reinforcement Learning
   1. trial-and-error -> less need for human insight
   2. generated motions' quality lagged behind, severe artifacts(缺陷)

incorporate MoCap / hand-authored animation data

directly reward the controller for
1. producing motions that resemble reference
2. achieve additional task objective

phase-aware policy


## 02 - Related Work

**Kinematic Models**

**Physics-Based Models**

**Reinforcement Learning**

**Motion Imitation**


## 03 - Overview

## 04 - Background

standard reinforcement learning problem
1. goal : $g$
2. policy : $\pi_\theta(a|s)$, $a \in A, s \in S$
3. current state : $s_t$
4. sampled action from $\pi$ : $a_t$
5. environment respond new state : $s' = s_{t+1}$
   1. sampled from dynamics $p(s' | s, a)$
6. reward : $r_t$ (scalar)
7. expected return : $$j(\theta) = \mathbb{E}_{\tau \sim p_\theta(\tau)}[\sum_{t=0}^T \gamma^t r_t]$$
   1. $p_\theta(\tau) = p(s_0) \prod_{t=0}^{T-1} p(s_{t+1} | s_t, a_t) \pi_\theta(a_t | s_t)$
   2. trajectory $\tau = (s_0, a_0, s_1, \cdots, a_{T-1}, s_T)$，state 比 action 多一个 $s_T$
   3. initial state distribution : $p(s_0)$
   4. total return of a trajectory (horizon $T$ steps) : $\sum_{t=0}^T \gamma^t r_t$
   5. discount factor : $\gamma$, ensure the return is finite

[PPO - 个人笔记](../../../ReinforcementLearning/PPO/PPO.md)

RL : Policy Gradient -> PPO
1. **gradient** of expected return : $\nabla_{\theta}J(\theta)$
   1. 通过 上下同乘 & 梯度对数技巧
   2. $$\nabla_{\theta}J(\theta) = \mathbb{E}_{s_t \sim d_\theta(s_t), a_t \sim \pi_\theta(a_t|s_t)} [\nabla_{\theta}\log(\pi_\theta(a_t|s_t))\mathcal{A}_t]$$
2. 使用 TD(time difference) & GAE(Generalized Advantage Estimation)


## 05 - Policy Representation

**Inputs**
1. character model
2. kinematics reference motions : **sequence** of target poses $\{\hat{q_t}\}$
   1. only provide **kinematic information** (no action)
3. task (reward function)

**States and Actions**
1. **state** $s$ (in character's local coordinate frame)
   1. configuration of character's body
   2. **relative positions** of each link with respect to the root (pelvis)
   3. **rotations** (quaternions 四元数)
   4. **velocities** (linear + angular)
   5. **==phase==** $\phi \in [0, 1]$ (0 = start, 1 = end)
2. **action** (target angle of PD controller)
   1. spherical joints : axis-angle form
   2. revolute  joints : scalar rotation angles



**Control Policy**
1. policy : $\pi(a_t | s_t, g_t)$ (queried at **30 Hz**)
2. state + goal -> action -> torque
3.
4. **torque**(use **action** to compute)
   1. **proportional-derivative** controller abstract away low-level control details
   2. $$\tau_\text{torque} = k_p (q_\text{target} - q_t) - k_d \dot{q}_t$$
   3. $\tau$ : torque
   4. $q_t$ : joint angle

**Rewards**
1. **motion imitation** objective/reward : $r^{I} (s_t, a_t)$
2. **task-specific** objective/reward : $r^{G} (s_t, a_t, g_t)$
   1. reward : single step
   2. return : total trajectory

**Algorithm** : PPO(proximal policy optimization)

**Network** (policy $\pi(a | s, g)$)
1. action distribution : **Gaussian**
   1. mean : $\mu(s)$
      1. 通过 network 计算
   2. covariance : $\Sigma$
      1. **fixed & diagnal**
      2. **hyper-parameter of the algo**




# 07 - Multi-Skill Integration




# 10 - Results

## 10.4 - Ablations

**Reference State Initialization**
1. compare with : fixed initial state

**Early Termination**
1. compare with : w/o early termination



