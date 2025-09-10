# MoCo : Momentum Contrast for Unsupervised Visual Representation Learning

[MoCo - Github](https://github.com/facebookresearch/moco)

[MoCo 论文逐段精读 - B站(bryanyzhu)](https://www.bilibili.com/video/BV1C3411s7t9/) - In Progress

动量对比学习，无监督

InfoNCE = Information Noise Contrastive Estimation

---

# Background

不需要 知道具体标签信息，但需要 知道哪些样本类似/不类似

通过设计 **代理任务(Proxy Task) / 前置任务(Pretext Task)**，人为的定义规则，规则 表明 哪些图片相似/不相似 (简介提供监督信号)
1. 图像
   1. Rotation Prediction - 让模型预测旋转角度
   2. Jigsaw Puzzle(拼图游戏) - 将图像分成9块，随机打乱，让模型预测正确的排列
   3. Colorization - 输入灰度图像，预测彩色版本
   4. Inpainting(补全) - 遮挡图像部分区域，让模型预测被遮挡内容
2. 文本
   1. MLM(掩码语言模型) - 遮挡部分词汇，预测被遮挡的词(BERT使用的代理任务)
   2. NSP(下一句预测) - 判断两个句子是否连续
3. 对比学习
   1. Instance Discrimination(个体判别，每张图片自成一类) - 将同一图像 通过 Transformation 得到 不同增强版本 作为正样本，不同图像作为负样本
   2. Clustering Assignment(聚类分配) - 将相似样本分配到同一聚类

Linear Protocol - 将预训练好的骨干模型冻结(backbone freeze)，当做特征提取器，只训练一个线性分类器来评估学到的表示质量



# MoCo

Momentum 加权移动平均，$y_t = m · y_{t - 1} + (1 - m) · x_t$
1. $m$ : 动量系数，越大越平滑
2. $y_t$ : 累计值
3. $x_t$ : 当前输入

将 对比学习 看作 字典查询 任务

区别
1. NLP 任务，raw信号空间 离散，容易构建 tokenize 字典
2. CV  任务，raw信号空间 连续 & 高维，难以构建字典

如何理解 字典
1. 数据集有 n 个样本
2. 某样本经过不同 Transformation 得到 正样本 pair : anchor(锚点) & positive
3. 其他样本 作为 negative 样本
4. 样本通过 Encoder 得到特征输出
   1. anchor ($x_q$) : 使用 encoder 1，得到 **query** ($q$)
   2. positive/negative ($x_k$) : 都使用 encoder 2，得到 **keys** ($k_i$)
   3. 两个 encoder 可以是 相同模型 也可以是 不同模型
5. 希望 query，和 positive 对应的 key 相近，和 negative 对应的 key 远离

对于 dynamic dictionary 的要求
1. large      : 更好、更连续的 抽样，视觉特征 越丰富，防止学到捷径，影响泛化性
2. consistent : 使用 相似的 encoder 得到，保证一致性，对应 **momentum encoder**

**queue** : 解耦 queue大小 & mini-batch大小，可以使用比较标准的 mini-batch size (128 / 256)，可以使用很大的字典(尺寸是 超参)

**momentum encoder** : 保证 key 的 一致性

Supervised & UnSupervised 区别就在于 pretext task & loss function
1. UnSupervised 缺少 标签
2. 通过 Pretext Task 生成 标签
3. 有了标签 就可以 配合 目标函数

MoCo 使用的 Pretext Task : instance discrimination task

Loss Function
1. 生成式 : 重建，fixed target
2. 判别式 : 选择题，fixed target
3. 对比式 : target 在训练中不断变化，由网络的 数据表示(网络算出的 特征向量，原始数据映射到 特征空间) 定义
4. 对抗式 : probability distribution 的差异

InfoNCE (Noise Contrastive Estimation)
1. 引入
   1. Softmax : $$\frac{\exp(z_+)}{\sum^K_{i=0} \exp(z_i)}$$
   2. Cross Entropy : 在 one-hot 的时候和 Softmax 是 $-\log$ 关系，$-\log \text{正确类别 Softmax 分数}$
   3. 在 Supervised 中，**K 表示 类别数**
2. 对比学习可以用该公式，但是实际上 对于例如 instance discrimination 任务，每个样本都是一个类别，K 将会非常大，计算复杂度高
3. NCE : 将问题简化为 二分类(data/noise Sample)，每次用数据样本和噪声样本对比，不是对整个数据集 算Loss，而是选取几个负样本 估计/近似
   1. 样本少 : 快 & 偏
   2. 样本多 : 慢 & 准
4. InfoNCE : NCE 的 二分类 变为 多分类
   1. $$\mathcal{L}_q = - \log \frac{\exp(q \cdot k_+ / \tau)}{\sum_{i=0}^K \exp(q \cdot k_i / \tau)}$$
   2. $\tau$ 是 温度超参数，控制分布形状，越大越平缓，越小越集中
   3. **K 表示 负样本数量**


用 Queue 表示 字典，元素就是 Key，每个 mini-batch，new key 被传入，
old key 被传出




