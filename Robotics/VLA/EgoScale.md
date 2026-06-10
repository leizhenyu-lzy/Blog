# EgoScale : Scaling Dexterous Manipulation with Diverse Egocentric Human Data

[EgoScale - GEAR @ NVIDIA Research - Website](https://research.nvidia.com/labs/gear/egoscale/#)

---

# Model Architecture

flow-based VLA
1. Pre-Trained VLM
2. DiT Action Expert (N iterations)
   1. condition : text(language instruction) & image -> vision-language embedding
   2. input  : Noisy Joint Angle & Noisy End-Effector Pose
   3. output : Joint Angle & End-Effector Pose
   4. robot data 有 proprioception，human data 没有，需要让模型的输入结构保持统一
      1. robot data : 正常输入关节角度
      2. human data : 输入一个 固定且可学习的占位符 Token，类似 NLP 里的 `[MASK]`
3. Embodiment-Conditioned MLP Adapters
   1. 不希望重新训练 DiT
   2. Input / Output Interface : MLP，joint -> latent -> joint
   3. 共享 : VLM & DiT & 手腕运动(Wrist motion)
   4. 输入输出接口 Adapters 根据具体机器人的 关节数 & 传感器 定制的

off-the-shelf(现成的) SLAM : 消除头部晃动干扰，计算出相机 在 3D 空间里的运动轨迹，把头部运动的干扰给反向抵消


# Training Recipe

step(`optimizer.step()`) ≠ epoch

DDP & Global BatchSize


3-Stage Pipeline
1. Stage 1 : Human Pre-Train
   1. 学基础的 物理常识
   2. data : 20K hours egocentric human data (no robot)
   3. fully unfreeze all VLA params
   4. diversity + semantic grounding
2. Stage 2 : **Aligned** Mid-Train
   1. data : aligned human-robot play dataset (人类 + 机器人遥操 数据)
   2. freeze VLM backbone, update vision encoder & DiT
   3. human-robot correspondence
3. Stage 3 : Post-Train
   1. data : task specific robot demonstration (具体任务的机器人遥操数据)
   2. if use mid-train, freeze vision encoder
   3. if skip mid-train, unfreeze vision encoder

