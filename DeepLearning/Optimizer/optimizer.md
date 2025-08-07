# Optimizer 优化器

[torch.optim - PyTorch Docs](https://docs.pytorch.org/docs/stable/optim.html#algorithms)

[LRScheduler - PyTorch Docs](https://docs.pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate)


https://www.bilibili.com/video/BV1NZ421s75D

[](https://www.bilibili.com/video/BV1NC4y1g716)

[](https://www.bilibili.com/video/BV1e94y1N7u5)

[](https://www.bilibili.com/video/BV1Nc411m7FL)

https://www.bilibili.com/video/BV1Ri421h7qV

https://www.bilibili.com/video/BV1Wt421b7uA

https://www.bilibili.com/video/BV1jH2RYgEDN

https://www.bilibili.com/video/BV1jh4y1q7ua



创建时，scheduler 保存了 optimizer 的引用，调用 scheduler.step() 时，scheduler 会直接修改 optimizer 的学习率

patience 机制 : 连续 patience 个 epoch 的 loss 没有下降 才触发

理解
1. 前期：大学习率快速收敛
2. 中期：发现卡住了(plateau)，说明步子太大
3. 后期：小学习率精确收敛到最优解




Adam

AdamW
1. Adam 的 改进版本，有更好的 权重衰减 机制
2. scheduler
   1. name      :
   2. factor    :
   3. patience  :
   4. mode      :
   5. min_lr    :

`from torch.optim import Adam, AdamW`

`from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts, ReduceLROnPlateau, _LRScheduler, ConstantLR`




scheduler : 学习率调度器
1. 基于步数
2. 基于性能
   1. `ReduceLROnPlateau`
3. 周期性
4. 预热相关
5. 自适应



