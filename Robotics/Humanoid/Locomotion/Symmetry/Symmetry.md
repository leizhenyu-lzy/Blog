# Symmetry


---

# On Learning Symmetric Locomotion - SIGGRAPH 2019

Peng XueBin

## 01 - Abstract & Introduction

symmetry is a potential useful structure

DRL need to improve learning efficiency & motion quality

symmetry 与去趟 efficiency improvement 方法 orthogonal(互补干扰)

直觉上
1. avoid asymmetric local minima
2. hard symmetry constraints 可能会带来问题
3. 对称策略 帮助实现 对称动作，并不保证 对称结果
   1. eg : 奔跑步态 在任意瞬间 都是不对称的，但 是由 对称策略 在不同时间点 驱动出来的结果

integrate symmetry **inductive bias(归纳偏置)**
1. DUP (Duplicate Tuples)  : 数据增强法，将 每条运动数据 及 其镜像副本 同时 存入经验回放池，tuple : $(s_t, a_t, r_t, s_{t+1})$
2. LOSS (Auxiliary Loss)   : 辅助损失法，增加 损失函数，惩罚 策略输出 & 镜像输出 的差异
3. PHASE (Phase Mirroring) : 相位镜像法，将步态周期 分为两半，前半周 学习原始策略，后半周 直接使用镜像后的策略
4. NET (Symmetric Network) : 对称网络法，通过 网络结构设计，使 模型 在数学上 保证 对于镜像输入 产生镜像输出

## 02 - Related Work



## 03 - Background

RL问题定义 & PPO


## 04 - Symmetry Enforcement Methods

镜像状态 $M_s(s)$

镜像动作 $M_a(a)$

对称的策略
1. $$\pi_{\theta}(M_s(s)) = M_a(\pi_{\theta}(s))$$
2. 给 policy 镜像的 state 作为 input，policy output 的 action 也必须是 原 action 的镜像


symmetric trajectory 定义

symmetric action 定义






## Results



---

# Symmetry Considerations for Learning Task Symmetric Robot Policies




