# 模式识别

## 00 Pre

## 01 Introduction

## 02 Bayesian


## 03 Parameter Estimation



## 04 Non Parametric


## 05 Linear Classification


## 06 Feature Extraction

### PCA 主成分分析

[同济小旭学长讲PCA](https://www.bilibili.com/video/BV1E5411E71z)

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
2. 找坐标系，找到方差最大的方向

数据变换
1. 数据线性变换

    ![](Pics/L06P003.png)

2. 数据旋转变换

    ![](Pics/L06P004.png)

![](Pics/L06P005.png)

![](Pics/L06P006.png)

![](Pics/L06P007.png)

问题转化为求R？

协方差矩阵的特征向量就是R

![](Pics/L06P008.png)

对本例$\bar{x}、\bar{y}$均为0

![](Pics/L06P009.png)

![](Pics/L06P010.png)

![](Pics/L06P011.png)

![](Pics/L06P012.png)

![](Pics/L06P013.png)

![](Pics/L06P014.png)

![](Pics/L06P015.png)

![](Pics/L06P016.png)

outsider将会对求解结果造成很大影响

![](Pics/L06P017.png)



## 07 Unsupervised Clustering



