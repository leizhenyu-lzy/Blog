# 模式识别

## 00 传送门 

REMAIN

## 01 Introduction

### Introduction to Pattern Recognition

To assign an object or event to one of a number of categories, based on features derived to emphasize commonalities.

Pattern is a set of objects or phenomena or concepts where the elements of the set are similar to one another in certain ways/aspects.

### Pattern Recognition Systems

![](Pics/L01P001.png)

模式识别步骤
1. 预处理 Preprocessing
   1. reduce influence of noise
   2. restore the degraded data
   3. standardize the feature(数模转换、二进制编码、滤波、transformation)
2. 特征提取 Feature Extraction
   1. 好的特征选取会对识别准确性带来很大提升
3. 分类&决定 Classification and Decision
   1. classifier design:分类规则通过训练样本学习
   2. classification decision:用分类器对输入数据进行识别
   3. Issue of generalization.泛化性

### Pattern Classification Methods

1. Supervised Learning
   1. 两个阶段：training（工程师 learn） & recognizing（用户 use）
2. Unsupervised Learning
   1. 将数据进行聚类，寻找内在联系和结构
   2. 不同的聚类方法将得到不同的clusters

![](Pics/L01P002.png)

![](Pics/L01P003.png)

### Relative Mathematics Concepts

#### probability distribution

#### normal distribution

![](Pics/L01P004.png)

#### standard normal distribution

<br>
<br>

## 02 Bayesian Decision Theory

### Introduction

Thomas Bayes --- Bayes Theorem

A theory for how to make decision in the presence of uncertainty.

三个重要概念：
1. 先验概率：prior probability : $p(\omega_i)$，反映了实际物体没有出现之前，我们所拥有的对可能出现的物体的先验知识。
2. 类条件概率：class-conditional probability density : $p(x|\omega_i)$，类别为$\omega$时，x的概率密度。
3. 后验概率：posterior probability : $p(\omega_i|x)$，在观察到物体特征向量x后做出的决策。
4. 变量说明：x是物体的特征向量，$\omega$是所有可能的类别

贝叶斯公式：将先验概率转换为后验概率

$p(\omega_i|x)=\frac{p(x|\omega_i) \times(\omega_i)}{p(x)}$

$posterior=\frac{likelihood \times prior}{evidence}$

可能需要配合全概率公式一起使用

![](Pics/L02P001.png)

![](Pics/L02P002.png)

从比较简单的判决函数转用贝叶斯公式计算后验概率，再进行分类（对于当前观察到的x显然$p(x)$的值相同，与类别无关，约去）

![](Pics/L02P003.png)

特殊情况

![](Pics/L02P012.png)

按照贝叶斯公式计算后验概率后的错误分类概率

![](Pics/L02P004.png)

![](Pics/L02P005.png)

贝叶斯决策实际上就是用后验概率来进行决策

### Bayesian Decision Theory

![](Pics/L02P006.png)

$\lambda$的用途：**在某个类别下做出某种决策的风险/损失**，记得是选使得R尽量小的决策。

条件风险：出现某个特征向量的时候，做出某种决策的风险/损失。无论遇到何种情况的特征，我们都可以通过选择最小化条件风险的行为使得预期损失最小。

![](Pics/L02P007.png)

积分是在整个特征空间进行的。如果想要总风险最小，就是选用这样一个判决函数$a(x)$来指导我们进行行为的决策（选出进行哪个行为），使得$R(a_i(x)|x)$对每个x尽可能小。

贝叶斯决策提供了一个总风险的优化过程。最小化后的总风险被称为贝叶斯风险$R^*$，它是可获得的最优的结果。

**这里的$\lambda_{ij}=\lambda(a_i|\omega_j)$代表当实际类别为$\omega_j$被判为$\omega_i$的风险/损失。**

![](Pics/L02P008.png)

![](Pics/L02P009.png)

通常这两个系数都是正的，因为一般来说，一次错误判断造成的损失比正确判决的大。

进一步整理得到下图：

![](Pics/L02P010.png)

一步步推导回顾：

![](Pics/L02P011.png)

#### 特殊情况：0/1损失函数



### Discrimination Functions

### The Normal Distribution

### Test

损失函数未给出，按照0-1损失，用后验

损失函数给出，提到的按提到的算，没提到的损失默认为0

判别函数，贝叶斯判别函数

正态分布是的正态分布，三种，随后一种简单分析



<br>
<br>

## 03 Parameter Estimation

### Introduction

### Maximum-Likelihood Estimation

### Bayesian Estimation

### Test

贝叶斯参数估计了解一下

极大似然估计要掌握

<br>
<br>

## 04 Non-Parametric Estimation and Nearest-Neighbor Classification

### Introduction

