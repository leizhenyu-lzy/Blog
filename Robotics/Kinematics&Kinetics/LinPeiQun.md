# 机器人学 运动学 & 动力学

## Table of Contents

- [机器人学 运动学 \& 动力学](#机器人学-运动学--动力学)
  - [Table of Contents](#table-of-contents)
- [台大机器人学 运动学(Kinematics) - 林沛群](#台大机器人学-运动学kinematics---林沛群)
  - [01 Spatial Descriptions and Transforms](#01-spatial-descriptions-and-transforms)
  - [02 - Manipulator Kinematics](#02---manipulator-kinematics)
- [台大机器人学 动力学(Kinetics) - 林沛群](#台大机器人学-动力学kinetics---林沛群)


---


# 台大机器人学 运动学(Kinematics) - 林沛群

[台大机器人学之运动学(Kinematics) - 林沛群](https://www.bilibili.com/video/BV1v4411H7ez)

## 01 Spatial Descriptions and Transforms

Rigid Body 状态描述
1. **2D 平面** : 2 Translation DoF + 1 Rotation DoF
2. **3D 空间** : 3 Translation DoF + 3 Rotation DoF

位移 & 姿态 (displacement & orientation)

**移动**
1. $\vec{P} = { }^{A} P_{B \ \text{org}}$ = origin of {B} represented in {A}
2. <img src="Pics/lpq001.png" width=450>



**转动**
1. **作用 1** : 描述 {B} 相对于 {A} 的姿态
   1. 从 {A} 看 {B} 的单个基向量，要得到值，相当于要将 {B} 的 该基向量 向 {A} 的 三个基向量进行 **投影(点乘)**
   2. <img src="Pics/lpq002.png" width=500>
2. **作用 2** : 用于转换向量坐标系(**坐标变换**)
   1. 从 {B} 看 一个向量 P 的坐标为 $[p_x, p_y, p_z]^T$，是在 {B} 的三个基上的分量(投影)。${}^A_B R$ 的各列 表示从 {A} 看 {B} 的各个基的表示，要得到在 {A} 的三个基的分量，仅需用 {B} 下的 P 左乘 ${}^A_B R$
   2. 从公式的角度理解(向量点乘，需在相同坐标系，无论基于哪个坐标系，得到的数值不变)
      <img src="Pics/lpq006.png" width=600>
3. **作用 3** : 描述物体转动状态 (**右手螺旋**确定方向)
   1. 旋转和坐标变换的关联
      1. 旋转 相当于带着整个坐标系 转到 新的位置，然后看 新向量 在 旧坐标系 下的坐标
      2. 可以看成 新向量在新坐标系下的坐标(等于旧向量在旧坐标系下的坐标)，再转换回 旧坐标系
   2. <img src="Pics/lpq007.png" width=250>
   3. $$R_{\hat{X}_A}(\theta)=\left[\begin{array}{ccc}
        1 & 0           & 0              \\
        0 & \cos \theta & -\sin \theta   \\
        0 & \sin \theta &  \cos \theta
        \end{array}\right]$$
   4. <img src="Pics/lpq008.png" width=400>
   5. $$R_{\hat{Y}_A}(\theta)=\left[\begin{array}{ccc}
        \cos \theta & 0 & \sin \theta   \\
        0            & 1 & 0             \\
        -\sin \theta & 0 & \cos \theta
        \end{array}\right] \text{注意负号位置}$$
   6. <img src="Pics/lpq009.png" width=400>
   7. $$R_{\hat{Z}_A}(\theta)=\left[\begin{array}{ccc}
        \cos \theta & -\sin \theta & 0   \\
        \sin \theta &  \cos \theta & 0   \\
        0           & 0            & 1
        \end{array}\right]$$
   8. <img src="Pics/lpq010.png" width=400>
4.  **性质**
   1. **${}^B_A R = {}^A_B R^T$** : 观察完全展开的 矩阵 ${}^A_B R$，显然 转置后，每一列可以看做 将 {A} 的 同一个基向量 向 {B} 的 三个基向量进行 **投影(点乘)**，因此可以得到 ${}^B_A R$
      1. <img src="Pics/lpq003.png" width=500>
   2. **${}^A_B R^T = {}^A_B R^{-1} = {}^B_A R$**(对于 Rotation Matrix， 逆 等于 转置) - (P.S. **${}^A_B R ^T × {}^A_B R = I$**)
      1. <img src="Pics/lpq004.png" width=450>

**Orthogonal Matrix 性质**
1. <img src="Pics/lpq005.png" width=500>
2. Rotation Matrix 的行列式为1，Reflection Matrix 的行列式为-1(TODO)

**3D空间中的旋转 & Rotation Matrix**
1. 空间中的 Rotation 有 3个 DoF，当前已知 有 分别绕 X/Y/Z 轴的旋转矩阵，需要将一般的 Rotation Matrix 表达的姿态拆分成 3次 绕 X/Y/Z 轴 旋转角度
2. 注意事项
   1. Rotation Matrix 是 **non-commutable**不可交换顺序，需要定义 旋转的顺序
   2. 旋转轴 需要明确定义
      1. Fixed Angles - **外旋(Extrinsic Rotation)**，旋转操作**相对于固定的全局坐标系(世界坐标系)**
      2. Euler Angles - **内旋(Intrinsic Rotation)**，旋转操作**相对于物体的当前局部坐标系**
3. **X-Y-Z Fixed Angles - 由 Angles 推算 R** - 先转的先左乘，位置在后面
   1. <img src="Pics/lpq011.png" width=550>
4. **X-Y-Z Fixed Angles - 由 R 推算 Angles** - 借助结果旋转矩阵的9个数字之间的关系，反推旋转角度
   1. <img src="Pics/lpq012.png" width=550>
   2. `atan` & `atan2`
      1. `arctan`(或 `atan`) 是 **标准的反正切函数**，输出范围$(-\frac{\pi}{2}, \frac{\pi}{2})$，即 **第一、第四象限**
      2. `atan2` 是 **扩展的反正切函数**，，范围$(-\pi, \pi)$，即 **四个象限**
   3. 当绕中间的 Y轴 旋转 **+90°** 时，导致**Gimbal Lock - 万向节死锁现象** **==☆==**，X轴 & Z轴 重合，没有唯一解
      1. 原 ${}^A_B R_{XYZ}(\gamma, \beta, \alpha)$ 会退化，四个数仅能得到 $\gamma - \alpha$

         $$\begin{align*}
            {}^A_B R_{XYZ} (\gamma, \beta, \alpha)
            &=\left[\begin{array}{ccc}
            0  & \cos \alpha \sin \gamma - \sin \alpha \cos \gamma & \cos \alpha \cos \gamma + \sin \gamma \sin \alpha \\
            0  & \sin \alpha \sin \gamma + \cos \alpha \cos \gamma & \sin \alpha \cos \gamma - \cos \alpha \sin \gamma \\
            -1 & 0                                                 & 0
            \end{array}\right] \\
            &=\left[\begin{array}{ccc}
            0  & \sin(\gamma - \alpha) &  \cos(\gamma - \alpha) \\
            0  & \cos(\gamma - \alpha) & -\sin(\gamma - \alpha) \\
            -1 & 0                     & 0
            \end{array}\right]
            \end{align*}$$
5. **Z-Y-X Euler Angles - 由 Angles 推算 R** - **先转的后左乘**，位置在前面(相当于一步步进行反向接力，解算回初始坐标系) - 和 Fixed Angles 顺序正好相反
   1. <img src="Pics/lpq013.png" width=550>
6. **Z-Y-Z Euler Angles - 由 Angles 推算 R** - 先转的后左乘，位置在前面(相当于一步步进行反向接力，解算回初始坐标系) - 和 Fixed Angles 顺序正好相反
   1. <img src="Pics/lpq014.png" width=550>
7. **Z-Y-Z Euler Angles - 由 R 推算 Angles** - 和 Fixed Angle 一样，会遇到 **Gimbal Lock**(当 $\beta = 0$，没有唯一解)
   1. <img src="Pics/lpq015.png" width=550>
   2. 针对不同的 R 有不同的 拆解方法 (ZYX, ZYZ)
8. 总结
   1. Euler Angles & Fixed Angles 各有 $3×2×2 = 12$(1、3转轴可以一样，相邻转轴不能一样) 种顺序可能
   2. <img src="Pics/lpq016.png" width=500>


**Homogeneous Transformation Matrix (T)** 齐次变换矩阵
1. 将 Rotation & Translation 整合 - 16个元素，6 DoF
   1. <img src="Pics/lpq017.png" width=350>
2. **移动 & 旋转** 复合 (向量 先旋转、再平移)
   1. <img src="Pics/lpq018.png" width=500>
3. Homogeneous Matrix 好处 - 可以进行连续变换
4. **Homogeneous Transformation Matrix (T)** 的三种用法(类似于 Rotation Matrix 的三种用法)
   1. <img src="Pics/lpq023.png" width=550>
5. Transformation Matrix 运算
   1. 连续运算 : 要注意 每个 frame 之间的 原点向量 需要 逐级变换到 参考系
   2. <img src="Pics/lpq024.png" width=550>
6. 逆矩阵
   1. 旋转部分 : 求逆，也就是 转置
   2. 平移部分 : ${}^B P_{A \ org}$，要达到 反向操作的效果，需要将 原点间距向量 ${}^A P_{B \ org}$ 取反(反向移回)，并从 {B} frame 进行表示 $- {}^B_A R \  {}^A P_{B \ org} = - {}^A_B R^T \  {}^A P_{B \ org}$
   3. <img src="Pics/lpq025.png" width=600>
7. 连续运算
   1. 注意 : 求逆部分不需要直接求，使用上述逆矩阵的特性即可方便得到
   2. <img src="Pics/lpq026.png" width=550>
   3. <img src="Pics/lpq027.png" width=600>



**Operators 算子** : Translation & Rotation & Transformation
1. single 移动 & 旋转
   1. <img src="Pics/lpq019.png" width=550>
2. combined 移动 & 旋转
   1. 先转动再移动 ≠ 先移动再转动(移动的向量也会被转动)
   2. <img src="Pics/lpq020.png" width=550>
3. frame 中的点运动 = frame 做反向运动 (CCW = counter-clock-wise, CW = clock-wise)
   1. <img src="Pics/lpq021.png" width=550>
   2. 感觉有点类似于 内旋，需要根据当前 frame 进行反向操作，而不是针对原始 frame - TODO
   3. <img src="Pics/lpq022.png" width=550>




**Gimbal Lock - 万向节死锁**
1. [Gimbal Lock - Wikipedia](https://en.wikipedia.org/wiki/Gimbal_lock)
   <img src="Pics/Gimbal_Lock_Plane.gif">



## 02 - Manipulator Kinematics



[](#01-spatial-descriptions-and-transforms)


---

# 台大机器人学 动力学(Kinetics) - 林沛群

[台大机器人学之动力学(Kinetics) - 林沛群](https://www.bilibili.com/video/BV1Vt41157jp/)


