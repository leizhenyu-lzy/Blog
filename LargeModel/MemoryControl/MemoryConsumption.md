# Memory Consumption - 显存占用

**Activations 激活值** : 任何 在 前向传播(Forward Pass) 中产生，并且为 在 反向传播(Backward Pass) 中计算梯度，而被框架保存在显存里的 **中间张量**


# Train - 训练阶段

**无 KV Cache**

组成部分
1. Model Weights
   1. 存一份权重用来 前向 & 反向 传播
2. Gradients 梯度
   1. 反向传播时，梯度矩阵 和 权重矩阵 形状相同
3. Optimizer State 优化器状态
   1. AdamW 优化器 记录每个参数的历史动量，为 每个参数 维护 Momentum(一阶动量) & Variance(二阶动量)，而且可能以高精度存储
4. Activations 激活值
   1. 反向传播梯度时，会用到中间结果
   2. 工程解法 : 激活重计算(时间换空间)，反向传播需要用到的时候，我再临时重新做一次前向计算
5. 其他
   1. Dropout Mask : 反向传播时，模型必须知道 前向传播时 丢弃了哪些位置(PyTorch 保存一个 和 输出一样大的二进制 Mask 矩阵)
   2. LayerNorm Mean & Variance
   3. 激活函数输入 : SwiGLU、GELU 等函数，求导时需要知道当初的输入矩阵

常规训练(如果有 激活重计算) : 优化器 占比大

长文本训练 : Activations 占比大



# Inference - 推理阶段

组成部分
1. Model Weights
2. KV Cache
3. Activations 激活值
   1. 瞬时的，算完传播下去后，可以释放，但需要保证能塞下 最大的中间矩阵 进行计算


常规场景(短对话、并发低) : 模型权重 占比大

企业级场景(长文本、高并发) : KV Cache 占比大




