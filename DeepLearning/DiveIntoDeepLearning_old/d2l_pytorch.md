# 动手学深度学习

![](Pics/Others/d2l-ai.png)

## 01 传送门

[d2l课程主页](https://zh-v2.d2l.ai/index.html)

[李沐B站主页](https://space.bilibili.com/1567748478)

[d2l-ai的Github主页](https://github.com/d2l-ai/d2l-zh)

<br>

## 02 深度学习介绍

图片分类（IMAGENET）

物体检测和分割
1. 物体检测（物体是什么出现在什么地方）
2. 物体分割（每个像素属于什么物体）

样式迁移

人脸合成

文字生成图片

文字生成（gpt3）

无人驾驶

广告点击

![](Pics/P01toP10/P01_001.png)


<br>


## 03 安装


## 04 数据操作+数据预处理

### 数据操作

N维数组样例

![](Pics/P01toP10/P04_001.png)

![](Pics/P01toP10/P04_002.png)

![](Pics/P01toP10/P04_003.png)

下图中，一列那里写错了，冒号和1位置反了

![](Pics/P01toP10/P04_004.png)

### 数据操作实现

见Jupyter Notebook

### 数据预处理实现

见Jupyter Notebook

### 数据操作QA

## 07 自动求导

### 自动求导

链式法则

![](Pics/P01toP10/P07_001.png)

自动求导

神经网络层数多，难以手写求导

![](Pics/P01toP10/P07_002.png)


计算图

PyTorch提供的autograd 包能够根据输⼊和前向传播过程自动构建计算图，并执⾏行反向传播

Tensor 是这个包的核心类，如果将其属性 .requires_grad 设置为 True ，它将开始追
踪(track)在其上的所有操作（这样就可以利利⽤用链式法则进⾏行行梯度传播了了）。完成计算后，可以调
⽤用 .backward() 来完成所有梯度计算。此 Tensor 的梯度将累积到 .grad 属性中。


注意在 y.backward() 时，如果 y 是标量量，则不需要为 backward() 传⼊入任何参数；否则，需要
传⼊一个与 y 同形的 Tensor

如果不想要被继续追踪，可以调⽤ .detach() 将其从追踪记录中分离出来，这样就可以防⽌将来的计
算被追踪，这样梯度就传不过去了。此外，还可以用 with torch.no_grad() 将不不想被追踪的操作代
码块包裹起来，这种方法在评估模型的时候很常用，因为在评估模型时，我们并不需要计算可训练参数
（ requires_grad=True ）的梯度。


加入中间变量

每个圈代表输入或者操作

![](Pics/P01toP10/P07_003.png)

![](Pics/P01toP10/P07_004.png)

1. 显式构造 Tensorflow、MXNet
2. 隐式构造 PyTorch、MXNet

自动求导的两种模式

![](Pics/P01toP10/P07_005.png)

![](Pics/P01toP10/P07_006.png)

![](Pics/P01toP10/P07_007.png)

反向时会使用前向时的中间结果

![](Pics/P01toP10/P07_008.png)

内存复杂度使得深度神经网络会消耗大量GPU资源

### 自动求导代码实现

见Jupyter Notebook

### 自动求导QA

1. 在神经网络中计算梯度需要正向和反向，在自动求导中只用反向

2. PyTorch会默认累积梯度，减少内存消耗

3. 深度学习中，loss一般只会是向量

4. 获取grad前需要backward

    计算梯度很“贵”，所以不会自动backward

## 08 线性回归+基础优化算法

### 线性回归

![](Pics/P01toP10/P08_001.png)

![](Pics/P01toP10/P08_002.png)

![](Pics/P01toP10/P08_003.png)

![](Pics/P01toP10/P08_004.png)

![](Pics/P01toP10/P08_005.png)

二分之一方便求导

![](Pics/P01toP10/P08_006.png)

![](Pics/P01toP10/P08_007.png)

![](Pics/P01toP10/P08_008.png)

![](Pics/P01toP10/P08_009.png)

### 基础优化算法

当模型没有显式解的时候

![](Pics/P01toP10/P08_010.png)

![](Pics/P01toP10/P08_011.png)

学习率太大会震荡，太小计算梯度过于频繁浪费资源

![](Pics/P01toP10/P08_012.png)

b大的时候比较精确，但是时间复杂度也会增加

![](Pics/P01toP10/P08_013.png)

![](Pics/P01toP10/P08_014.png)

### 线性回归从0开始实现

见Jupyter Notebook

### 线性回归简洁实现

未学习

### QA

batchsize大，可能导致过拟合

batchsize小，重复多次可能会有更好的泛化性能，收敛性也会更好

使用iter可以不用一次生成所有的batch

<br>


## 09 Softmax回归+损失函数+图片分类数据集

### Softmax回归

虽然名字中带有“回归”，但实际上是一个分类问题

回归vs分类
1. 回归预测一个连续值
2. 分类预测一个离散类别

MNIST 手写数字识别（10类）

ImageNet 自然物体分类（1000类）

![](Pics/P01toP10/P09_001.png)

![](Pics/P01toP10/P09_002.png)

![](Pics/P01toP10/P09_003.png)

![](Pics/P01toP10/P09_004.png)

利用指数，使得所有都变为非负

![](Pics/P01toP10/P09_005.png)

对真实的那一类别求softmax并进行对数操作

![](Pics/P01toP10/P09_006.png)

### 损失函数

用于衡量预测值和真实值的区别

![](Pics/P01toP10/P09_007.png)

均方损失

二分之一是为了求导数方便

蓝色曲线：y=0，变化y'

绿色曲线：自然函数（高斯分布）

橙色曲线：损失函数梯度（过原点）

![](Pics/P01toP10/P09_008.png)

权重更新不会过大，同时0-1会有跃变，最后收敛可能会有问题

![](Pics/P01toP10/P09_009.png)

### 图片分类数据集

### Softmax回归从零开始实现

### Softmax回归简介实现

### QA

## 10 多层感知机

![](Pics/P01toP10/P10_001.png)

### 感知机

![](Pics/P01toP10/P10_002.png)

σ函数的输出未必是1和0

### 多层感知机

### 代码实现

### QA

