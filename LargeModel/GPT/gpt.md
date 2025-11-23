# GPT (Generative Pre-Training)


[大模型修炼之道(二): GPT系列GPT1，GPT2，GPT3，GPT4 - B站视频(RethinkFun)](https://www.bilibili.com/video/BV1ZJ4m1K73s)

**==GPT1==** : Improving Language Understanding by Generative Pre-Training
1. 动机
   1. NLP 每个任务都 需要大量标注数据，模型 不能 复用(运用到其他任务)
   2. CV 领域得益于 ImageNet 数据集，可以 预训练 模型，下游 子任务 微调
   3. OPENAI 要做 NLP 领域的 预训练模型
2. 难点
   1. 没有像 ImageNet 那样大量的标注数据
   2. 模型架构如何设计，方便轻微修改，来应用到下游任务
3. 没有标注数据 -> 使用 语言模型 自回归方式 训练模型 (给文本，预测下一个词)
4. 架构选择 -> RNN / Transformer (更好 记住 训练数据中的 模式)
5. 模型结构
   1. Decoder Only




**==BERT==** : Pre-training of Deep Bidirectional Transformers for Language Understanding

**==GPT2==** : Language Models are Unsupervised Multitask Learners

**==GPT3==** : Language Models are Few-Shot Learners

**==GPT4==** : Technical Report


