# 自动控制原理

[toc]

## Portals

[自动控制原理（系统学习） -- 卢京潮](https://www.bilibili.com/video/BV1ZJ411c757)

[自动控制原理（快速学习） -- 轻声说了随便](https://space.bilibili.com/437724982)

![](Pics/icon/lujingchao.png)

## REMAIN

信号与系统和自控联系（传递函数，单位冲激响应，齐次解，特解，零输入，零状态）

## 01 自动控制的一般概念

*卢京潮 p1、p2、p3、p4、p5*

## 02 控制系统的数学模型

**时域模型——微分方程**

线性时不变系统

非线性方程线性化

### 拉普拉斯变换

*卢京潮 p6*

![](Pics/Laplace/Laplace000.png)

微分定理**减$0_-$时**的函数值

使用终值定理的条件是，原像函数的终值确实存在。（否则可能可以计算出结果，但是不正确）

![](Pics/Laplace/Laplace001.png)

![](Pics/Laplace/Laplace009.png)

![](Pics/Laplace/Laplace010.png)

![](Pics/Laplace/Laplace011.png)

![](Pics/Laplace/Laplace013.png)

![](Pics/Laplace/Laplace015.png)

![](Pics/Laplace/Laplace017.png)

![](Pics/Laplace/Laplace019.png)

![](Pics/Laplace/Laplace020.png)

![](Pics/Laplace/Laplace012.png)

![](Pics/Laplace/Laplace014.png)

![](Pics/Laplace/Laplace016.png)

![](Pics/Laplace/Laplace018.png)

### 拉普拉斯逆变换

*卢京潮 p7、p8*

逆变换
1. 反演公式
2. 查表法（部分分式法）--- 使用留数法

**用Laplace变换求解线性常微分方程**

初始条件只与输出有关，输入不受影响

也可以通过Laplace变换求解自由响应（零输入响应）

![](Pics/Laplace/Laplace003.png)

![](Pics/Laplace/Laplace004.png)

![](Pics/Laplace/Laplace005.png)

![](Pics/Laplace/Laplace006.png)

**影响系统响应的因素**
1. 输入信号（规定r(t)=u(t)，阶跃信号，如果跟踪阶跃信号较好，跟踪其他信号会很好）
2. 初始条件（规定零初始条件）
3. 系统的结构参数（自身特性决定系统性能）

### 传递函数

*卢京潮 p8*

定义：**零初始条件下**，线性定常系统输出量拉氏变换与输入量拉氏变换之比。（$G(s)=\frac{C(s)}{R(s)}$）

传递函数和微分方程对应，可以互相唯一确定

两种标准形式
1. 首一标准型
2. 尾一标准型 --> 前面系数为增益

$G(s)=L(系统单位冲激响应)$

![](Pics/Laplace/Laplace007.png)

**传递函数与输入输出无关**

两种求传递函数的方法
1. 对单位冲激响应进行拉氏变换
2. 输出拉氏变换除以输入拉氏变换

（时域卷积等于频域相乘，利用单位冲激信号对原信号进行卷积，得到的就是原信号本身REMAIN）

**传递函数的局限**
1. 原则上**不反映非零初始条件时，系统的全部信息**（定义是零初始条件下，**零状态响应**）
2. **只适用于描述SISO（单输入/单输出）系统**
3. **只能用于表示线性定常系统**，否则无法将$C(s)$提取出来（如下图非线性系统所示）

![](Pics/Laplace/Laplace008.png)

### 控制系统的复域数学模型

*卢京潮 p9、p10*

**典型环节的传递函数**

![](Pics/transferfunc/transferfunc001.png)

![](Pics/transferfunc/transferfunc005.png)

![](Pics/transferfunc/transferfunc002.png)

典型环节不一定有物理实现（分子阶数比分母高）

不同的元部件可以有相同的传递函数

任意传递函数都可以看作典型环节的组合

![](Pics/transferfunc/transferfunc003.png)

如果将系统从中间断开，分别算出传递函数进行相乘，无法得到正常工作时的输入输出传递关系，必须连在一起算（**要考虑负载效应**）。

![](Pics/transferfunc/transferfunc004.png)

### 结构图及其等效变换

*卢京潮 p11、p12*

![](Pics/transferfunc/transferfunc006.png)

**比较点与引出点之间的移动(慎用，很麻烦)**，比较点之间、引出点之间可以分别互相移动而不受影响

![](Pics/transferfunc/transferfunc008.png)

![](Pics/transferfunc/transferfunc009.png)

**难题(Paper Tiger)$\times$2**，一步一步耐心做即可

![](Pics/transferfunc/transferfunc010.png)

![](Pics/transferfunc/transferfunc011.png)

![](Pics/transferfunc/transferfunc012.png)

![](Pics/transferfunc/transferfunc013.png)

**必须要使用“杀手锏”的题**

![](Pics/transferfunc/transferfunc014.png)

![](Pics/transferfunc/transferfunc015.png)

![](Pics/transferfunc/transferfunc016.png)

（将线路进行化简，更改一下走线）

![](Pics/transferfunc/transferfunc017.png)

（注意：负负得正，经过了两个比较点）

![](Pics/transferfunc/transferfunc018.png)

![](Pics/transferfunc/transferfunc019.png)

![](Pics/transferfunc/transferfunc020.png)

（分清并联和反馈）

![](Pics/transferfunc/transferfunc021.png)

### 梅森公式

*卢京潮 p13、p14*

**信号流图**

和方框图不同的是，信号流图的每个点代表一个信号。

相关概念
1. 节点：比较点、引出点
2. 前向通路：**输入到输出，与任何一个节点相交不多于一次的通路**
3. 前向通路增益：前向通路中各传递函数的乘积
4. 回路：**起点和终点再同一节点，且与其他节点相交不多于一次的闭合回路**（顺着信号线方向）
5. 回路增益L：回路中所有传递函数的乘积
6. 不接触回路：互相之间没有公共结点的回路

![](Pics/mason/mason001.png)

（在信号流图中$a_3$和$a_4$看上去连在一起，但并不代表同一个信号。）

**梅森公式/mason Mason**

![](Pics/mason/mason000.png)

对于剩余回路构成的余子式，与前向通路有公共点也不行（注意特征式的正负号、比较点的正负）

![](Pics/mason/mason002.png)

**难题$\times$5**，小心仔细不要漏（前向通路、回路），分清前馈通道和反馈通道（从原点出发的前馈通道构不成回路），比较点的正负

![](Pics/mason/mason003.png)

![](Pics/mason/mason004.png)

（藏B回路，注意只通过$G_3$的回路有两条）

![](Pics/mason/mason005.png)

![](Pics/mason/mason006.png)

（藏B前向通道，初次之外还有一个M形的不要漏）

![](Pics/mason/mason007.png)

![](Pics/mason/mason008.png)

（多输入情况，回路不变总特征式不变）

![](Pics/mason/mason009.png)

### 控制系统传递函数

*卢京潮 p14(后半段)*

**开环传递函数与闭环传递函数之间的关系**

![](Pics/transferfunc/transferfunc007.png)

![](Pics/transferfunc/transferfunc037.png)

**完整框图**

![](Pics/transferfunc/transferfunc022.png)

**控制输入R、干扰输入N、系统输出C、偏差E、反馈B**

**开环传递函数**（不是开环系统的传递函数）

将主反馈切断，得到闭环系统的开环传递函数

开环增益：**开环传递函数化为“尾一”标准型**前面的系数

闭环增益：**闭环传递函数化为“尾一”标准型**前面的系数

![](Pics/transferfunc/transferfunc023.png)

**控制输入r(t)作用下的闭环传递函数**

![](Pics/transferfunc/transferfunc024.png)

$\Phi_e(s)$中的$e$表示对误差的传递函数

**干扰输入n(t)作用下的闭环传递函数**

![](Pics/transferfunc/transferfunc025.png)

**系统总输出和总误差**

利用叠加原理求得，不用×额外的负号（图中有些正号有点不清楚）

![](Pics/transferfunc/transferfunc026.png)

**综合例题**

![](Pics/transferfunc/transferfunc027.png)

（常规计算：先写出输入到输出的传递函数，将输入信号进行拉氏变换，与传递函数相乘，再进行拉氏反变换）

![](Pics/transferfunc/transferfunc028.png)

![](Pics/transferfunc/transferfunc029.png)

![](Pics/transferfunc/transferfunc030.png)

![](Pics/transferfunc/transferfunc031.png)

![](Pics/transferfunc/transferfunc032.png)

![](Pics/transferfunc/transferfunc033.png)

（**计算由初始条件引起的自由响应：已知传递函数，需将其转换为微分方程，同时写出齐次微分方程（零输入响应）。进行拉氏变换，并将初始条件代入，得到由初始条件引起的传递函数。再进行拉氏反变换。**）传递函数，本身计算的是输入为冲激信号的零状态响应，现在要求零输入响应，需要通过求解其次微分方程，同时带入初始条件。

REMAIN

零输入响应：方程为齐次方程，仅有齐次解，特解为0

零状态响应：齐次解+特解

![](Pics/transferfunc/transferfunc034.png)

（利用**叠加原理**，将总的输出计算出来）

（也可以在复数域，将系统所有输出相加，再一起进行拉氏反变换）

![](Pics/transferfunc/transferfunc035.png)

![](Pics/transferfunc/transferfunc036.png)

（偷鸡，由于本例较为简单，不适用于所有情况）

## 03 线性系统的时域分析与校正

### 概述

三个指标
1. 稳（**基本要求**）：稳定性分析。系统受到扰动后能回到原来的平衡位置。
2. 准（**稳态要求**）：稳态误差（稳态精度）稳态输出与理想输出之间的误差要小。
3. 快（**动态要求**）：时间响应&动态性能（跟踪阶跃信号的过渡过程指标）。阶跃响应的过渡过程要平稳迅速。

时域法
1. 可以提供系统时间响应的全部信息
2. 直接在时间域中对系统进行分析校正，直观，准确
3. 基于求解系统输出的解析解，十分繁琐

典型输入信号
1. 单位脉冲
2. 单位阶跃
3. 单位斜坡
4. 单位加速度

![](Pics/timedomain/timedomain001.png)

![](Pics/timedomain/timedomain002.png)

![](Pics/timedomain/timedomain003.png)

超调量：反映平稳性（在峰值时间取得）

**注意：超调量对应的就是单位阶跃响应曲线。二阶系统的闭环传递函数决定了单位阶跃响应最终的形态**。计算系统传递函数的时候不要将阶跃信号算入，只要求$\frac{Y(s)}{R(s)}$即可。

调节时间：反映迅速程度

### 一阶系统的时间响应及动态性能

*卢京潮 p15*

阶跃响应

![](Pics/timedomain/timedomain004.png)

![](Pics/timedomain/timedomain005.png)

调节时间是时间常数三倍（对于一阶系统，将分母化为尾一标准型（不用管分子），s前面的系数就是调节时间）

![](Pics/timedomain/timedomain006.png)

**系统对信号响应的微分=系统对信号的微分的响应**，**系统对信号响应的积分=系统对信号的积分的响应**（对任意有限阶的线性定常系统都成立）
 
![](Pics/timedomain/timedomain007.png)

原先做法是先对单位阶跃响应和单位阶跃信号进行Laplace变换再相除，得到系统闭环传递函数。对闭环传递函数进行Laplace反变换得到k(t)（单位冲激响应）。最后通过开环传递函数和闭环传递函数的关系求解G(s)。

现在可以直接对单位阶跃信号进行求导，得到单位冲激响应。再进行拉氏变换得到闭环传递函数，最后利用开闭环传递函数的关系求解。

### 二阶系统的时间响应及动态性能

*卢京潮 p16*

![](Pics/timedomain/timedomain008.png)

对于二阶系统的传递函数习惯使用**首一标准型**

**$\xi$阻尼比**

**$\omega_n$无阻尼自然频率**

![](Pics/timedomain/timedomain009.png)

1. 零阻尼：两个纯虚根
2. 欠阻尼：两个共轭复根
3. 临界阻尼：一个重实根
4. 过阻尼：两个实根

#### 临界阻尼&过阻尼情况

![](Pics/timedomain/timedomain010.png)  

![](Pics/timedomain/timedomain011.png)

![](Pics/timedomain/timedomain012.png)

将二阶系统拆分为两个惯性环节的级联。可以看到，靠近虚轴较近的极点对于系统动态性能影响较大，距离虚轴远的极点影响较小。（距离虚轴远，与阶跃响应的拉氏变换$\frac{1}{s}$相乘后，进行拉氏反变换，得到的响应$1-e^{-at}$的指数幂是更大的负数，代表更接近阶跃函数本身，所以对系统影响不大。）下图中黑线为实际二阶系统的响应曲线，蓝线为主导极点的阶跃响应。

![](Pics/timedomain/timedomain013.png)


**闭环主导极点**，距离虚轴越近，影响越大

#### 欠阻尼情况

*卢京潮 p17、p18、p19*

极角：从实轴负半轴，顺时针转到共轭复根

![](Pics/timedomain/timedomain014.png)

![](Pics/timedomain/timedomain015.png)

凑项

![](Pics/timedomain/timedomain016.png)

![](Pics/timedomain/timedomain017.png)

![](Pics/timedomain/timedomain018.png)

零阻尼二阶系统，超调量为100%，调节时间为∞。

欠阻尼二阶系统，两个包络线

![](Pics/timedomain/timedomain019.png)

将单位阶跃响应对t求导，得到单位冲激响应。

![](Pics/timedomain/timedomain021.png)

令单位冲激响应等于0，求出极值点。只有正弦函数部分有可能等于零。

![](Pics/timedomain/timedomain022.png)

阻尼比越小，振荡越快，超调量越大。

**峰值时间**

![](Pics/timedomain/timedomain020.png)

**超调量**

![](Pics/timedomain/timedomain023.png)

![](Pics/timedomain/timedomain024.png)

超调量只与阻尼比有关，与无阻尼自然震荡频率无关。只要$\beta$值相同（极点在同一射线上），系统的超调量就确定了。

**阻尼比越大，超调量越小。（$\beta$角越大，超调量越大）**

**上升时间**

比峰值时间小（少转一个$\beta$角）

$\frac{\pi-\beta}{\sqrt{1-\xi} \omega_n}$

**调节时间**

以包络线进入5%误差带的时间为基准（得到的结果偏大，更加保守）。使用包络线是为了让调节时间可以连续变化。

![](Pics/timedomain/timedomain025.png)

（注意这里也不一定是3.5。有别的版本，对于2%误差带是4，对于5%误差带是3）

![](Pics/timedomain/timedomain026.png)

![](Pics/timedomain/timedomain027.png)

![](Pics/timedomain/timedomain028.png)

理论上阻尼比等于0.707最好（精确定义的时候）

利用拉氏变换的终值定理，计算最终的稳定值。

**峰值时间由闭环极点的虚部决定，超调量由极点的实部和虚部之比决定，调节时间由闭环极点的实部决定（实部决定包络线的收敛速度）**

![](Pics/timedomain/timedomain029.png)

![](Pics/timedomain/timedomain030.png)

![](Pics/timedomain/timedomain031.png)

#### 二阶系统性能改善

![](Pics/timedomain/timedomain032.png)

改善二阶系统动态性能措施：
1. **测速反馈——增加阻尼**，对输出求导，再引回误差信号处（输出减输入）。
2. **比例+微分——提前控制**，原来的进入系统的只有误差信号本身，现在再加上误差的导数（PD控制）。误差会有滞后性，控制不及时。而比例微分做到了提前控制。

![](Pics/timedomain/timedomain033.png)

![](Pics/timedomain/timedomain034.png)

从闭环传递函数可以看出，测速反馈做的就是增大阻尼比，降低超调量（如果原先的阻尼比已经够大，就不要使用该方法）。

另外比例微分和测速反馈的闭环特征方程相同，所以闭环极点相同，推出**阻尼比和无阻尼自然震荡频率相同**。

但是，比例微分增加了闭环零点，结果相比测速反馈：**超调量增加，峰值时间减小**。

使用**零点极点法**，计算别的

![](Pics/timedomain/timedomain035.png)

![](Pics/timedomain/timedomain036.png)

![](Pics/timedomain/timedomain037.png)

![](Pics/timedomain/timedomain038.png)

### 高阶系统的阶跃响应及动态性能

*卢京潮 p20*

**KEY:主导闭环极点**：距离虚轴较近，且不存在闭环零极点对消的闭环极点（远的零极点舍弃（距离>=5倍））。

偶极子：零极点对消。

![](Pics/timedomain/timedomain039.png)

上图是一个七阶系统（只画了上半平面，小心共轭复根），现在利用二阶系统估算动态性能指标。

![](Pics/timedomain/timedomain040.png)

### 线性系统的稳定性分析

*卢京潮 p20*

**系统正常工作的首要条件**：受到干扰，偏离平衡位置。干扰消失，回到原来的位置。

![](Pics/timedomain/timedomain041.png)

**对于线性定常系统，通过判断单位冲激响应是否回零**，如果不回零一定不稳定，如果**回零一定稳定**。

**稳定的充要条件**：所有的闭环极点必须具有负实部，也不能在虚轴上。

![](Pics/timedomain/timedomain042.png)

对于高阶系统，解出所有根是否困难。希望有一种可以不求解特征方程的根就能判断系统稳定性。

#### 劳斯判据

**只用考虑闭环极点，零点不考虑**。

![](Pics/timedomain/timedomain043.png)

**如果缺项也是不稳定，全负可能稳定**

首先要满足必要条件。（否则一定不稳定）

不仅可以判断稳定性，还能求出不稳定的点的个数

![](Pics/timedomain/timedomain044.png)

变号的次数就是右半平面的极点数。**（正变负、负变正都算）**

一般劳斯表的最后一行$s^0$的数就是特征方程的最后的常数项。

**特殊情况处理**

①如果劳斯表第一列有0，但不全为零（如果这一行只有第一列有数也不行），用$\varepsilon$（一个很小的正数）代替，继续算。

![](Pics/timedomain/timedomain045.png)

②遇到全零行，虽然可以继续算，但已经不稳定

**辅助方程的解是原特征方程解的子集。**（更新后的如果没变号，一定是在虚轴上的一对纯虚根，不稳定。变号可能是一对符号相反的实根，或者两对实部符号相反、虚部相同的共轭复根）。

对辅助方程求导。

![](Pics/timedomain/timedomain046.png)

![](Pics/timedomain/timedomain047.png)

**对于二阶系统，系数全部大于零，系统稳定。**

**对于三阶系统，系数全部大于零，中间两个系数的乘积大于外边两个系数的乘积，则稳定**

![](Pics/timedomain/timedomain048.png)

系统的开环稳定和闭环稳定不能相互保证。

![](Pics/timedomain/timedomain049.png)

K是开环增益不同于$K_a$。

![](Pics/timedomain/timedomain050.png)

两种思路（**基本原则，方程本身不能变**）
1. 将原特征方程中拆解出(s+1)
2. 将s=x-1带入，只要x都在虚轴左边，就能保证s比-1小

**系统的稳定性是自身的属性，与输入类型和形式无关**

**系统的稳定与否，只取决于闭环极点，与闭环零点无关**，闭环零点实惠影响系统的动态性能，但不会影响稳定性。

![](Pics/timedomain/timedomain051.png)

![](Pics/timedomain/timedomain052.png)

### 线性系统的稳态误差

*卢京潮 p21、p22*

**准，稳态误差是系统稳态性能指标，对系统控制精度的度量**

**只有与稳定系统才有研究稳态误差的意义**，一定要**先判稳**。

原理性误差（不考虑由于系统非线性因素引起的误差）

![](Pics/timedomain/timedomain053.png)

无差系统不是在任何情况都无差，只是在阶跃输入作用下。

![](Pics/timedomain/timedomain054.png)

按输出端定义的误差（强行写成单位负反馈形式）。按输入端定义的计算时较为方便。

由输入和干扰共同作用。一般说稳定误差就是静态误差（如果系统不稳定，只能得到动态误差）。

![](Pics/timedomain/timedomain055.png)

**利用拉普拉斯变换的终值定理**

#### 静态误差

![](Pics/timedomain/timedomain056.png)

**输入的闭环传递函数和干扰的闭环传递函数分母相同**

计算动态性能指标时，同一加单位阶跃信号。计算稳态误差时，没有这种规定，输入信号也可以是斜坡、加速度信号等等。

![](Pics/timedomain/timedomain057.png)

当输入提高“档次”后，无差系统就不一定无差了。

**静态误差系数法**

开环传递函数中由v个纯积分环节。纯积分环节的个数称为型别（类型）。

**型别是对闭环系统而言的，但是计算时是将主反馈打断，求出开环传递函数，看有几个纯积分环节**

**开环传递函数有几个积分环节，闭环系统就称为几型的**

![](Pics/timedomain/timedomain058.png)

显然，稳态误差与输入有关，也和系统的结构参数有关（最关键的是开环增益和型别）。

![](Pics/timedomain/timedomain059.png)

静态位置、速度、加速度误差系数是针对输入信号的（分别对应阶跃、斜坡、加速度信号）

![](Pics/timedomain/timedomain060.png)

**结论：**
1. **型别确定后，稳态误差随输入档次的增加而增加**
2. **输入档次确定后，稳态误差随型别的增加而降低**
3. **当型别和输入档次对等的时候，稳态误差是一个非零的常值**
4. **型别高、输入档次低，稳态误差为0**
5. **型别低、输入档次高，稳态误差为∞**

![](Pics/timedomain/timedomain061.png)


![](Pics/timedomain/timedomain062.png)

对于上图系统，输入最终一定等于输出。否则，假设达到稳态并且输出不等于输入，误差经过一个积分环节，再经过一个比例微分环节，再经过一个积分环节将会得到一个二次向上升的信号。与假设不符合。

**系统的型别对于减小稳态误差有很关键的因素，但是也不是越多越好。型别越高系统越难稳定（特征多项式越容易缺项，不稳定）。**

下题只能使用定义法求解。

![](Pics/timedomain/timedomain063.png)

前馈环节不影响系统的稳定性，不影响系统的传递函数。（写开环传递函数的时候不管前馈通道。（本题不用？REMAIN））写特征方程也不管前馈通道，因为只和回路有关，前馈构不成回路（用梅森公式考虑）。（本体其实也不需要写开环传递函数）

可以看出**按前馈补偿的符合控制方案可以有效提高系统的稳态精度**

![](Pics/timedomain/timedomain064.png)

最后稳态误差的式子中剩余什么说明什么起作用。本例对于输入信号产生的稳态误差，$s_1、s_2$都起作用才能和之前的$s^2$约去。对于干扰产生的稳态误差，只有$s_1$起了作用

![](Pics/timedomain/timedomain065.png)

一定要判稳

![](Pics/timedomain/timedomain066.png)

#### 动态误差

REMAIN 

### 线性系统的时域校正



瞬态响应

相对稳定性



## 04 根轨迹法

![](Pics/rootlocus/rootlocus001.png)

用于解决系统的分析和校正，根轨迹法也称作复域法

**一定是闭环特征根的轨迹**

**开环传递函数，写为首一标准型，系数$K^*$称为根轨迹增益**，根轨迹增益仅对开环传递函数而言。



### 根轨迹法的基本概念

*卢京潮 p25*

![](Pics/rootlocus/rootlocus002.png)

![](Pics/rootlocus/rootlocus003.png)

对于系统的调节时间，靠近虚轴的点的影响更大。向左移动，调节时间变短（由之前的系统性能指标可得，实部大渐近线衰减快）。**靠近虚轴的点是主导极点**

![](Pics/rootlocus/rootlocus004.png)

$K^*$越大，稳态误差越小。

![](Pics/rootlocus/rootlocus005.png)

闭环零点不会随开环增益改变，但是包括前向通道的开环零点和反馈通道的开环极点。

同时满足模条件和相角条件说明在根轨迹上。（$K^*$是0到∞变化的，所以模条件总是可以满足的，但是相角条件并不一定满足）

![](Pics/rootlocus/rootlocus006.png)

![](Pics/rootlocus/rootlocus007.png)

![](Pics/rootlocus/rootlocus008.png)

![](Pics/rootlocus/rootlocus009.png)

相角条件是充要条件，模值条件用于确定根轨迹增益

### 绘制根轨迹的基本法则

*卢京潮 p26（后半段）、p27、p28*

![](Pics/rootlocus/rootlocus017.png)

**法则1-4**

![](Pics/rootlocus/rootlocus010.png)

![](Pics/rootlocus/rootlocus011.png)

共轭开环零极点对于实轴上的根轨迹相角条件贡献为0（每组都是$2\pi$），实轴上的每一个开环零极点对于根轨迹的贡献为$\pi$。

![](Pics/rootlocus/rootlocus012.png)

当开环传递函数给定，a的值也就随之确定，开环极点的和等于$-a_{n-1}$（将分母$GH(s)$展开即得）也确定了。对于闭环特征方程，如果$n-m\geqslant2$，则不会影响到$-a_{n-1}$，所以**闭环极点之和就等于开环极点之和，是一个常数**。

![](Pics/rootlocus/rootlocus013.png)

用$\sigma、\omega$列写方程（以$K^*$为中间变量），如果可以表达成圆方程的形式就证明轨迹是圆弧。

相切时，超调量最大。

![](Pics/rootlocus/rootlocus014.png)

![](Pics/rootlocus/rootlocus015.png)

![](Pics/rootlocus/rootlocus016.png)

**法则5-8**

![](Pics/rootlocus/rootlocus018.png)

从根轨迹上的无穷远点s看，所有零极点都在“质心”上，这样相角条件很容易得出，n-m个角度的和要等于$(2k+1)\pi$。最终对任意整数k，不同的相角只有n-m个。

对于幅值条件，相当于s到质心距离的n-m次方，进行展开。同时，利用长除法，得到相对应位置的系数，得证。

![](Pics/rootlocus/rootlocus019.png)

由根之和可知，在本题中，-1和0的分离点应该在-0.5和-1之间（-4和-2的根在向右走），同时也不能超过渐近线。

![](Pics/rootlocus/rootlocus020.png)

分离点至少是一个二重根。

![](Pics/rootlocus/rootlocus021.png)

对于算出的根轨迹，需要进行检验，以保证正确性，不符合的要舍去。

![](Pics/rootlocus/rootlocus022.png)

根轨迹与虚轴交点有两种求法
1. 利用劳斯表全零行，求出根轨迹增益$K^*$（**这个根轨迹增益就是使得系统临界稳定的根轨迹增益**，还要经过换算得到开环增益$K$）。全零行上一行构成辅助方程，求解该方程即可。（如果要继续写完劳斯表，将辅助方程求导，得到对应系数继续列写）
2. 将$s=j\omega$带入特征方程进行求解，将结果进行检验。

![](Pics/rootlocus/rootlocus023.png)

![](Pics/rootlocus/rootlocus024.png)

在要求的极点附近取一点（挨得很近，开环零点极点到这个点的向量近似等于到所求点的向量）。通过相角条件列写方程，$\Theta_1$就是所要求的出射角。

![](Pics/rootlocus/rootlocus025.png)

![](Pics/rootlocus/rootlocus026.png)

![](Pics/rootlocus/rootlocus027.png)

![](Pics/rootlocus/rootlocus028.png)

![](Pics/rootlocus/rootlocus029.png)

上图可以稳定但是稳定的不多（右边的曲线向左穿过虚轴的时候是稳定的）。但系统的动态特性不好，$\beta$角较大，阻尼比小，超调量大。另外极点实部较小，调节时间较长。

![](Pics/rootlocus/rootlocus030.png)

### 广义根轨迹

*卢京潮 p29、p30*

REMAIN

### 利用根轨迹分析系统性能

*卢京潮 p31、p32*

REMAIN












**闭环特征根**在s平面的位置影响**相对稳定性**和**瞬态性能**。

与劳斯判据结合

**闭环传递函数**

$T(s)=\frac{Y(s)}{R(s)}=\frac{p(s)}{q(s)}$

特征方程$q(s)$，决定了系统响应模式

原则上利用相角条件就能得到根轨迹

根轨迹与实轴交点 --> 临界阻尼

**绘制根轨迹**

1. 将特征方程写成特定形式$1+K^*\frac{\Pi(s+z_i)}{\Pi(s+p_j)}=0$，**首一形式**，$z_i$，$p_j$是开环的零极点，特征方程的根是闭环极点的轨迹，$K^*$是根轨迹增益（开环增益化成**首一形式**）。
2. 根轨迹起始于开环极点、终止于开环零点
3. 实轴上的根轨迹段：位于奇数个开环零点和极点的左侧
4. 根轨迹分支条数等于开环极点的个数
5. 根轨迹分支关于实轴对称
6. 根轨迹渐近线
   1. 与实轴交角：$$
   2. 在实轴位置：开环极点个数N，开环零点n，$\$


## 05 线性系统的频域分析与校正

### 频率特性的基本概念

*卢京潮 p33、p34*



### 幅相频率特性

*卢京潮 p33、p34*

### 对数频率特性

*卢京潮 p33、p34*

### 稳定裕度

*卢京潮 p33、p34*

### 利用开环频率特性特性系统性能

*卢京潮 p33、p34*

### 闭环频率特性曲线的绘制

*卢京潮 p33、p34*

### 利用闭环频率特性分析系统的性能

*卢京潮 p33、p34*

### 频率法串联校正

*卢京潮 p33、p34*

## 06 线性离散系统的分析与校正

### 离散系统

*卢京潮 p57*

离散系统由两种
1. 采样系统 --- 时间离散，数值连续
2. 数字系统 --- 时间离散，数值量化（会有量化误差）

计算机控制系统优点：
1. 控制由程序实现，便于修改，可以实现复制控制律
2. 抗干扰性强
3. 一机多用，利用率高
4. 便于联网，实现生产过程的自动化和管理

计算机控制系统缺点：
1. 采样点间信息丢失，和连续系统相比，性能有所下降
2. 需要附加模数转换、数模转换

![](Pics/discretetime/discretetime001.png)

A/D过程：
1. 采样：时间上离散 --- 理想采样过程（采样瞬间完成，没有量化误差）
2. 量化：数值上离散
3. 编码：

数字计算机
1. 离散输入、离散输出
2. 可以看成连续输出加上一个采样开关
   ![](Pics/discretetime/discretetime002.png)

D/A过程：
1. 零阶保持器（ZOH --- zero order holder）
2. 将离散的信号变为阶梯信号

### 信号采样与保持

*卢京潮 p57、p58*

**理想采样序列及其拉氏变换**

![](Pics/discretetime/discretetime003.png)

![](Pics/discretetime/discretetime004.png)

![](Pics/discretetime/discretetime005.png)

![](Pics/discretetime/discretetime007.png)

两种表达方式
1. 离散信号与连续信号在采样点的关系
2. 离散系统像函数和连续系统像函数的关系（联系**香农采样定理**）

![](Pics/discretetime/discretetime006.png)


**采样定理（Shannon）**

信号完全复现的**必要条件**（没有理想滤波器，使用的是零阶保持器），规定了离散系统采样周期的设计

频谱和频率特性
1. 频谱对信号
2. 频率特性对系统（输出信号的傅里叶变换和输入信号的傅里叶变换的比）

周期信号，频谱离散；非周期信号，频谱密度连续

![](Pics/discretetime/discretetime008.png)

![](Pics/discretetime/discretetime009.png)

**零阶保持器对系统的影响**

![](Pics/discretetime/discretetime010.png)

（将$s=j\omega$带入第二个式子，取出一半（凑欧拉公式），使用欧拉公式）

抽样频率$\omega_s=\frac{1}{T}$，由香农采样定理，希望得到的理想滤波器是从$0\rightarrow\frac{\omega_s}{2}$的矩形框，如下图蓝线所示

![](Pics/discretetime/discretetime012.png)

![](Pics/discretetime/discretetime011.png)

零阶保持器近似看作**相角延迟环节**

导致了**相角裕度损失、系统稳定程度降低、动态性能指标变差**（数字系统性能变差的原因）

### Z变换

*卢京潮 p59、p60*

![](Pics/discretetime/discretetime013.png)

**将抽样信号的Laplace变换中的$e^{sT}$用$z$代换**（一般取$T=1$），即得到Z变换。

注意**不是**将$e^{-sT}$用$z$代换，**没有负号**

$z^{-1}$表示一拍延迟

**z变换只能对应离散信号，不能对应连续信号（不知道是有哪个连续信号抽样得来的）。**连续信号如果采样结果相同，则z变换也相同。

**连续信号先将t替换为nT**

**Z变换方法**
1. 级数求和法（定义法）
2. 查表法（部分分式展开法）
3. 留数法（反演积分法）

![](Pics/discretetime/discretetime014.png)

![](Pics/discretetime/discretetime015.png)

对表的说明：连续信号经过采样得到的离散信号再进行z变换（t=nT）

![](Pics/discretetime/discretetime036.png)

![](Pics/discretetime/discretetime016.png)

![](Pics/discretetime/discretetime017.png)

![](Pics/discretetime/discretetime018.png)

（**计算乘以$\frac{z}{z-e^{-Ts}}$的留数**）

**Z变换基本性质**

![](Pics/discretetime/discretetime034.png)

![](Pics/discretetime/discretetime019.png)

![](Pics/discretetime/discretetime020.png)

![](Pics/discretetime/discretetime022.png)

![](Pics/discretetime/discretetime024.png)

![](Pics/discretetime/discretetime026.png)

![](Pics/discretetime/discretetime028.png)

用一拍超前信号减去原信号（利用超前定理）

超前、滞后定理例题

![](Pics/discretetime/discretetime021.png)

假设蓝点为原信号，例8表示将信号延时一拍得到黑点，例9表示将超前两拍得到红点（又由于单边z变换指研究t大于0，所以要将前面两个红点减去）

复位移定理例题

![](Pics/discretetime/discretetime023.png)

初值定理例题

![](Pics/discretetime/discretetime025.png)

终值定理例题

![](Pics/discretetime/discretetime027.png)

**Z变换的局限性**
1. 只反映采样点信息（不对应连续函数）
2. 一定条件下，输出的连续信号在采样点处会有跳变

![](Pics/discretetime/discretetime037.png)

上图展示了Z变换的局限性，如果没有零阶保持器（将数字信号转为模拟信号），将会产生锯齿，和预期信号不符。

### Z反变换

*卢京潮 p60*

![](Pics/discretetime/discretetime029.png)

**长除法(可能写不出通项、只能写成有限项)**

![](Pics/discretetime/discretetime030.png)

**查表法（先除个z再进行展开，方便展开成熟悉的形式）**

![](Pics/discretetime/discretetime031.png)

**留数法（注意多重根）**

![](Pics/discretetime/discretetime032.png)

（**计算乘以$z^{n-1}$的留数**）

![](Pics/discretetime/discretetime033.png)

Z变换和Z反变换的留数法不同

![](Pics/discretetime/discretetime035.png)

### 离散系统的数学模型

*卢京潮 p61、p62*

**线性常系数差分方程及其解法**

![](Pics/discretetime/discretetime038.png)

![](Pics/discretetime/discretetime039.png)

**前向差分：未来到现在**

**后向差分：现在到过去**

**线性**：两端都是输入变量或者输出变量的采样值。**不出现交叉乘积项，不出现高次乘方项。**

**定常**：系数为常数

![](Pics/discretetime/discretetime040.png)

![](Pics/discretetime/discretetime041.png)

![](Pics/discretetime/discretetime042.png)

**脉冲传递函数**

在输出的地方虚设采样开关，使得可以用离散系统的分析方法进行分析（**舍得，退一步是为了进两步——卢京潮**）

G(z):单位脉冲响应序列的Z变换

![](Pics/discretetime/discretetime043.png)

![](Pics/discretetime/discretetime044.png)

![](Pics/discretetime/discretetime045.png)

环节之间有采样开关的时候，需要分别计算再相乘

环节之间无采样开关的时候，需要整体计算

![](Pics/discretetime/discretetime046.png)

有ZOH时，可以将ZOH进行拆分（中间可以添加一个采样开关，不影响系统整体结构，而且可以分开计算在相乘），信号经过采样开关，再经过$\frac{1}{s}$积分环节后，变为阶梯信号

![](Pics/discretetime/discretetime047.png)

通过和之前的结果进行比较，可以发现，**加ZOH环节并不改变系统阶数，也不改变开环极点，只改变开环零点**。

**对于离散系统，梅森增益公式不可用**（有采样开关）

对误差信号e的采样开关可以等效为再输入信号和反馈信号处添加采样开关。

![](Pics/discretetime/discretetime048.png)

上图使用梅森增益公式没错

![](Pics/discretetime/discretetime049.png)

上图使用梅森增益公式没错

