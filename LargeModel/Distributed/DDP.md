# Distributed Data Parallel (DDP)

[Distributed Data Parallel in PyTorch Tutorial Series - YouTube](https://www.youtube.com/playlist?list=PL_lsbAsL_o2CSuhUhJIiW0IkdT5C2wGWj)

DDP 工作流程
1. 当 training job 被分配给多个 GPU，DDP 为每个 GPU 启动一个进程
2. 每个 进程中有 一样的 模型 & optimizer 本地副本(local copy)
   1. 相同 模型初始参数
   2. 相同 优化器随机种子
3. 改变的是数据，从 DataLoader 获取 input batch，使用 `DistributedSampler`，确保每个进程接收不同输入
4. 每个进行 使用不同的 batch 数据，独立进行 forward & backward，**先不让 optimizer 进行参数优化**(否则会得到不同的模型)
5. DDP 启动 sync 步骤，使用 Ring All-Reduce 算法



[Ring All-Reduce -  个人笔记](./NCCL.md#ring-all-reduce)


DDP 创新点
1. 与 Autograd 集成 (Gradients Hook)
   1. DDP 模块在模型参数上注册了钩子函数 (Autograd Hooks)
   2. 反向传播过程中，当参数的梯度刚刚计算完成时，这个钩子就会被触发
   3. 一旦钩子触发，DDP 不会等待整个反向传播完成，而是立即将该参数所属的 梯度桶(Bucket) 投入到 通信后端(NCCL) 开始 All-Reduce
2. 通信 & 计算 重叠 (Overlap)
   1. DDP 提高效率的关键
   2. NCCL 在后台进行 All-Reduce 通信时，GPU 同时继续计算模型中更靠前的层 的梯度
   3. 通过这种流水线操作，提高了 GPU 的利用率 & 整体训练吞吐量

