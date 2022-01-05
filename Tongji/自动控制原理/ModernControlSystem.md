# 自动控制原理

[toc]

## Portals

[自动控制原理 -- 卢京潮](https://www.bilibili.com/video/BV1ZJ411c757)

[自动控制原理 -- 轻声说了随便](https://space.bilibili.com/437724982)

## 01 自动控制的一般概念

*卢京潮 p1、p2、p3、p4、p5*

## 02 控制系统的数学模型

**时域模型——微分方程**

线性时不变系统

非线性方程线性化

### 拉普拉斯变换

*卢京潮 p6*

![](Pics/Laplace000.png)

微分定理**减$0_-$时**的函数值

使用终值定理的条件是，原像函数的终值确实存在。（否则可能可以计算出结果，但是不正确）

![](Pics/Laplace001.png)

![](Pics/Laplace009.png)

![](Pics/Laplace010.png)

![](Pics/Laplace011.png)

![](Pics/Laplace013.png)

![](Pics/Laplace015.png)

![](Pics/Laplace017.png)

![](Pics/Laplace019.png)

![](Pics/Laplace020.png)

![](Pics/Laplace012.png)

![](Pics/Laplace014.png)

![](Pics/Laplace016.png)

![](Pics/Laplace018.png)

### 拉普拉斯逆变换

*卢京潮 p7、p8*

逆变换
1. 反演公式
2. 查表法（部分分式法）--- 使用留数法

**用Laplace变换求解线性常微分方程**

初始条件只与输出有关，输入不受影响

也可以通过Laplace变换求解自由响应（零输入响应）

![](Pics/Laplace003.png)

![](Pics/Laplace004.png)

![](Pics/Laplace005.png)

![](Pics/Laplace006.png)

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

$G(s)=L(系统单位冲击响应)$

![](Pics/Laplace007.png)

**传递函数与输入输出无关**

两种求传递函数的方法
1. 对单位冲击响应进行拉氏变换
2. 输出拉氏变换除以输入拉氏变换

**传递函数的局限**
1. 原则上**不反映非零初始条件时，系统的全部信息**（定义是零初始条件下）
2. **只适用于描述SISO（单输入/单输出）系统**
3. **只能用于表示线性定常系统**，否则无法将$C(s)$提取出来（如下图非线性系统所示）

![](Pics/Laplace008.png)

### 控制系统的复域数学模型

*卢京潮 p9、p10*

**典型环节的传递函数**

![](Pics/transferfunc001.png)

![](Pics/transferfunc005.png)

![](Pics/transferfunc002.png)

典型环节不一定有物理实现（分子阶数比分母高）

不同的元部件可以有相同的传递函数

任意传递函数都可以看作典型环节的组合

![](Pics/transferfunc003.png)

如果将系统从中间断开，分别算出传递函数进行相乘，无法得到正常工作时的输入输出传递关系，必须连在一起算（**要考虑负载效应**）。

![](Pics/transferfunc004.png)

### 结构图及其等效变换

![](Pics/transferfunc007.png)

![](Pics/transferfunc006.png)

**比较点与引出点之间的移动(慎用，很麻烦)**，比较点之间、引出点之间可以分别互相移动而不受影响

![](Pics/transferfunc008.png)

![](Pics/transferfunc009.png)


### 梅森增益公式

### 瞬态响应

### 相对稳定性

### 根轨迹法

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



## 奈奎斯特判据

## 线性离散系统的分析与校正

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

![](Pics/discretetime001.png)

A/D过程：
1. 采样：时间上离散 --- 理想采样过程（采样瞬间完成，没有量化误差）
2. 量化：数值上离散
3. 编码：

数字计算机
1. 离散输入、离散输出
2. 可以看成连续输出加上一个采样开关
   ![](Pics/discretetime002.png)

D/A过程：
1. 零阶保持器（ZOH --- zero order holder）
2. 将离散的信号变为阶梯信号

### 信号采样与保持

*卢京潮 p57、p58*

**理想采样序列及其拉氏变换**

![](Pics/discretetime003.png)

![](Pics/discretetime004.png)

![](Pics/discretetime005.png)

![](Pics/discretetime007.png)

两种表达方式
1. 离散信号与连续信号在采样点的关系
2. 离散系统像函数和连续系统像函数的关系（联系**香农采样定理**）

![](Pics/discretetime006.png)


**采样定理（Shannon）**

信号完全复现的**必要条件**（没有理想滤波器，使用的是零阶保持器），规定了离散系统采样周期的设计

频谱和频率特性
1. 频谱对信号
2. 频率特性对系统（输出信号的傅里叶变换和输入信号的傅里叶变换的比）

周期信号，频谱离散；非周期信号，频谱密度连续

![](Pics/discretetime008.png)

![](Pics/discretetime009.png)

**零阶保持器对系统的影响**

![](Pics/discretetime010.png)

（将$s=j\omega$带入第二个式子，取出一半（凑欧拉公式），使用欧拉公式）

抽样频率$\omega_s=\frac{1}{T}$，由香农采样定理，希望得到的理想滤波器是从$0\rightarrow\frac{\omega_s}{2}$的矩形框，如下图蓝线所示

![](Pics/discretetime012.png)

![](Pics/discretetime011.png)

零阶保持器近似看作**相角延迟环节**

导致了**相角裕度损失、系统稳定程度降低、动态性能指标变差**（数字系统性能变差的原因）

### Z变换

*卢京潮 p59、p60*

![](Pics/discretetime013.png)

**将抽样信号的Laplace变换中的$e^{sT}$用$z$代换**（一般取$T=1$），即得到Z变换。

注意**不是**将$e^{-sT}$用$z$代换，**没有负号**

$z^{-1}$表示一拍延迟

**z变换只能对应离散信号，不能对应连续信号（不知道是有哪个连续信号抽样得来的）。**连续信号如果采样结果相同，则z变换也相同。

**连续信号先将t替换为nT**

**Z变换方法**
1. 级数求和法（定义法）
2. 查表法（部分分式展开法）
3. 留数法（反演积分法）

![](Pics/discretetime014.png)

![](Pics/discretetime015.png)

对表的说明：连续信号经过采样得到的离散信号再进行z变换（t=nT）

![](Pics/discretetime036.png)

![](Pics/discretetime016.png)

![](Pics/discretetime017.png)

![](Pics/discretetime018.png)

（**计算乘以$\frac{z}{z-e^{-Ts}}$的留数**）

**Z变换基本性质**

![](Pics/discretetime034.png)

![](Pics/discretetime019.png)

![](Pics/discretetime020.png)

![](Pics/discretetime022.png)

![](Pics/discretetime024.png)

![](Pics/discretetime026.png)

![](Pics/discretetime028.png)

用一拍超前信号减去原信号（利用超前定理）

超前、滞后定理例题

![](Pics/discretetime021.png)

假设蓝点为原信号，例8表示将信号延时一拍得到黑点，例9表示将超前两拍得到红点（又由于单边z变换指研究t大于0，所以要将前面两个红点减去）

复位移定理例题

![](Pics/discretetime023.png)

初值定理例题

![](Pics/discretetime025.png)

终值定理例题

![](Pics/discretetime027.png)

**Z变换的局限性**
1. 只反映采样点信息（不对应连续函数）
2. 一定条件下，输出的连续信号在采样点处会有跳变

![](Pics/discretetime037.png)

上图展示了Z变换的局限性，如果没有零阶保持器（将数字信号转为模拟信号），将会产生锯齿，和预期信号不符。

### Z反变换

*卢京潮 p60*

![](Pics/discretetime029.png)

**长除法(可能写不出通项、只能写成有限项)**

![](Pics/discretetime030.png)

**查表法（先除个z再进行展开，方便展开成熟悉的形式）**

![](Pics/discretetime031.png)

**留数法（注意多重根）**

![](Pics/discretetime032.png)

（**计算乘以$z^{n-1}$的留数**）

![](Pics/discretetime033.png)

Z变换和Z反变换的留数法不同

![](Pics/discretetime035.png)

### 离散系统的数学模型

*卢京潮 p61、p62*

**线性常系数差分方程及其解法**

![](Pics/discretetime038.png)

![](Pics/discretetime039.png)

**前向差分：未来到现在**

**后向差分：现在到过去**

**线性**：两端都是输入变量或者输出变量的采样值。**不出现交叉乘积项，不出现高次乘方项。**

**定常**：系数为常数

![](Pics/discretetime040.png)

![](Pics/discretetime041.png)

![](Pics/discretetime042.png)

**脉冲传递函数**

在输出的地方虚设采样开关，使得可以用离散系统的分析方法进行分析（**舍得，退一步是为了进两步——卢京潮**）

G(z):单位脉冲响应序列的Z变换

![](Pics/discretetime043.png)

![](Pics/discretetime044.png)

![](Pics/discretetime045.png)

环节之间有采样开关的时候，需要分别计算再相乘

环节之间无采样开关的时候，需要整体计算

![](Pics/discretetime046.png)

有ZOH时，可以将ZOH进行拆分（中间可以添加一个采样开关，不影响系统整体结构，而且可以分开计算在相乘），信号经过采样开关，再经过$\frac{1}{s}$积分环节后，变为阶梯信号

![](Pics/discretetime047.png)

通过和之前的结果进行比较，可以发现，**加ZOH环节并不改变系统阶数，也不改变开环极点，只改变开环零点**。

**对于离散系统，梅森增益公式不可用**（有采样开关）

对误差信号e的采样开关可以等效为再输入信号和反馈信号处添加采样开关。

![](Pics/discretetime048.png)

上图使用梅森增益公式没错

![](Pics/discretetime049.png)

上图使用梅森增益公式没错
