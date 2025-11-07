# FastTD3: Simple, Fast, and Capable Reinforcement Learning for Humanoid Control

[FastTD3 - Project Website](https://younggyo.me/fast_td3/)

[FastTD3 - Github](https://github.com/younggyoseo/FastTD3)

[TD3 - Github](https://github.com/sfujim/TD3)

[MuJoCo Playground - Project Website](https://playground.mujoco.org/)

[HumanoidBench - Project Website](https://humanoid-bench.github.io/)

---

bottleneck : slow training

FastTD3 : high-performance variant of the Twin Delayed Deep Deterministic Policy Gradient (TD3) algorithm



optimizations are based on the observations of Parallel Q-Learning (PQL)

Features
1. parallel simulation
2. large batch sizes
3. distributional critic


---

# FastTD3 代码实现

```
fast_td3/
├── fast_td3.py           # 核心算法：Actor、Critic 网络定义
├── fast_td3_simbav2.py   # SimbaV2 变体 (高级网络结构)
├── fast_td3_utils.py     # 工具类 : Replay Buffer、归一化 等
├── train.py              # 训练主循环
├── hyperparams.py        # 超参数配置
└── environments/         # 环境的封装 (humanoid_bench, isaac_lab, mt_bench, mujoco_playground)
```


## fast_td3/fast_td3.py

`DistributionalQNetwork` 类
1. `__init__()`
   1. n_obs : 观测维度
   2. n_act : 动作维度
   3. num_atoms : 分布的 原子数/刻度数，Categorical Distribution
   4. v_min & v_max : Q值 分布的 最 小/大 值，被 分为 num_atoms 个刻度，包括两端
   5. hidden_dim : int
   6. device : `torch.device`
   7. **net** : Linear & ReLU (no softmax)
      1. input  size = n_obs + n_act
      2. output size = num_atoms
      3. 创建 `nn.Linear` 时，PyTorch 会自动初始化权重
      4. 权重(Weight) : 使用 Kaiming Uniform 初始化
      5. 偏置(Bias)   : 使用 Uniform 初始化
2. `forward()` : 组合 obs & actions，喂给 net
3. `projection()` : 执行 贝尔曼分布方程 (Distributional Bellman Equation) 的操作，并 将目标分布 投影回 固定的支持集上
   1. input
      1. obs : $s'$，经验回放缓冲区中采样到的下一状态
      2. actions : $a'$，目标网络计算出的 在下一状态 $S'$ 下的 最佳(贪婪)动作
      3. rewards : 从 当前状态 到 下一状态 获得的奖励
      4. bootstrap : **布尔张量 或 浮点张量(0 或 1)**，表示该转换是否是终止状态
         1. 如果下一状态是终止状态(eg : 游戏结束)，则不应该计算未来回报
      5. discount : 折扣因子
      6. q_support : 当前 Q 网络 建模的 回报值 的离散集合
      7. device
   2. 计算支持点间隔 (delta_z) :  $\Delta z = \frac{V_{max} - V_{min}}{N_{atoms} - 1}$
   3. 计算 目标回报值 (target_z)，根据 Bellman 方程计算 : $\mathcal{T} Z = R + \gamma Z'$
      1. **$Z'$** : 下一状态的 最佳动作 对应的回报分布的 期望，或 直接使用下一状态的 Q 分布的支持点
      2. **q_support**($\{z_j\}$) : 当前网络的 atom支持集
   4. 截断(clamp) & 归一化(b) & 确定相邻原子(下界 l & 上界 u) & 特殊处理(±1)
   5. 计算下一状态的概率 (next_dist)
   6. 投影 & 分配 (proj_dist)
      1. 线性插值，分配 上界/下界 原子的概率
      2. `offset` : 将二维索引 (batch_index, atom_index) 展平为一维索引的技巧，以配合 PyTorch 的 `index_add_` 操作，从而高效地累加概率
      3. `index_add_` : 实现 `next_dist * (u.float() - b)` 和 `next_dist * (b - l.float())` (即 概率分布 × 分配权重) 分别累加到 proj_dist 展平后的张量中对应的 $l$ 和 $u$ 索引上
   7. proj_dist 就是目标贝尔曼分布 $\mathcal{T} Z$ 投影到固定支持集 $\{z_j\}$ 上的概率分布 $\hat{P}$



`Actor` 类
1. `__init__()`
2. `forward()`
3. `explore()`



`MultiTaskActor` 类
1. `__init__()`
2. `forward()`

`Critic` 类 : Double Distributional Q-Network
1. `__init__()`
   1. qnet1 & qnet2 : 实例化 `DistributionalQNetwork` 类
   2. q_support : 通过 `register_buffer()` 实现
      1. `torch.nn.Module` 类的方法，将一个 `torch.Tensor` 注册为模型(`nn.Module` 实例) 的 非训练参数
      2. 不需要梯度更新
      3. 保存到 state_dict
      4. 自动移动到 device (随着 model 本身)
2. `forward()` : 同时调用 qnet1 & qnet2 的 `forward()`
3. `projection()` : 同时调用 qnet1 & qnet2 的 `projection()`
4. `get_value()` : 从 概率分布 计算 期望 Q值



`MultiTaskCritic` 类
1. `__init__()`
2. `forward()`
3. `projection()`



## fast_td3/fast_td3_simbav2.py

TODO

## fast_td3/fast_td3_utils.py



## fast_td3/train.py


## fast_td3/hyperparams.py


## fast_td3/environments

