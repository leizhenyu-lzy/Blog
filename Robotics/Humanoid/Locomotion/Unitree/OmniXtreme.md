# OmniXtreme : Breaking the Generality Barrier in High-Dynamic Humanoid Control

[OmniXtreme - Project Website](https://extreme-humanoid.github.io/#method)

[OmniXtreme - Github](https://github.com/Perkins729/OmniXtreme)

---


## Table of Contents
- [OmniXtreme : Breaking the Generality Barrier in High-Dynamic Humanoid Control](#omnixtreme--breaking-the-generality-barrier-in-high-dynamic-humanoid-control)
  - [Table of Contents](#table-of-contents)
- [01 - Abstract \& Introduction](#01---abstract--introduction)
- [02 - Related Work](#02---related-work)
- [03 - Methodology](#03---methodology)
- [04 - Experiment](#04---experiment)
- [05 - Conclusion](#05---conclusion)
- [06 - Appendix](#06---appendix)
  - [K - Knee Negative Power Penalty](#k---knee-negative-power-penalty)


---

diverse extreme behaviors in 1 unified policy

---

# 01 - Abstract & Introduction


---

# 02 - Related Work

---

# 03 - Methodology

---

# 04 - Experiment

---

# 05 - Conclusion

---

# 06 - Appendix


## K - Knee Negative Power Penalty

核心目的 : 防止 过强的 再生制动(Braking) 损坏电路

**瞬时(instantaneous) 机械功率** : $P = \tau · \dot{q}$ (力矩 乘以 角速度)
1. $\tau$ (Tau)      : 关节输出的力矩(Torque)，单位 $N · m$
2. $\dot{q}$ (q-dot) : 关节的角速度(Angular Velocity)，单位 $rad/s$
3. 正负
   1. **正功率** ($P > 0$) : **耗电模式**，力矩方向 与 运动方向 **相同**，代表 电机 正在消耗电能来产生机械能
      1. eg : 机器人蹬地起跳、支撑身体上升
   2. **负功率** ($P < 0$) : **发电模式**，力矩方向 与 运动方向 **相反**，代表 电机 处于制动/刹车状态
      1. eg : 落地冲击时 膝盖被动弯曲，电机施加反向力矩减速
      2. 会产生 巨大的 **反向电流**(再生制动)
      3. 负功率过大，会触发机器人的 过流保护、电池欠压，甚至烧毁驱动板

$$\tilde{P}_j = \max(0, -P_j - 150)$$
1. 设置 死区(deadband) = 150
2. 惩罚 超过死区阈值的 过大 负功率

$$c_{knee} = \sum_{j \in \mathcal{J}_{knee}} \left( \frac{\tilde{P}_j}{500} \right)^2$$
1. 归一化惩罚项
2. 500 是 normalization 常数项 power_norm

最终奖励 : 乘以 权重 $w = -10$，即 $r_{knee} = -10 \cdot c_{knee}$




