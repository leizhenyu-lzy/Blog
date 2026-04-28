# DETR : End-to-End Object Detection with Transformers

[DETR - Meta Blog](https://ai.meta.com/blog/end-to-end-object-detection-with-transformers/)

[DETR - Github](https://github.com/facebookresearch/detr)

---

DETR : Detection Transformer

一般 object detection 需要 NMS(Non-Maximum Suppression) 后处理，DETR 不需要

将 **object detection 问题**(锚框 + 类别) 转化为 **集合预测问题**(set prediction)

end2end 无需 surrogate problems

DETR 步骤
1. CNN : 特征提取
2. Transformer Encoder : 学习 全局特征
3. Transformer Decoder : 生成 预测框
4. Bipartite Matching Loss : 预测框 & GroundTruth框 匹配 + Loss
   1. Training 需要，Inference 不需要，直接用 threshold 卡 置信度



Object Detection 指标
1. AP (average **precision**，准确率) : $\frac{TP}{TP + FP}$
2. AR (average **recall**，召回率) : $\frac{TP}{TP + FN}$
3. **Confusion Matrix** (True/False 衡量 预测是对还是错，Pos/Neg 是 模型的预测结果)
   1. True  Positive : 真正例
   2. False Positive : 假正例
   3. True  Negative : 真负例
   4. False Negative : 假负例
4. IOU (Intersection over Union，交并比)
5. 物体大小 (根据 像素面积 判断)
   1. small  : $\text{size} \lt 32^2$
   2. middle : $32^2 \le \text{size} \le 96^2$
   3. large  : $\text{size} \gt 96^2$


对比 Faster R-CNN，在 big object 上表现较好，在 small object 表现较差


training setting 不同与 常规 目标检测，需要 更长的训练时间




**bipartite matching loss** / Hungarian Loss(匈牙利损失)
1. DETR 输出 固定数量的预测集合
2. 解决 哪个 预测框 对应 哪个 GroundTruth框
3. 步骤
   1. 寻找 **最优匹配**(1 to 1) Bipartite Matching(二分图匹配)
      1. 在 预测集 & 真实集 间，寻找一个 具有最小匹配代价 (Matching Cost) 的 **全局最优排列组合**(Permutation)
      2. **匈牙利算法**
         1. prediction框 & GroundTruth框 构成 **cost matrix**
         2. **相对零代价** : 在 cost matrix 的 某一行/某一列 加减 同一个常数，最优分配方案是不变的
         3. `scipy.optimize.linear_sum_assignment`
            1. 不需要必须是 N*N 方阵，不够的用 no object 把 GroundTruth 补齐
      3. **匈牙利算法 不需要梯度传导**，只是用于 匹配
      4. 落选框 只计算 分类 loss，不计算 box loss(指示函数 $\mathbb{1}_{\{c_i \neq \varnothing\}}$)，惩罚是 background 却 预测为 高置信度类别的框
   2. 计算损失 Loss Computation (Hungarian Loss)

Visualization
1. encoder (fig 3): 全局特征 区分物体
2. decoder (fig 6): 细化外围点
   1. 对于 object detection，最关键的是 找到物体的 上下左右边缘极限位置 (偷懒)

注意力图 天然 就是 关于物体的 大致热力图(分辨率很低)
1. 绘制 注意力权重(Attention Weights)，reshape 和 positional encoding 的 维度一致

object query 类似于 不同关注点(问不同方向的问题)

Deformable-DETR
