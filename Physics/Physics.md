# Physics

---

## Table of Contents

- [Physics](#physics)
  - [Table of Contents](#table-of-contents)
- [动量 \& 角动量](#动量--角动量)
- [进动(precession) \& 章动(nutation)](#进动precession--章动nutation)
- [惯性张量](#惯性张量)
- [转动惯量/惯性矩(Moment of Inertia) \& 极惯性矩(Polar Moment of Inertia) \& 惯性积(Product of Inertia)](#转动惯量惯性矩moment-of-inertia--极惯性矩polar-moment-of-inertia--惯性积product-of-inertia)
  - [材料力学](#材料力学)



---

# 动量 & 角动量

<img src="Pics/physics001.gif" width=300>

**角动量**
1. $$L = \vec{r} × \vec{P} = \vec{r} × (m \vec{v}) = \vec{r} × (\vec{\omega} × (m \vec{r})) = m \vec{r}^2 \vec{\omega} = I \vec{\omega}$$
   1. $\vec{v} = \vec{\omega} × \vec{r}$
   2. $\vec{\omega} · \vec{r} = 0$
   3. 利用 向量 三重积 公式 $a × (b × c) = b(a · c) - c(a · b)$
2. 物理量
   1. 角动量 $L$ : Angular Momentum，物体围绕 点/轴 旋转时，所包含的 旋转运动量
   2. **转动惯量** $I$ : Moment of Inertia
   3. 角速度 $\vec{\omega}$ : Angular Velocity
3. **方向** : 右手螺旋法则，手指指向旋转方向，与角速度方向一致

类似于 描述 直线运动的 动量，可以类比为 旋转动量

**动量**
1. $P = m v$
2. 物理量
   1. 动量 $P$ : Linear Momentum
   2. 质量 $m$ : Mass
   3. 速度 $v$ : Velocity
3. **方向** : 动量的方向和速度的方向一致



**动量定理** (不考虑 m 变化)
1. $$\frac{d \vec{P}}{dt} = \frac{m d\vec{v}}{dt} = m \vec{a} = \vec{F}$$

**角动量定理**
1. $$\frac{d \vec{L}}{dt} = \frac{d (\vec{r} × \vec{P})}{dt} = \frac{d \vec{r}}{dt} × (m \vec{v}) + \vec{r} × \frac{d \vec{P}}{dt} = \vec{r} × \vec{F} = \vec{\tau}$$
   1. 注意 $\vec{r}$ 是 位置矢量，因此 $\frac{d \vec{r}}{dt} = \vec{v}$，因此 $\frac{d \vec{r}}{dt} × (m \vec{v}) = 0$



总结
1. <img src="Pics/physics002.png" width=700>
2. <img src="Pics/physics003.png" width=700>
3. <img src="Pics/physics004.png" width=700>

角动量守恒 : 没有外部**力矩**作用的情况下，系统的总角动量保持不变

角动量是否守恒 与 动量是否守恒 没有直接的联系

---

# 进动(precession) & 章动(nutation)

进动
1. 当一个旋转的刚体 受到外力矩作用时，旋转轴不会静止不动，而是会绕某个方向缓慢地旋转
2. eg : 陀螺
   1. <img src="Pics/physics005.gif" width=150> <img src="Pics/physics006.png" width=400>
   2. 重力 & 支撑力 产生 力矩(右手螺旋)
      1. 起作用的力矩来源是重力
      2. 支持力的主要作用是提供一个反作用力，防止物体掉落，本身不直接产生力矩
   3. 根据角动量定理 $\frac{d \vec{L}}{dt} = \vec{\tau}$，力矩使角动量的方向发生变化
   4. 旋转轴发生进动，角动量的大小，方向随着施加的力矩方向发生旋转
   5. **陀螺的高速旋转产生了角动量，而角动量具有保持方向的特性**


---

# 惯性张量

[List of moments of inertia - Wiki](https://en.wikipedia.org/wiki/List_of_moments_of_inertia)

[转动惯量列表 - Wiki](https://zh.wikipedia.org/wiki/%E8%BD%89%E5%8B%95%E6%85%A3%E9%87%8F%E5%88%97%E8%A1%A8)

绕定点转动 比 绕定轴转动 复杂，方向不确定

惯性张量 : 3×3 对称矩阵
1. $$ I = \begin{bmatrix}
       I_{xx} & -I_{xy} & -I_{xz} \\
      -I_{xy} &  I_{yy} & -I_{yz} \\
      -I_{xz} & -I_{yz} &  I_{zz}
      \end{bmatrix}$$
2. 主对角线 : 惯量矩(moments of inertia)
   1. $I_{xx}$ : 绕 x 轴
   2. $I_{yy}$ : 绕 y 轴
   3. $I_{zz}$ : 绕 z 轴
3. 其他元素 : 惯量积(products of inertia)

---

# 转动惯量/惯性矩(Moment of Inertia) & 极惯性矩(Polar Moment of Inertia) & 惯性积(Product of Inertia)

[转动惯量 - Wiki](https://zh.wikipedia.org/wiki/%E8%BD%89%E5%8B%95%E6%85%A3%E9%87%8F)

惯性矩(轴 2次矩)
1. 恒正
2. 单位 : $m^4$

极惯性矩(点 2次矩)
1. 恒正
2. 单位 : $m^4$

惯性积(2轴 2次混合矩)
1. 可正、可负、可零
2. 单位 : $m^4$
3. **对称刚体在主轴惯性积为零**

惯性矩 & 极惯性矩 可以用 垂直轴定理 关联

## 材料力学

材料 越远离 bending axis，横截面 越硬，越抗弯
1. <img src="Pics/physics007.png" width=400>

area moment of inertia = second moment of inertia
1. <img src="Pics/physics008.png" width=400>

depending on where place the reference axis

一般采用的 axes 通过 质心，用积分计算
1. <img src="Pics/physics009.png" width=450>

平行轴定理，用于 不通过质心，但平行于 质心轴 的 axes
1. <img src="Pics/physics010.png" width=450>

Example
1. <img src="Pics/physics011.png" width=450>

P.S. AREA moment of inertia(面积惯性矩) ≠ MASS moment of inertia(质量惯性矩)
1. <img src="Pics/physics012.png" width=400>


Polar moment of inertia(极惯性矩) - **J**
1. 截面 对 点 的 面积惯性矩，与 点的选取 有关
2. 垂直轴定理
   1. <img src="Pics/physics013.png" width=450>

坐标旋转
1. <img src="Pics/physics014.png" width=500>




