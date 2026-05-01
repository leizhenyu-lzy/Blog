# Paged-Attention

vLLM 提出的 显存管理方案

为了 解决 K**V Cache 中的 显存浪费问题**，因此也 **只用于 Inference 阶段**

传统 KV Cache 浪费原因
1. 预分配 + 内部碎片 (**浪费空间**)
   1. 虽然 对话结束会释放，但 **浪费发生在 生成的过程中**
   2. 大模型服务器特性 : 高并发 & 连续批处理
   3. 导致 显存占用率高，但是 实际利用率低
   4. **Internal Fragmentation** (内部碎片)
2. 外部碎片 (**空间不连续**)
   1. 不同用户的请求进出，即使空闲的地方加起来容量够，如果不是连续的一大块，也无法使用
   2. **External Fragmentation** (外部碎片)

Paged-Attention 解决方法
1. 引入 操作系统中 页表(Page Table) 的概念
2. Blocks 切块 : 不要求 显存连续分配，而是把显存切成一个个固定大小的 block
3. 动态分配 : 用多少拿多少，填满后再去系统找一块 空闲 block
4. **==逻辑连续，物理分散==** : 通过维护一个 Block Table(块映射表)，在底层计算 Attention 的时候，找到对应的 block 进行计算

Paged-Attention 优势
1. 消灭 外部碎片
2. 内部碎片 最多也只是一个 没填满的 block
3. 提高 **并发量**
4. 完美支持 Prefix Cache : 如果多个用户共享同一段 Prompt，不需要复制数据，只需把前缀的 Block 指针 共享

**模型推理框架** 负责管理 显存分配 & 释放
1. 相当于 GPU 的 操作系统，有 Allocator 等组件
2. 普通 CPU 内，链表 可以让 数据分散在内存各处
3. 但 GPU 内，传统的 Attention 算子(CUDA kernel) 要求 Tensor 在连续的 显存上
4. vLLM 团队 **重写 最底层的 Attention 数学计算算子**
   1. 让底层的算子 在做矩阵乘法时，能够 一边算，一边查 Block Table