大多数模式识别方法都假设密度函数的形式已知

Lazy Learning（Nonparametric Estimation）保留数据，想想KNN

Eager Learning（Parametric Estimation）根据数据学习出参数

非参数估计来源于非参数统计学

两种方法：直方图，近邻搜索



### Density Estimation

### Parzen Windows

### KNN Estimation

### The Nearest-Neighbor Rule

### Test

Parzen窗口和KNN估计要掌握

<br>
<br>

## 05 Linear Classification

### Portals


### Introduction

之前假设的是概率密度函数的参数形式已知，通过训练样本估计概率密度的参数值。

现在假定判别函数的参数形式已知，通过训练的方法来估计判别函数的参数值

![](Pics/L05P001.png)

线性判别函数相对容易计算

线性判别函数：x的各个分量的线性函数，或者是以x为自变量的某些函数的线性函数

**寻找线性判别函数转换为极小化准则函数的问题**

以分类为目的的准则函数可以是**样本风险、训练误差**

### Linear Discriminant Functions

![](Pics/L05P002.png)

**令g(x)=0**即得到用于分类的判定面（超平面）

![](Pics/L05P003.png)

超平面上每一点满足该等式，代入任意两点，可得到$W$与超平面上任意向量正交。

![](Pics/L05P004.png)

$x_p$是$x$在超平面$H$上的正交投影，易得$g(x_p)=0$

另外，$\frac{w_0}{||w||}$是原点到$H$的距离

#### 多类别情况

决策树

### Fisher Linear Discrimination

### Perceptron Criterion Function 感知器准则函数



### Minimum Error Classification

### Minimun Squared Error Procedures

### Nonlinear Discriminant Functions

### Test

概念、算法多

Fisher  感知器

最小错误分类、最小平方错误分类 计算较复杂

伪逆矩阵需要掌握

非线性判别函数 看懂例题即可

<br>
<br>

## 06 Feature Selection and Feature Extraction

### Portal

