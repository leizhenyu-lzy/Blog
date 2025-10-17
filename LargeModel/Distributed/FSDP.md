# Fully Sharded Data Parallel (FSDP)

[Getting Started with Fully Sharded Data Parallel (FSDP2) - PyTorch Docs](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

FSDP & DDP
1. DDP  思路 : 切分数据，复制 完整模型(参数、梯度、优化器状态)
   1. 内存冗余 : N个 模型副本
   2. 显存需求 : N × ModelSize
   3. 通信内容 : 完整 梯度(backward)
   4. 解决问题 : 加速训练
2. FSDP 思路 : 切分数据，同时将 模型(参数、梯度、优化器状态) 也完全切分(分片)，达到极高的显存效率
   1. 内存冗余 : 1个 模型分片
   2. 显存需求 : 1 × ModelSize
   3. 通信内容 : 参数分片(forward) 和 梯度分片(backward)
   4. 解决问题 : 装下巨型模型
3. 场景
   1. 模型尺寸小到中等
      1. DDP 是更优的选择，前向传播时无需进行任何通信，只在反向传播结束时进行一次 All-Reduce 来同步梯度
      2. FSDP 反而会引入额外的、不必要的通信开销，在 前向传播 和 反向传播 的每层计算之前，执行一次 All-Gather 操作，将该层所需的参数分片收集完整
   2. 模型尺寸巨大
      1. 必须使用 FSDP，虽然通信开销大，但它是唯一能将模型装进内存的方案


All-Reduce = Reduce-Scatter + All-Gather
<img src="Pics/dist004.png" width=600>

<img src="Pics/dist005.png">

<img src="Pics/dist006.png">



