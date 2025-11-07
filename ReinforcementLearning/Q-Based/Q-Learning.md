# Q-Learning

Q-Learning 特性
1. Value-based : 学习的是 Q值 函数 Q(s,a)，即 状态-动作 价值函数
2. Model-Free
3. Off-Policy

PPO 使用 **状态价值 $V$**，Q-Learning 使用 **动作价值 $Q$**

**潜在奖励** 用 **Q表** 表示 (state-action 为 行-列)，有初始值，后续不断更新

更新使用 **Temporal-Difference Update (TD 更新式)**
1. 用 一步采样 经验逼近 **Bellman Optimality Equation**，也称为 **BootStrap**
2. $$\delta_t \;=\; r_t + \gamma \max_{a'} Q(s_{t+1}, a_{t+1}) - Q(s_t, a_t) \qquad \text{(TD 误差)}$$
   1. $r$ : 单步 reward
   2. $a_{t+1}$ : 不一定是下一步实际执行的动作，只是通过 max 选出来的
3. $$Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha\,\delta_t \qquad \text{(TD 更新)}$$
   1. $\alpha$ : learning rate
4. 当前 Q 值 = 旧的 Q 值 + 学习步长 × (实际奖励 + 未来最大 Q 值 - 旧的 Q 值)

Q 是 在状态 s 选择动作 a 后，**未来能获得的累积奖励的估计值**，不仅仅考虑当前奖励，还考虑未来可能获得的奖励，类似于 **经验分数**

$\epsilon$-greedy : 百分数，表示按照Q表选择动作的概率，其他时候随机选择行为

<img src="Pics/ql001.png" width=600>

不断扩展，不断衰减 $\gamma$

<img src="Pics/ql002.png" width=600>






