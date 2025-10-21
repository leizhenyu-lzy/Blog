# torchrun

`torchrun` (以前称为 `torch.distributed.run`)

PyTorch 官方推荐的分布式训练启动器，其最大的卖点
1. 容错能力 (Fault Tolerance)
2. 弹性训练 (Elastic Training)

**torchrun** 提供 外部的 **调度 & 监控(重启 & 协调)**，**训练脚本** 提供 内部的 **状态保存 & 恢复逻辑**

两者结合，才能实现真正的 **容错训练**

当故障发生时，**最多** 只损失从上一个 checkpoint 到 故障发生点之间 的训练进度



**torchrun 作为一个外部协调器(Agent) 核心机制**
1. 自动重启 (Automatic Restart)
   1. **Agent 监控** : torchrun 启动后，它会在每个节点上启动一个或多个代理进程(Agent Process)，代理进程负责监控本地运行的 Worker 进程 (即训练脚本 main 函数)
   2. **故障检测** : 如果一个Worker 进程失败 (eg: 因为 OOM、NCCL 通信错误、节点被抢占)，本地的 Agent 会立即检测到失败
   3. **统一重启** : Agent 会立即终止所有幸存的 Worker 进程，它会尝试重新启动整个 Worker 进程组，重启次数受限于启动时设置的 `--max-restarts` 参数
2. Rendezvous 机制 (Worker Discovery)
   1. **动态发现** : torchrun 使用 Rendezvous 后端 来让所有 Worker 进程动态地发现彼此
   2. **重新协调** : 当发生失败并重启时，所有新的 Worker 进程 会重新执行 `init_process_group()`，帮助重新组建一个健康的通信组，并分配新的全局 rank 和 world_size
   3. **==P.S.==** : 在 torchrun 机制下，进程的 rank 是不稳定的，重启后可能会变化
3. 弹性伸缩 (Elasticity)
   1. 处理资源的动态变化
   2. **动态加入/退出** : 如果 一个节点离开(故障) 或 一个新的节点加入，`torchrun` 会检测到集群成员发生变化
   3. **统一重启** : 会像处理故障一样，终止所有 Worker 进程
   4. **重新平衡** : 在新的节点集合上重新启动所有进程，并根据新的 world_size 和 rank 重新平衡负载，确保训练继续进行


**训练脚本 要求**
1. 定期保存 Checkpoint (快照) : 训练脚本必须 定期保存一个完整的训练快照 (Snapshot)
   1. 模型参数 : `model.state_dict()`
   2. 优化器状态 : `optimizer.state_dict()`
   3. epoch 计数，步数 计数 : 记录训练进度，纯 Python 变量
   4. 学习率调度器状态 : `scheduler.state_dict()`
   5. 随机数生成器状态 : `torch.get_rng_state()` / Python 的 random 库状态，确保训练的可复现性
   6. 代码
      ```python
      checkpoint = {
          'epoch': epoch,
          'global_step': step,
          'model_state_dict': model.state_dict(),
          'optimizer_state_dict': optimizer.state_dict(),
          'scheduler_state_dict': scheduler.state_dict(),
          # 'cuda_rng_state': torch.cuda.get_rng_state(), # 推荐！
      }
      torch.save(checkpoint, PATH)
      ```
2. 加载 Checkpoint : 脚本的 main 入口点必须首先尝试加载最近的 checkpoint
3. 恢复状态 : 如果加载成功，训练必须从保存的 epoch 和 step 恢复，而不是从头开始
4. **Graceful Restarts (优雅重启)**
   ```python
   def main():
       load_snapshot(snapshot_path)
       initialize()
       train()
   def train():
       for batch in iter(dataset):
           train_step(batch)
               if should_checkpoint:
           save_snapshot(snapshot_path)
    ```


TODO
1. `--standalone`


