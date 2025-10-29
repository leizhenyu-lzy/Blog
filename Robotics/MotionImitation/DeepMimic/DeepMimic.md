# DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills

ACM SIGGRAPH 2018

[DeepMimic - Project Website](https://xbpeng.github.io/projects/DeepMimic/index.html)

---

Input
1. character model
2. kinematics reference motions : sequence of target poses $\{\hat{q_t}\}$
3. task (reward function)

Control Policy
1. $\pi(a_t | s_t, g_t)$
2. state + goal -> action -> torque
3. use action(target angle of PD controller) compute torque
   1. $$\tau_\text{torque} = k_p (q_\text{target} - q_t) - k_d \dot{q}_t$$
   2. $\tau$ : torque
   3. $q_t$ : joint angle

Reward
1. imitation reward : $r^{I} (s_t, a_t)$
2. task-specific reward : $r^{G} (s_t, a_t, g_t)$

