# Sparse Attention

DSA : DeepSeek Sparse Attention
1. indexer
   1. 给每个历史 tokens 打分，选出 Top-K tokens，再进行注意力计算
   2. indexer 仍然需要遍历全部 tokens
   3. 每个注意力层都需要各自的 indexer


MSA : MiniMax Sparse Attention

GLM 5.2 Sparse Attention
1. IndexShare : **解决 DSA 计算量大**，多个 Attention Layer 共用一个 indexer
2. LayerSplit : **降低单卡显存占用**，每张 GPU 不再存储所有 Attention Layer 的 KV Cache，仅持有部分层的
3. slime RL : Agent 后训练基础设施架构，为了支持智能体强化学习 后训练的复杂任务，支持多种训练和任务组织，提升长程任务训练效果

[GLM-5.2: Built for Long-Horizon Tasks - Project Website](https://z.ai/blog/glm-5.2)

