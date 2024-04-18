# 混淆矩阵 & F1-score

## Portals

[小萌五分钟 Confusion Matrix](https://www.bilibili.com/video/BV1oz4y1R71a)

[小萌五分钟 F1值](https://www.bilibili.com/video/BV1vt4y117Zz)

## 混淆矩阵 Confusion Matrix

T/F表示的是预测的正确与否，positive/negative表示的是分类器给出的分类

TP : true positive  预测是正确的正样本
FP : false positive 预测是错误的正样本
TN : true negative  预测是正确的负样本
FP : false positive 预测是错误的负样本

![](pics/confusionmat000.png)

![](pics/confusionmat001.png)

![](pics/confusionmat002.png)

希望绿色的数值大，橙色的数值小，这样模型效果好。

## F1-score

![](pics/f1score.jpg)

![](pics/f1_score000.png)

![](pics/f1_score001.png)

准确率Accuracy：说明分类器正确分类的比例。

精确率Precision：可以判断出有多少其他类被分到自己这一类(被我们的算法选为positive的数据中，有多少真的是positive的？)

召回率Recall：可以判断出有多少自己这一类被分到其他类(实际应该为Positive的数据中，多少被我们选为了Positive？)

$F_1=\frac{2}{\frac{1}{Precision}+\frac{1}{Recall}}$

F1_score是Precision和Recall的调和平均值

$F_\beta=(1+\beta^2)\times \frac{Precision·Recall}{\beta^2·Precision+Recall}$

Recall的重要性是Precision的$\beta$倍

![](pics/f1_score003.png)

![](pics/f1_score004.png)

![](pics/f1_score002.png)



F1-score越大自然说明模型质量更高。但是还要考虑模型的泛化能力，F1-score过高但不能造成过拟合，影响模型的泛化能力。

