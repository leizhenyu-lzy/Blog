# Symmetry


---

# On Learning Symmetric Locomotion - SIGGRAPH 2019

Peng XueBin


## 01 - Abstract & Introduction

symmetry is a potential useful structure

DRL need to improve learning efficiency & motion quality

symmetry 与其他 efficiency improvement 方法 orthogonal(互补干扰)

直觉上
1. avoid asymmetric local minima
2. hard symmetry constraints 可能会带来问题
3. 对称策略(policy) 帮助实现 对称动作，并不保证 对称结果(gait)
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

Mirroring Function (镜像函数) 是 environment 的一部分

Mirror State  : $M_s(s)$

Mirror Action : $M_a(a)$

Symmetric Trajectory : $(s, a)$ & $(M_s(s), M_a(a))$


Symmetric Policy
1. $\pi_{\theta}(M_s(s)) = M_a(\pi_{\theta}(s))$
2. 对称策略 传入 镜像状态 时，产生 镜像动作

Symmetric State-Value Function
1. $V(s) = V(\mathcal{M}_s(s))$
2. **NET-POL** 消融实验 : 只在 policy 网络上 使用 对称架构，而在 state-value 网络上 不使用 对称约束，学习速度 & 最终表现 会显著下降


对称策略(policy) 并不保证 对称结果(gait)
1.



在 RL 中，使用 reward function 来 直接优化 gait symmetry 的问题
1. 导致 delayed / sparse reward

追求的是 approximately symmetric 的 policy


### A.1 - Mirroring Functions

不同 joints 类别 的 处理原则
1. common
   1. 位于身体中轴线上的部分，一般是 **绕 $y$ 轴**
   2. 镜像后，保持不变
2. opposite
   1. 位于中轴线上，但运动方向与左右对称相关的部分
   2. 镜像时，取负值
3. side
   1. 成对出现的肢体部件
   2. 镜像时，左右互换(按需 加 负号(非 y-axis))，eg : knee 就不用 加
   3. 为了方便，可以在 构建 urdf 的时候就将 相关旋转轴(除了 绕 y-axis) 反向，省去 取负操作

environment 处理
1. 向量信息(vector-valued): y-axis 方向的值 需要 取反，eg : 速度 & 目标位置
2. 朝向信息(orientations) : roll & yaw 需要 取反，eg : 欧拉角



### 04.01 - Duplicate Tuples (DUP)

### 04.02 - Auxiliary Loss (LOSS)

### 04.03 - Phase-Based Mirroring (PHASE)

### 04.04 - Symmetric Network Architecture




## 07 - Results



---
---

# Symmetry Considerations for Learning Task Symmetric Robot Policies




