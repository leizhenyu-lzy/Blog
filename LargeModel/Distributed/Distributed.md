# Accelerate

`accelerate config` 多gpu分布式训练
1. Hugging Face Accelerate 工具包提供的一条交互式 CLI 命令，用来 生成/修改 分布式训练的配置文件
2. 核心作用
   1. 收集当前的硬件与分布式环境信息
      1. GPU 数量、CPU 线程数、是否跨节点
      2. 后端通信库 (nccl / gloo / mpi)
      3. 是否启用 fp16/bf16、梯度累积、梯度检查点等高级特性
      4. 是否使用 DeepSpeed、FSDP、DDP 等并行策略
   2. 写入 yaml 文件
   3. 不用每次手工拼一长串分布式参数


# 分布式训练方案



## **DDP (Distributed Data Parallel)** - PyTorch 官方

[Distributed Data Parallel in PyTorch Tutorial Series - YouTube](https://www.youtube.com/playlist?list=PL_lsbAsL_o2CSuhUhJIiW0IkdT5C2wGWj)

核心 : **数据并行**
1. 每张 GPU 保存一份完整模型参数
2. 每个 rank(GPU 进程) 拿到不同的 mini-batch 切片，独立 前向 + 反向
3. 反向时广播 / All-Reduce 把各 GPU 的梯度求平均，再同步更新参数

优
1. 接口最原生(torch.nn.parallel.DistributedDataParallel)
2. 对网络结构要求低，兼容性最好

劣
1. 每卡都要存整份模型 → 模型越大，显存越吃紧

## **FSDP (Fully Sharded Data Parallel)** - PyTorch 官方

[Getting Started with Fully Sharded Data Parallel (FSDP2) - PyTorch Docs](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)

FSDP1 已经 deprecated，现在是

比 DDP 新

torch.distributed.fsdp

核心 : 参数 + 优化器状态 全切片
1. 把每个权重矩阵按 GPU 数量切块，只在需要时聚合到当前 GPU，计算完再切片回去
2. 反向后各 GPU 只保留自己那 1/N 的 参数 及 优化器状态，显存占用 ≈ DDP 的 1/N
3. 也支持 ZeRO-3 式的梯度 sharding、混合精度、CPU offload 等

优
1. 在 PyTorch 原生生态内完成，无需接第三方库
2. API 与 DDP 类似，迁移成本相对可控

劣
1. 复杂度比 DDP 高，需要正确 wrap 模型(按层级拆分)、调更多参数
2. 对通信带宽敏感，在 低速网络 或 单机多卡 PCIe 较慢时 加速不明显


## **DeepSpeed** - 微软开源库(GitHub microsoft/DeepSpeed)

核心 : **一站式大模型训练与推理加速套件**
1. 包含 ZeRO-1/2/3 参数、梯度、优化器 sharding (与 FSDP 类似但更早提出)
2. 支持 ZeRO-Infinity (显存 + CPU + NVMe 多级 offload)
3. 内置混合精度(fp16/bf16)、梯度累计、显存池化、Flash-Attention、inference engine
4. 可以与 HuggingFace Transformers、Megatron-LM 等无缝集成

优
1. 功能最丰富，针对 百亿-万亿 参数模型 有成熟解决方案
2. 涵盖 训练 & 推理，不只是分布式策略
3. 社区示例多、生态围绕大模型活跃

劣
1. 依赖外部库(pip install deepspeed)，与 PyTorch 主干的 API 不完全一致
2. 配置文件 YAML 较多、调参曲线陡峭，初学者需要花时间理解 ZeRO 各级别
3. 某些最新 PyTorch 特性(FSDP 自带) 需等待适配