[同济小旭学长讲PCA](https://www.bilibili.com/video/BV1E5411E71z)

### Introduction

know what features to select? (PCA LDA ICA Transforms)

reduce misclassification error ---> better feature

特征种类
1. 统计特征
2. 时域特征
3. 几何特征
4. 光谱特征

Dimensionality Reduction 降维
1. 大多数learning方法对于高维数据效率低
2. 数据的本征维数可能很小（治病基因可能很短）
3. 特征特征是confusable的
4. 简化计算，简化特征空间结构（分界面结构简单）

特征抽取和特征选择是DimensionalityReduction（降维）的两种方法，针对于the curse of dimensionality(维灾难)，都可以达到降维的目的。但是这两个有所不同。

1. 特征抽取（Feature Extraction）:Creating a subset of new features by combinations of the existing features.也就是说，特征抽取后的新特征是原来特征的一个映射。

2. 特征选择（Feature Selection）:choosing a subset of all the features(the ones more informative)。也就是说，特征选择后的特征是原来特征的一个子集。

好的特征集合的条件：
1. 具有很大的识别信息量（很好的可分性）
2. 具有可靠性（模棱两可的似是而非的应该去掉）
3. 具有尽可能强的独立性（重复的、相关性强的不会增加更大分类信息）
4. 数量尽可能少，同时损失的信息量尽可能小（计算快）

### Class Separability Criterion 类别可分性准则

[特征提取 --武汉大学](https://www.bilibili.com/video/BV1U54y1i7dZ)

[特征提取 --国防科技大学](https://www.bilibili.com/video/BV144411D74h?p=34)

需要一个准则函数J(criterion function)，衡量不同特征及其组合的分类有效性，例如Minimum Error Rate(错误分类最小)

理想准则：某组特征使得分类器错误概率最小。但是，在实际应用中，直接使用是非常困难的，此时还没有训练分类器；对不同特征，训练的分类器也不同；也不能保证分类器在训练后是最理想的。

实际的类别可分性判据硬满足的条件（4个）：

![](Pics/L06P022.png)

可分性判据越大，误分率越小

i、j代表类，Jij>0说明可分

互相独立时，总贡献是每一个特征的贡献，具有可加性

加入新特征，提高可分性（至少不降低）

**不是所有可分性判据都能满足所有上述条件，选取最重要的**

#### Based on Distance 距离度量

![](Pics/L06P023.png)

直接基于样本，不涉及分类器，所以应用广泛

##### 距离函数

![](Pics/L06P024.png)

![](Pics/L06P025.png)

#### 准则函数

![](Pics/L06P026.png)

tr是迹，即方阵的主对角线元素的总和

Sw：within-class scatter matrix 类内散度矩阵 越小越好

Sb：between-class scatter matrix 类间散度矩阵 越大越好

#### 特征提取步骤

![](Pics/L06P027.png)

![](Pics/L06P028.png)

#### Based on Probability 概率分布



#### Base on Entropy Function 熵函数



### Feature Extraction

![](Pics/L06P020.png)

是对于原来特征的一个低维**映射**，凝练出**新特征**

![](Pics/L06P021.png)

based on distance

based on probability distance



#### PCA 主成分分析

用于数据降维

![](Pics/L06P001.png)

省去某些维度信息

![](Pics/L06P002.png)

目标：将数据投影到新坐标系，使得信息保留最多

评判标准：使得数据分布尽量分散（方差大），作为主成分（坐标系）

保存信息：
1. 新坐标系原点
2. 新坐标系角度
3. 新坐标点

操作步骤：
1. 去中心化，将坐标原点放在数据中心
2. 找新的坐标系，找到投影后方差最大的方向（因为去中心化，所以所有数据点到原点的距离为常数。由勾股定理，当点到投影平面的距离最短时，投影点到原点的距离平方最大，也就是方差最大。因为到投影平面的距离短，所以保留了数据信息）

数据变换
1. 数据线性变换

    ![](Pics/L06P003.png)

2. 数据旋转变换

    ![](Pics/L06P004.png)

白数据$D$，x与y不相关，且都符合标准正态分布。通过先拉伸后旋转变化得到$D'$，此时x与y相关

![](Pics/L06P005.png)

![](Pics/L06P006.png)

现在我们已有的数据是$D'$，希望通过操作将已有数据还原成白数据

![](Pics/L06P007.png)

问题转化为求R？

**协方差矩阵的单位特征向量就是R，特征值就是新数据的方差**

![](Pics/L06P008.png)

对本例$\bar{x}、\bar{y}$均为0，因为已经进行区中心化

![](Pics/L06P009.png)

![](Pics/L06P010.png)

![](Pics/L06P011.png)

![](Pics/L06P01201.png)

这里体现出了，协方差矩阵的特征向量拼接起来就是R。L其实就是特征值组成的向量

![](Pics/L06P01202.png)

![](Pics/L06P013.png)

![](Pics/L06P014.png)

选取几个最大特征值对应的特征向量，将数据**左乘**以这些特征向量所合成的矩阵的**转置**即进行了映射（投影）。

![](Pics/L06P015.png)

![](Pics/L06P016.png)

outsider将会对求解结果造成很大影响

![](Pics/L06P017.png)


#### PCA步骤

先对数据进行去中心化

求得协方差矩阵

先求出协方差矩阵的特征值，再求得对应的特征向量

较大的特征值所对应的特征向量就是投影的方向

对于高维数据，可能需要选取较多的特征向量，并合成矩阵转置后再右乘数据，进行降维

![](Pics/L06P029.png)

### Feature Selection

![](Pics/L06P018.png)

**从原始特征中选择**有代表性、分类性的特征，Dnew < Dorigin

![](Pics/L06P019.png)

#### 特征选择方法

![](Pics/L06P030.png)

1. 最优的 optimal
   1. exhaustive search 穷举搜索
   2. branch and bound search 分支限界搜索
2. 次优的 suboptimal
   1. Sequential Forward Search(SFS) 序列前向选择
   2. Sequential Backward Search(SBS) 序列后向选择
   3. Plus 1 take away r
   4. Sequential Forward Floating Search(SFFS)
   5. Sequential Backward Floating Search(SBFS)
   6. Best Individual Features

<br>

穷举搜索会生成每一个可能的解，保证了最优性，所以效率低。

分支界定法，搜索状态空间树，可以通过bound进行剪枝。并且有两个模块：
1. 一个用于在搜索解空间时生成分支
2. 另一个生成bound，即时剪断一些分支

<br>

SFS：特征子集X从空集开始，每次选择一个特征x加入特征子集X，使得特征函数J(X)最优。简单说就是，每次都选择一个使得评价函数的取值达到最优的特征加入，其实就是一种简单的贪心算法。

SBS：从特征全集O开始，每次从特征集O中剔除一个特征x，使得剔除特征x后评价函数值达到最优。序列后向选择与序列前向选择正好相反，它的缺点是特征只能去除不能加入。

SFS与SBS都属于贪心算法，容易陷入局部最优值。



<br>
<br>

### Test

类的可分离性

PCA 协方差矩阵

准则函数，题目会告诉选取哪一个

模拟退火和遗传算法不考

## 07 Unsupervised Learning and Clustering

### Portal

[K-means Blog](https://zhuanlan.zhihu.com/p/78798251)

[物以类聚的Kmeans](https://www.bilibili.com/video/BV1ei4y1V7hX)

[什么是K-Means](https://www.bilibili.com/video/BV1mf4y1k7UC)

### Introduction

Supervised(Labeled Data)

Unsupervised(Unlabeled Data)

目标：
1. Find the class label
2. Find the number of classes directly from data

评价指标：
1. high **intra-class** similarity:cohesive within clusters
   
   高类间相似：**聚类内**的凝聚力

2. low **inter-class** similarity:distinctive berween clusters
   
   低类阶级相似：**聚类间**的独特性

    ![](Pics/L07P001.png)

**聚类是主观的**

**类的概念是模棱两可的**（可以有很多的聚类的方法，聚成不同的类）

聚类算法
1. 基于邻接度 contiguity
2. 基于密度 density
3. 基于欧式密度 Euclidean density



Definition Distance Measures

distance(dissimilarity)

![](Pics/L07P002.png)

1. 欧氏距离
   
   ![](Pics/L07P003.png)

2. 三角距离
   
   ![](Pics/L07P004.png)



应用
1. 图像处理
   1. 图片分组
   2. Image Segmentation
2. 网页
   1. 用户分类
3. 信息生物学
   1. 蛋白质聚类


### Probability Model-Based Clustering

对于每个区域，概率密度都是单峰的(unimodal distribution)

REMAIN

### Dynamic Clustering

基本方法
1. K-means
2. K-medoids
3. Fuzzy c-means
4. ISODATA

#### K-means算法

无监督聚类算法

K代表类别数 cluster number

不断迭代的算法

收敛到一个局部最小值

![](Pics/L07P005.png)

Ck指的是每一个类别的中心

![](Pics/L07P006.png)

算法步骤：

1. （随机）选择K个值，作为聚类的初始中心

2. 对任意一个样本点，求其到K个聚类中心的距离，将样本点**归类到距离最小的中心的聚类**，如此迭代n次
   
   ![](Pics/L07P007.png)

3. 每次迭代过程中，利用均值等方法**更新各个聚类的中心点(质心)**，假定找到的成员都是正确的

4. 对K个聚类中心，利用2,3步迭代更新后，如果位置点变化很小(可以设置阈值)，则认为达到稳定状态，迭代结束，对不同的聚类块和聚类中心可选择不同的颜色标注

优点：
1. 原理比较简单，实现也是很容易，收敛速度快(not always) 
2. 聚类效果较优。 
3. 算法的可解释度比较强。 
4. 主要需要调参的参数仅仅是簇数k。

问题：
1. 不同的初始中心点导致不同的聚类结果
   1. 不使用随机，采用某些方法（选择距离聚类中心最远的点）
   2. 解决方法：K-means++……
2. 不同K的选择导致不同结果
   1. 随着K增加，J(D)单调减小
   2. 解决方法：手肘法、GapStatistic……
      ![](Pics/L07P009.png)

缺点：
1. 需要预先设定K
2. 初始点的选择对结果影响大
3. 对于非凸的数据集比较难收敛 
4. 如果各隐含类别的数据不平衡，比如各隐含类别的数据量严重失衡，或者各隐含类别的方差不同，则聚类效果不佳。
5.  最终结果和初始点的选择有关，容易陷入局部最优
6.  对噪音（noisy）和异常点（离群点outlier）比较的敏感

### Hierarchical Clustering 分层聚类

![](Pics/L07P010.png)

hierarchical cluster
1. 基于欧氏距离
   1. agglomerative 聚合的
   2. divisive 分裂的
2. 基于概率

#### hierarchical cluster Ⅰ

partition data set sequentially

tree of clusters

![](Pics/L07P011.png)

![](Pics/L07P012.png)

##### Distance Measure
1. singe link
   两个聚类中最接近的两个元素之间的距离

   ![](Pics/L07P013.png)

2. complete link
   两个聚类中最远的两个元素之间的距离

   ![](Pics/L07P014.png)

3. average link
   两个聚类中任意的两个点之间的距离的平均值

   ![](Pics/L07P015.png)

不同link的不同聚类结果

![](Pics/L07P016.png)

##### agglomerative聚类步骤

![](Pics/L07P020.png)

##### 例子

![](Pics/L07P017.png)

![](Pics/L07P018.png)

一遍遍的刷新矩阵，矩阵逐渐变小。直到最后2×2矩阵，不用写成1×1

![](Pics/L07P019.png)

汇合点所标记的只就是更新矩阵时找到的非零最小值

##### 相关问题

dendrogram n.系统树图

![](Pics/L07P021.png)

知道分为几类，就知道最终结果

选择最长的lifetime，某次合并的Δ最大，表示将两个不同的类进行合并

#### hierarchical cluster Ⅱ

暂无

#### 总结

![](Pics/L07P022.png)

<br>
<br>

### Test

K均值

分层聚类

答题规范

## 08



### Test

三个网络
