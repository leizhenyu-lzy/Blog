# DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills

ACM SIGGRAPH 2018

[DeepMimic - Project Website](https://xbpeng.github.io/projects/DeepMimic/index.html)

---

Current Problem : Generalization & Directability

RL's trial-and-error -> less need for human insight

current RL generated motions' quality lagged behind, severe arfifacts(缺陷)

---

**Inputs**
1. character model
2. kinematics reference motions : **sequence** of target poses $\{\hat{q_t}\}$
   1. only provide kinematic information (not action)
3. task (reward function)

**Control Policy**
1. policy : $\pi(a_t | s_t, g_t)$ (queried at **30 Hz**)
2. state + goal -> action -> torque
3. **state** $s$ (in character's local coordinate frame)
   1. configuration of character's body
   2. relative positions of each link with respect to the root (pelvis)
   3. rotations (quaternions 四元数)
   4. velocities (linear + angular)
   5. phase $\phi \in [0, 1]$ (0 - start, 1 - end)
4. action(target angle of PD controller)
   1. spherical joints : axis-angle form
   2. revolute  joints : scalar rotation angles
5. **torque**(use **action** to compute)
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





