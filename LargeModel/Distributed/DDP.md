# Distributed Data Parallel (DDP)

[Distributed Data Parallel in PyTorch Tutorial Series - YouTube](https://www.youtube.com/playlist?list=PL_lsbAsL_o2CSuhUhJIiW0IkdT5C2wGWj)

[Ring All-Reduce -  个人笔记](./NCCL.md#ring-all-reduce)


DDP 工作流程
1. 当 training job 被分配给多个 GPU，DDP 为每个 GPU 启动一个进程
2. 每个 进程中有 一样的 模型 & optimizer 本地副本(local copy)
   1. 相同 模型 初始参数
   2. 相同 优化器 随机种子
3. **改变数据**，从 DataLoader 获取 input batch，使用 `DistributedSampler`，确保每个进程接收不同输入
4. 每个进行 使用不同的 batch 数据，独立进行 forward & backward，**先不让 optimizer 进行参数优化**，否则会得到不同的模型
5. DDP 启动 Synchronization 步骤，使用 **Ring All-Reduce**(Reduce-Scatter + All-Gather) 算法
   1. Ring All-Reduce 算法 本身 不是逐层的
   2. PyTorch 的 DDP 将模型的所有梯度参数 划分成几个较大的 桶Bucket，而不是对每一个微小的参数都进行一次 All-Reduce (少量大规模通信 代替 大量小规模通信)
   3. DDP 监听 : DDP 在每个参数上设置了钩子，当某一层的梯度计算完成时，这个梯度就被放入 所属的 桶中，一旦一个桶内所有的梯度都已就绪，DDP 会 立即 & 异步 启动对这个桶的 Ring All-Reduce
   4. 逐桶 触发机制，使得梯度计算和通信可以同时进行
6. 此时 每个 模型 copy 都有相同的 gradient 梯度，各自运行优化器 进行 参数更新 就得到相同的更新参数，保持同步，可以进行下一次迭代


概念
1. node  : 类似 物理 server/machine
2. rank  : process 的 全局 唯一 ID (进程间需要通信)，还有 local rank (单个 node 内的 唯一 ID)
3. world : 类似一个 Group，world 内的 process(GPU) 可以彼此通信


DDP 整体是 去中心化的，**master 仅用于 初始化 & 协调**，`init_process_group` 时，系统需要一个临时的、单一的协调点 (master)
1. master 不是在训练中承担 通信 或 计算 任务
2. master 在启动阶段完成 集中式 协调任务
   1. 发现机制 (Rendezvous)
      1. 所有 rank 进程 需要知道彼此的存在，形成 **进程组**
      2. 所有其他 rank 在启动时都会连接到这个 master 地址(ADDR & PORT)
   2. 状态同步 (仅在初始化时) : 模型初始化广播，数据下载协调


DDP 创新点
1. 与 Autograd 集成 (Gradients Hook)
   1. DDP 模块在模型参数上注册了钩子函数 (Autograd Hooks)
   2. 反向传播过程中，当参数的梯度刚刚计算完成时，这个钩子就会被触发
   3. 一旦钩子触发，DDP 不会等待整个反向传播完成，而是立即将该参数所属的 梯度桶(Bucket) 投入到 通信后端(NCCL) 开始 All-Reduce
2. 通信 & 计算 重叠 (Overlap)
   1. DDP 提高效率的关键
   2. NCCL 在后台进行 All-Reduce 通信时，GPU 同时继续计算模型中更靠前的层 的梯度
   3. 通过这种流水线操作，提高了 GPU 的利用率 & 整体训练吞吐量


---


# Distributed Data Parallel Video Tutorials

[Distributed Data Parallel Video Tutorials - PyTorch](https://docs.pytorch.org/tutorials/beginner/ddp_series_intro.html)

## Single-Node Multi-GPU Training (`mp.spawn`)

**import DDP 相关的 额外模块**

```python
# PyTorch 对 Python 标准库 multiprocessing 的 封装 & 扩展，用于在单台机器上启动多个独立的训练进程
import torch.multiprocessing as mp

# 专为分布式训练设计的 Sampler，确保每个epoch开始时，所有进程的数据打乱顺序是同步的，从而保证训练的随机性和一致性
from torch.utils.data.distributed import DistributedSampler

# DistributedDataParallel 分布式数据并行模式的核心封装类(封装 训练模型)，自动处理梯度同步
from torch.nn.parallel import DistributedDataParallel as DDP

# init_process_group    : 初始化分布式进程组
#     1. 建立 & 初始化 所有进程之间的 通信连接
#     2. 定义 通信后端 backend(NCCL / Gloo) & 总进程数(world_size) & 当前进程ID(rank)
# destroy_process_group : 销毁分布式进程组，清理和终止所有进程之间的分布式连接和资源
from torch.distributed import init_process_group, destroy_process_group
```

**初始化 分布式 进程组**

`init_process_group()`
1. 所有进程都被告知去连接 同一组 IP地址 & Port
2. `rank` 需要是 global rank
3. Rendezvous 过程 : 第一个成功监听并等待其他进程连接的进程，就会成为实际的 master，其他进程则作为 worker
4. 技术上任何进程都可以成为 Master 进程，但是 标准 PyTorch DDP 启动工具(如 `torch.distributed.run` 或 `mp.spawn`) 中，总是保证 `rank=0` 的进程会被指定为 master，监听 IP_Address & Port，并负责 **模型参数的初始广播**
5. 对于 **单机多GPU** 情况，localhost 是 master 地址(所有进程都知道的公共地址，其实所有 进程都在这台机器上，所以只能是 localhost)，rank 0 是 master 进程 (监听)
6. 对于 **跨 node** 情况，IP地址 不再是 localhost，需要指向集群中 一个特定的、可访问的 Master 节点的 IP地址(必须是 远程IP)
7. 阻塞特性，暂停所有进程的执行，直到所有进程(`world_size` 个) 都成功连接到 master 进程，成功创建进程组，所有进程获取的通信所需的信息，同步屏障才会解除

```python
def ddp_setup(rank, world_size):
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"

    init_process_group(backend="nccl", rank=rank, world_size=world_size)  # 这里是 global rank
    torch.cuda.set_device(rank)
```

**包装 原有 Model**
1. `device_ids` 是 **local_rank**
2. 对于 跨node 情况，是会多配置 `node_rank`，然后 所有进程 在 `init_process_group()` 代码上设置一个 同步屏障(Synchronization Barrier)


```python
self.model = DDP(model, device_ids=[gpu_id])  # gpu_id 是 纯数字，整数索引列表，不带 cuda
```

**保存 需要 解包 之前已经先被 DDP类 包装了一次的 Model，得到 底层参数**，同时需要加上 条件 `if self.gpu_id == 0` 否则每个 process 都会保存一次 (redundance，所有 copy 都是一样的)

```python
# ckpt = self.model.state_dict()  # origin
ckpt = self.model.module.state_dict()
```

修改 `DataLoader`
1. 需要 显式 使用 `DistributedSampler` 包装 `Dataset` 对象
2. **shuffle 功能需要改为 False**，因为 `DistributedSampler` 已经承担 数据打乱(Shuffling) 和 数据切分(Sharding) 的双重职责


```python
train_data = torch.utils.data.DataLoader(
    dataset=train_dataset,
    batch_size=32,
    pin_memory=True,  # 作用是优化 DataLoader 和 GPU 之间的数据通道，是提升训练速度
    shuffle=False,
    sampler=DistributedSampler(train_dataset),
)
```

调整训练函数
1. 形参调整
   1. `device` 转 `rank` & `world_size`
   2. `world_size = torch.cuda.device_count()`
   3. 分布式训练中，全局 `rank` 是核心身份标识，有了 `rank` 和 `world_size`，PyTorch 就可以推断出所有其他必要的信息
2. 增加 `destroy_process_group()`
3. 主动调用训练函数，改为 使用 `mp.spawn(func, args=(parameters))` 启动 (单机多卡情况)



```python
# def main(device, total_epochs, save_every):  # origin
def main(rank, world_size, total_epochs, save_every):  # rank: 接收 mp.spawn 或 torchrun 自动注入的 当前进程 ID (即全局 rank)
```

## Fault Tolerance (TorchRun)

more performance, more susceptibility of failure，可能导致 process 之间 不 sync

通过 `torchrun` 提供容错能力

[torchrun - 个人笔记](./TorchRun.md)

torchrun assigns `RANK` and `WORLD_SIZE` automatically

不需要明确写出 master的 IP地址 & 端口，也不需在 `init_process_group()` 中写明 `rank` & `world_size`，仅需一个 backend(nccl) 即可


torchrun 会提供 `LOCAL_RANK` 环境变量，因此不用手动传入 `gpu_id`

```python
# self.gpu_id = gpu_id  # origin
self.gpu_id = int(os.environ["LOCAL_RANK"])
```

保存 & 加载 (torchrun 容错 对于 脚本的要求) : seamlessly resume after interruption

```python
def _save_snapshot(self, epoch):
    snapshot = {}
    snapshot["MODEL_STATE"] = self.model.module.state_dict()
    snapshot["EPOCHS_RUN"] = epoch
    torch.save(snapshot, "snapshot.pt")
    print(f"Epoch {epoch} | Training snapshot saved at snapshot.pt")

def _load_snapshot(self, snapshot_path):
    snapshot = torch.load(snapshot_path)
    self.model.load_state_dict(snapshot["MODEL_STATE"])
    self.epochs_run = snapshot["EPOCHS_RUN"]
    print(f"Resuming training from snapshot at Epoch {self.epochs_run}")


class Trainer:
    def __init__(self, snapshot_path, ...):
    if os.path.exists(snapshot_path):  # 增加 snap shot 加载
        self._load_snapshot(snapshot_path)


def train(self, max_epochs: int):
    for epoch in range(self.epochs_run, max_epochs):  # 增加继续训练
        self._run_epoch(epoch)
```

不需要 `mp.spawn()`

```python
if __name__ == "__main__":
    import sys
    total_epochs = int(sys.argv[1])
    save_every = int(sys.argv[2])
    main(save_every, total_epochs)

# 命令行执行
# torchrun --standalone --nproc_per_node=4 multigpu_torchrun.py <total_epochs> <save_every>
# standalone : 使用 c10d 作为本地 Rendezvous(不支持弹性)，单次、固定规模的分布式任务，所有的进程发现和协调都应该在本地进行，不依赖外部的协调服务
```

## Multinode Training

需要确保 nodes 之间 可以通过 TCP 连接

训练脚本 简单修改
1. 增加 `self.global_rank = int(os.environ["RANK"])`，由 torchrun 设置
2. log 的时候 就可以使用 `global_rank`，不会和 不同 node 的 `local_rank` 混淆

### torchrun on each node

参数说明
1. `--nproc_per_node` : num of process per node，torchrun 支持 异构 nproc
2. `--nnodes` : 总节点数
3. `--node_rank` : 当前 node 的 rank，从 0 开始到 nnodes-1
4. `--rdzv_id` : Rendezvous ID (集合点 ID)，独特的任务标识符，确保只有拥有相同 ID 的进程 才能加入这个通信组
5. `--rdzv_backend` : Rendezvous 后端
6. `--rdzv_endpoint` : Master 节点的 地址 & 端口

在跨节点分布式训练中，所有的 rdzv 相关配置和 nnodes 参数必须在所有参与训练的节点上保持完全一致

```bash
torchrun \
--nproc_per_node=4 \  # torchrun 支持 异构 nproc
--nnodes=2 \
--node_rank=0 \
--rdzv_id=456 \
--rdzv_backend=c10d \
--rdzv_endpoint=172.31.43.139:29603 \
multinode_torchrun.py 50 10  # 脚本和参数
```

```bash
torchrun \
--nproc_per_node=2 \  # torchrun 支持 异构 nproc
--nnodes=2 \
--node_rank=1 \
--rdzv_id=456 \
--rdzv_backend=c10d \
--rdzv_endpoint=172.31.43.139:29603 \
multinode_torchrun.py 50 10  # 脚本和参数
```



### SLURM

TODO


## minGPT Training

Hydra - TODO


---

# 创建进程

跨节点训练不能使用 `mp.spawn`，仅用于在单台机器上创建进程，`torch.multiprocessing.spawn` 自动注入 rank

需要使用 PyTorch 官方推荐的启动工具，并在两台机器上分别执行启动命令
1. `torchrun`
2. 旧版中的 `torch.distributed.launch`

`torchrun`
1. 在启动本地进程时，会自动计算并设置每个进程的全局 rank 和本地 rank，将它们作为环境变量传递给 Python 脚本
2. 计算公式 `Global_Rank = (Node_Rank × nproc_per_node) + Local_Rank`
   1. `nproc_per_node` : num of process per node，通常被设置为 当前 node 上的 GPU 总数


