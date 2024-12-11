
[UofT - 自动驾驶课程](https://space.bilibili.com/144564877/channel/collectiondetail?sid=4047592)




普通最小二乘
1. 认为 noise 方差相同

加权最小二乘
1. 使用 不同仪器测量，不同精度
2. 仪器的 noise 方差越大，给予的 权重越小(方差倒数)
3. 普通最小二乘 是 加权最小二乘 的特殊情况(相同权重)

递归最小二乘(Recursive Least Squares)
1. 对于 a stream of data，来一个 观测数据 做一次估计，不需要等待全部数据，每次仅使用上一次的最优估计和当前测量值，不需要对全部现有数据进行估计
2. 已知 上一时刻的最优估计值 $\hat{x}_{k-1}$ & 当前时刻都测量值 $y_k$，估计当前时刻的估计值 $\hat{x}_{k}$ (不使用再前面的数据)
3. Hidden Markov Model(隐马尔可夫模型)，基于马尔可夫过程的，但在其状态是 **隐藏的(不可直接观测)** 情况下进行建模
4. 核心是找到 **Gain Matrix** $K_k$
   1. $$\hat{x}_k = \hat{x}_{k-1} + K_k ( y_k - H_k \hat{x}_{k-1})$$
   2. 最小化 平方误差的 期望值(use probabilistic function)，即 方差
   3. 协方差矩阵的 Trace(迹) 就是 方差之和


最小二乘(Least Squares) & 最大似然(Maximum Likelihood)
1. connection between the method of `least squares` & `maximum likelihood` with **Gaussian Random Variables**
2. Measurement Model (eg : $y=x+v$, $v \sim N(0, \sigma^2)$)
   1. measurement 是 likelihood(似然)
   2. $\hat{x} = \text{argmax}_x p(y|x)$
   3.

