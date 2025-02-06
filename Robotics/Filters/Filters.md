# Filter

Bayes Filter 提供 **通用框架**

Kalman Filter 适用于 **线性高斯系统**

Particle Filter 适用于 **非线性非高斯系统**



Dynamic System (State Space Model)
1. Hidden Markov Models(HMM, 隐马尔可夫模型) - Discrete State
2. Kalman Filter - Linear Dynamic System - Linear Mixture Gaussian Model
3. Particle Filter - Non-Linear Non-Gaussian Dynamic System


Problems
1. Learning : 学习参数
2. Inference :
   1. decoding
   2. probability of evidence
   3. filtering(online) :
   4. smoothing(offline) :
   5. prediction


## Table of Contents

- [Filter](#filter)
  - [Table of Contents](#table-of-contents)
- [Bayes Filter](#bayes-filter)
  - [递归形式推导](#递归形式推导)
    - [马尔可夫 Markov 假设](#马尔可夫-markov-假设)
    - [分解观测数据](#分解观测数据)
    - [递归形式](#递归形式)
  - [递归过程](#递归过程)
    - [预测 Predict](#预测-predict)
    - [更新 Update](#更新-update)
  - [总结](#总结)
- [Kalman Filter](#kalman-filter)
  - [模型](#模型)
    - [状态转移模型](#状态转移模型)
    - [观测模型](#观测模型)
  - [递归过程](#递归过程-1)
  - [相关链接](#相关链接)
- [Particle Filter](#particle-filter)


---

# Bayes Filter

Bayes Filter 是一个通用的概率框架，用于估计动态系统的状态

通过 递归更新 状态的 后验概率分布，结合 系统模型 & 观测模型 进行状态估计

Bayes Filter 是其他滤波算法的基础框架

核心 : **贝叶斯公式**

Related
1. [贝叶斯公式解读 - 张颢](../../Math/Probability/Probability.md#贝叶斯公式-bayes-rule)
2. [MAP 最大后验概率](../../Math/Probability/Probability.md#最大后验概率估计-mapmaximum-a-posteri归一化ori)
3. MAP 只关注 最有可能的单个状态，而 Bayes Filter 计算 **整个后验分布**

Bayes 过滤器主要用于解决 隐状态(Hidden State)估计问题


系统 : 状态 $x_t$，传感器测量值 $z_t$，需要求解 $p(x_t | z_{1:t})$ (后验概率分布)

**==区分==**
1. 先验(Prior) : $p(x_t | z_{1:t-1})$
   1. 还没有看到当前时刻的观测数据 $z_t$，对当前状态 $x_t$ 的预测
2. 后验(Posterior) : $p(x_t | z_{1:t})$
   1. 还没有看到当前时刻的观测数据 $z_t$，对当前状态 $x_t$ 的更新估计


## 递归形式推导

最终形式如下 :

$$p(x_t | z_{1:t}) = \frac{p(z_t | x_t)p(x_t | z_{1:t-1})}{p(z_t | z_{1:t-1})}$$


在 Bayes Filter 的更新步骤中，我们希望计算在给定所有观测数据 $z_{1:t}$ 的条件下，状态 $x_t$ 的后验分布 $p(x_t|z_{1:t})$。

根据贝叶斯定理，可得(不适用于 **递归计算**) :

$$p(x_t|z_{1:t}) = \frac{p(z_{1:t}|x_t)p(x_t)}{p(z_{1:t})}$$

为了将其转化为递归形式，我们需要引入以下假设和分解 :


### 马尔可夫 Markov 假设

假设
1. 当前 **状态** $x_t$ 只依赖于 **前一时刻的状态** $x_{t-1}$，即
   1. $$p(x_t|x_{0:t-1}) = p(x_t|x_{t-1})$$
2. 当前 **观测** $z_t$ 只依赖于 **当前状态** $x_t$，即
   1. $$p(z_t|x_{0:t}, z_{1:t-1}) = p(z_t|x_t)$$

**==注意==**
1. 状态 $x_t$ 之间并不相互独立，相关
2. 观测 $z_t$ 之间也不相互独立，相关(通过 $x_t$ 之间)

### 分解观测数据

观测数据 $z_{1:t}$ 可以分解为
1. **当前的观测** $z_t$
2. **过去的观测** $z_{1:t-1}$

似然函数可以写为

$$p(z_{1:t}|x_t) = p(z_t|x_t) \cdot p(z_{1:t-1}|x_t)$$


### 递归形式

通过以上假设和分解，我们可以将后验分布 $p(x_t|z_{1:t})$ 写为 :

$$p(x_t|z_{1:t}) = \frac{p(z_t|x_t) \cdot p(z_{1:t-1}|x_t) \cdot p(x_t)}{p(z_{1:t})}$$

进一步简化
1. $p(z_{1:t-1}|x_t) \cdot p(x_t)$ 可以表示为 $p(x_t|z_{1:t-1}) \cdot p(z_{1:t-1})$
2. $p(z_{1:t})$ 可以分解为 $p(z_t|z_{1:t-1}) \cdot p(z_{1:t-1})$

最终，公式可以简化为

$$p(x_t|z_{1:t}) = \frac{p(z_t|x_t) \cdot p(x_t|z_{1:t-1})}{p(z_t|z_{1:t-1})}$$

分母不能再简化了，因为 如果 没有给定 $x_t$，$z_t$ 和 $z_{1:t-1}$ 之间并不独立 (提供了 $x_{t-1}$ 的信息，又通过状态转移模型 影响 $x_t$，相当于间接提供了 $x_t$ 的信息)


## 递归过程

### 预测 Predict

利用系统的 **动态模型(状态转移模型)** 预测 **当前状态的先验概率分布** $p(x_t | z_{1:t-1})$
1. **系统动态模型** : $p(x_t | x_{t-1})$ 表示从状态 $x_{t-1}$ 转移到 $x_t$ 的概率
2. **上一时刻的后验分布** : $p(x_{t-1} | z_{1:t-1})$

通过全概率公式，预测 **当前状态的先验分布**

$$p(x_t | z_{1:t-1}) = \int p(x_t | x_{t-1}) p(x_{t-1} | z_{1:t-1}) dx_{t-1}$$


### 更新 Update


利用当前的观测数据 $z_t$ 来修正 **预测的先验分布**，得到 **后验分布** $p(x_t | z_{1:t})$
1. **观测模型** : $p(z_t | x_t)$ 表示在状态 $x_t$ 下观测到 $z_t$ 的概率
2. **先验分布**(当前时刻) : $p(x_t | z_{1:t-1})$

根据贝叶斯定理，更新后验分布 :

$$p(x_t | z_{1:t}) = \frac{p(z_t | x_t) p(x_t | z_{1:t-1})}{p(z_t | z_{1:t-1})}$$

其中，$p(z_t | z_{1:t-1})$ 是归一化常数，确保后验分布的总概率为 1

$$p(z_t | z_{1:t-1}) = \int p(z_t | x_t) p(x_t | z_{1:t-1}) dx_t$$



## 总结

Bayes Filter 体现了贝叶斯思想的核心 : 通过不断结合先验知识和新的观测数据，逐步修正对世界的认识

应用
1. 机器人定位
2. 目标跟踪
3. 传感器融合

书籍
1. 《Probabilistic Robotics》（概率机器人学） : 详细讲解 Bayes Filter 及其应用
2. 《Estimation with Applications to Tracking and Navigation》 : 深入探讨状态估计的理论和实践

课程
1. Coursera 上的《Robotics: Estimation and Learning》
2. edX 上的《Autonomous Mobile Robots》




---

# Kalman Filter

**核心假设**
1. **线性系统** : 系统的 状态转移模型 & 观测模型 都是线性的
2. **高斯噪声** : 系统的 过程噪声 & 观测噪声 都服从高斯分布


## 模型

### 状态转移模型

$$x_t = F_t x_{t-1} + B_t u_t + w_t$$
1. $x_t$ : 当前时刻的状态
2. $F_t$ : 状态转移矩阵
3. $u_t$ : 控制输入
4. $B_t$ : 控制输入矩阵
5. $w_t$ : 过程噪声，服从高斯分布 $w_t \sim \mathcal{N}(0, Q_t)$


### 观测模型

$$z_t = H_t x_t + v_t$$
1. $z_t$ : 当前时刻的观测
2. $H_t$ : 观测矩阵
3. $v_t$ : 观测噪声，服从高斯分布 $v_t \sim \mathcal{N}(0, R_t)$


## 递归过程

预测 & 更新

(1) 预测步骤 (Prediction Step)

在预测步骤中，我们利用系统的状态转移模型预测当前时刻的状态和协方差。

- 状态预测：

\[
\hat{x}_{t|t-1} = F_t \hat{x}_{t-1|t-1} + B_t u_t
\]

- \(\hat{x}_{t|t-1}\)：基于 \(t-1\) 时刻的状态估计，预测 \(t\) 时刻的状态。
- \(\hat{x}_{t-1|t-1}\)：\(t-1\) 时刻的后验状态估计。

- 协方差预测：

\[
P_{t|t-1} = F_t P_{t-1|t-1} F_t^T + Q_t
\]

- \(P_{t|t-1}\)：预测状态的协方差矩阵。
- \(P_{t-1|t-1}\)：\(t-1\) 时刻的后验协方差矩阵。
- \(Q_t\)：过程噪声的协方差矩阵。

(2) 更新步骤 (Update Step)

在更新步骤中，我们利用当前的观测数据修正预测结果，得到更准确的状态估计。

- 计算卡尔曼增益：

\[
K_t = P_{t|t-1} H_t^T (H_t P_{t|t-1} H_t^T + R_t)^{-1}
\]

- \(K_t\)：卡尔曼增益，用于权衡预测值和观测值。
- \(R_t\)：观测噪声的协方差矩阵。

- 状态更新：

\[
\hat{x}_{t|t} = \hat{x}_{t|t-1} + K_t (z_t - H_t \hat{x}_{t|t-1})
\]

- \(\hat{x}_{t|t}\)：更新后的状态估计。
- \(z_t - H_t \hat{x}_{t|t-1}\)：观测残差（也称为新息）。

- 协方差更新：

\[
P_{t|t} = (I - K_t H_t) P_{t|t-1}
\]

- \(P_{t|t}\)：更新后的协方差矩阵。
- \(I\)：单位矩阵。






## 相关链接

[机器学习 - 白板推导系列(十五) - 线性动态系统 - 卡曼滤波(Kalman Filter)](https://www.bilibili.com/video/BV1zW411U7fa/)

[合集 [卡尔曼滤波器] DR_CAN 合集](https://space.bilibili.com/230105574/channel/collectiondetail?sid=1814741)













---

# Particle Filter

Particle Filter 是 Bayes Filter 在 **非线性非高斯系统** 的实现

通过一组随机样本(粒子)来近似状态的后验分布



















