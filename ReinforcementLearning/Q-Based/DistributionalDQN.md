# Distributional DQN

```
Distributional DQN
├── Categorical DQN (C51)      ← 用固定的离散原子表示分布
├── QR-DQN                     ← 用分位数(Quantile)表示分布
├── IQN                        ← 隐式分位数网络
└── FQF                        ← 全参数化分位数函数
```

C51 是 Categorical DQN 经典做法

用 **固定的离散支持**(通常 51 个原子，C51) 表示回报分布，并把一次 Bellman 备份得到的目标分布 投影回这组原子上，再用 **交叉熵** 训练

Q 网络 输出对这些原子的概率 $p_{\theta}(z_i | s, a)$，通过 softmax 得到

**传统 DQN** 输出 **确定的 Q值**

**Categorical DQN** 输出 **离散的 Q值 概率分布**

可以计算 期望 Q