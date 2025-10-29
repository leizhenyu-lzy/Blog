# Adversarial Motion Priors Make Good Substitutes for Complex Reward Functions

[AMP_for_Hardware - Website](https://sites.google.com/berkeley.edu/amp-in-real/home)

[AMP_for_Hardware - Github](https://github.com/Alescontrela/AMP_for_hardware)

---

## Table of Contents

- [Adversarial Motion Priors Make Good Substitutes for Complex Reward Functions](#adversarial-motion-priors-make-good-substitutes-for-complex-reward-functions)
  - [Table of Contents](#table-of-contents)
- [Dataset](#dataset)
- [RSL\_RL](#rsl_rl)
  - [algorithm/amp\_ppo.py](#algorithmamp_ppopy)
  - [algorithm/amp\_discriminator.py](#algorithmamp_discriminatorpy)
  - [dataset/motion\_loader.py](#datasetmotion_loaderpy)
  - [dataset/motion\_util.py](#datasetmotion_utilpy)
  - [dataset/pose3d.py](#datasetpose3dpy)
  - [runners/amp\_on\_policy\_runner.py](#runnersamp_on_policy_runnerpy)
  - [storage/replay\_buffer.py](#storagereplay_bufferpy)
  - [utils/utils.py](#utilsutilspy)



---



AMP_for_Hardware 整体结构
1. legged_gym : 仿真环境
2. rsl_rl     : 强化学习算法
3. datasets   : 动捕数据(json)
   1. trot 对角步
   2. pace 同侧步
   3. turn 转弯
4. resources  : 机器人模型文件
5. logs       : 训练日志和模型


# Dataset

dataset : 本质是 json，使用 `json.load` 即可读取
1. 元数据
   1. LoopMode: `Wrap` 表示动作可以循环播放，到达最后一帧后回到第一帧，形成无缝循环
   1. FrameDuration : 每帧的持续时间，帧间的时间间隔
   1. EnableCycleOffsetPosition: 启用位置循环偏移，允许角色在循环播放时保持前进运动，而不是原地重复
   1. EnableCycleOffsetRotation: 启用旋转循环偏移，允许角色在循环时保持转向的连续性
   1. MotionWeight: 0.5 - 动作权重，用于混合多个动作
2. 帧数据(长度 61) 参考 `rsl_rl/rsl_rl/datasets/motion_loader.py`，总时长就是 num_frames * duration
   ```py
   POS_SIZE = 3
   ROT_SIZE = 4
   JOINT_POS_SIZE = 12
   TAR_TOE_POS_LOCAL_SIZE = 12
   LINEAR_VEL_SIZE = 3
   ANGULAR_VEL_SIZE = 3
   JOINT_VEL_SIZE = 12
   TAR_TOE_VEL_LOCAL_SIZE = 12
   ```



# RSL_RL

[RSL_RL 的 PPO - 个人笔记](../RSL_RL/rsl_rl.md)

基于 RSL_RL 的 PPO 增加 AMP 成为 AMP-PPO

文件结构
1. **algorithms**
   1. `ppo.py`
   2. `amp_ppo.py` (new)
   3. `amp_discriminator.py` (new)
2. **datasets**
   1. `motion_loader.py` (new)
   2. `motion_util.py` (new)
   3. `pose3d.py` (new)
3. **env** - 环境抽象
   1. `vec_env.py`
4. **modules** - 网络模型
   1. `actor_critc_recurrent.py`
   2. `actor_critc.py`
5. **runners** - 训练驱动脚本
   1. `on_policy_runner.py`
   2. `amp_on_policy_runner.py` (new)
6. **storage** - 采样数据缓存
   1. `rollout_storage.py`
   2. `replay_buffer.py` (new)
7. **utils**
   1. `utils.py` (modify)




## algorithm/amp_ppo.py

`AMPPPO` 类 (仅说明和 `PPO` 类的 差别)
1. `__init__()`
   1. discriminator 组件
      1. discriminator :
      2. amp_transition : `RolloutStorage.Transition` 类
      3. amp_storage : `ReplayBuffer` 类
         1. `obs_dim = discriminator.input_dim // 2` : 整除2的原因，判别器的输入是 transition `[amp_obs_t , amp_obs_{t+Δt}]`，是 单帧 amp_obs 的 两倍
         2. `buffer_size = amp_replay_buffer_size` :
      4. amp_data : `AMPLoader`
      5. amp_normalizer : `Normalizer` 类，policy & expert 使用 同一套，保持判别器输入的分布一致性，每次先使用旧统计值进行 normalize，再更新统计值
   2. optimizer & params
      1. optimizer : `optim.Adam(params, lr=learning_rate)`
      2. params : 将 `actor_critic` & `discriminator.trunk`(判别器前几层) & `discriminator.amp_linear`(判别器最后一层) 三部分参数放进同一个 Adam，就能在一次反向传播里同时更新 策略+判别器
      3. 反向传播一次就能同时更新，在计算图里互不相依，梯度各算各的，Adam 只负责把各自的梯度做一步更新而已
      4. 给 判别器加了更大的 weight_decay，有助于判别器不过拟合
   3. min_std
2. `act()` : 收集数据到 transition，相比 rsl_rl 增加 `amp_transition.observations`
   1. ppo 的 action 仍然仅由 obs 得到，与 amp_obs 无关，amp 只是在训练时候产生间接影响
3. `process_env_step()` : 将 transition 增加到 storage，相比 rsl_rl 增加 `amp_storage.insert()` 和 `amp_transition.clear()`
4. `update()` **==☆==**
   1. 新增 loss : mean_amp_loss(amp 平均损失), mean_grad_pen_loss(梯度惩罚 平均损失)
   2. 增加 pred : mean_policy_pred(策略数据判别分数), mean_expert_pred(专家数据判别分数)
   3. 增加 生成器 : amp_policy_generator & amp_expert_generator，都是调用 `feed_forward_generator()` 函数
   4. **循环** : 将 generator & amp_policy_generator & amp_expert_generator 打包
      1. 根据 schedule & KL 更新 learning rate
      2. 计算 surrogate & value loss
      3. 计算 discriminator loss : expert_loss & policy_loss 求平均，都是 `torch.nn.MSELoss`
         1. 先用之前累计的统计量，进行 normalize
         2. expert 判别分数 目标 +1
         3. policy 判别分数 目标 -1
      4. 计算 grad_pen_loss 梯度惩罚
      5. 整体 loss : **surrogate_loss & value_loss & entropy & amp_loss & grad_pen_loss**
      6. 梯度下降，反向传播，梯度裁剪，迭代器更新权重
      7. 非 fixed_std 需要 clamp min_std
      8. 更新 normalizer 中的 统计量，为了后续更准确地 normalize 数据
      9. 累加 新增的 loss & pred
   5. 计算 loss & pred 均值
   6. 清空 storage




## algorithm/amp_discriminator.py

判别器
1. 训练阶段
   1. 专家数据 : disc 越大越好，很像真实动作
   2. 策略数据 : disc 越小越好，不像真实动作
2. 奖励计算阶段
   1. disc ≈ 1 时奖励最大



`AMPDiscriminator` 类 : 继承 `nn.Module`
1. `__init__()`
   1. input_dim : 判别器 接收 状态对，因此等于 `amp_data.observation_dim * 2` (在 `amp_on_policy_runner.py` 中 创建 AMPDiscriminator)
   2. amp_reward_coef
   3. trunk : `nn.Sequential`，一堆的 `nn.Linear` & `nn.ReLU` pair (切换为 train mode)
   4. amp_linear : `nn.Linear`，最后一层 `nn.Linear`，输出一个值 (切换为 train mode)
   5. task_reward_lerp
2. `forward()` : 依次执行 `trunk()` & `amp_linear()` 得到 判别器分数
3. `compute_grad_pen()` : WGAN-GP(Wasserstein GAN with Gradient Penalty)，强制梯度范数接近目标值，解决权重裁剪(weight clipping) 导致的 梯度消失/爆炸
   1. expert 的 state & next_state 合成 input，计算判别器分数 disc
   2. 计算 输出对输入的 梯度，沿着 已经构建好的 计算图(存储在张量的 grad_fn 属性中) 反向传播，数学上求梯度不需要 loss 直接求 Jacobian 矩阵即可
      1. `backward()` 通常用于 标量loss
      2. `autograd.grad()` 可用于 任何张量，等价于 按照 grad_outputs 加权求和，作为 虚拟 loss 进行 backward
         1. create_graph : 为梯度计算创建计算图，允许计算二阶梯度，后续要对梯度(`grad_pen.backward()`)再求导
         2. retain_graph : 保留计算图，允许多次反向传播，policy_d & expert_d & grad_pen 都要反向传播
         3. only_inputs : 只计算对指定inputs的梯度，不计算对模型参数的梯度
   3. 计算 梯度惩罚 : 每个样本的 L2 范数，和 目标的 差距，平方误差的均值
      1. WGAN-DP 原文是目标 1，AMP 中是 0，让判别器在专家数据附近更 温和，避免判别器尖锐，导致策略难以学习
4. `predict_amp_reward()` : AMP奖励计算
   1. `with torch.no_grad()`
   2. 计算 reward 的时候，切换为 eval 模式，最后 切换为 train
   3. 可以通过 lerp 系数 选择是否 和 task_reward 插值 (<=0 只用 amp reward，>0 amp & task reward 插值)，控制 风格学习 & 任务完成 之间的平衡
5. `_lerp_reward()` : 使用 task_reward_lerp 线性插值 task & discriminator reward



## dataset/motion_loader.py

import
1. rsl_rl.datasets.pose3d
2. rsl_rl.datasets.motion_util
3. rsl_rl.utils.utils



`AMPLoader` 类
1. 类变量中 定义 数据维度 & 数据索引，用于从 dataset 中取数据
2. `__init__()`
   1. time_between_frames : 用来构造 AMP transition 时，两帧之间应隔的时间，也就是 state & next_state 时间，$\Delta t_{\text{amp}}$
   2. 遍历 文件夹下的 所有轨迹文件，再 逐帧 标准化 & 归一化 quaternion，将每个文件的数据 记录在 各个 `List` 中，对于帧数据 list of `torch.tensor` (文件中 所有 frames 的 某些列，作为 tensor 整体，append 到 list 中)
      1. trajectories : 排除 ROOT_POS & ROOT_ROT & TAR_TOE_VEL_LOCAL，list of `torch.tensor`
      2. trajectories_full : 排除 TAR_TOE_VEL_LOCAL，list of `torch.tensor`
      3. trajectory_names : 动捕数据文件名
      4. trajectory_idxs : 动捕数据文件索引
      5. trajectory_lens : 总时间(间隔数 * frame_duration)，会转为 `np.array`
      6. trajectory_weights : dataset 中的 `MotionWeight` 字段，全部导入后会进行 归一化，除以 sum，会转为 `np.array`，用于调整采样比例
      7. trajectory_frame_durations : dataset 中的 `FrameDuration` 字段，会转为 `np.array`
      8. trajectory_num_frames : dataset 中的总帧数，会转为 `np.array`
   3. Preload Transition : 预加载数据(包括 ROOT_POS & ROOT_ROT)
      1. preload_transitions : `Boolean`
      2. traj_idxs : `weighted_traj_idx_sample_batch()`
      3. times : `traj_time_sample_batch()`
      4. preload_s & preload_s_next : 当前时刻 & 下一时刻 states，调用 `get_full_frame_at_time_batch()`
   4. all_trajectories_full : 将 list of `torch.tensor` 合称为 大的 单个 `torch.tensor`
3. `reorder_from_pybullet_to_isaac()` : 关节、足端 顺序从 PyBullet(FR, FL, RR, RL) 调整到 IsaacGym(FL, FR, RL, RR)，保证与仿真机器人模型一致
4. sample (replace=False 不放回，replace=True 放回)
   1. `weighted_traj_idx_sample()` / `weighted_traj_idx_sample_batch()` : 采样 1个/size个 idx，以 trajectory_weights 为比例
   2. `traj_time_sample()` / `traj_time_sample_batch()` : 传入 traj_idx，因为用到了 frame_duration `Δt_orig`
      1. subst = $\Delta t_{\text{amp}} + \Delta t_{\text{dataset}}$
      2. 实现的效果是 采样区间 落在 `[0, trajectory_len − (Δt_amp + Δt_orig)]` (为了后续插值)
5. blend
   1. `slerp()` : 线性插值，blend 是混合比例，并不是严格意义上的 球面线性插值(spherical lerp)
   2. `pybullet_utils.transformations.quaternion_slerp()` : 四元数插值方法
   3. `blend_frame_pose()` : 基本上使用基础线性插值，四元数调用 pybullet 并 标准化
6. `get_frame_at_time()` / `get_frame_at_time_batch()` / `get_full_frame_at_time()` / `get_full_frame_at_time_batch()` (区别是 single/batch & traj/traj_full)
   1. p : 采样的动作时刻(time) 在 整条动作时长(`trajectory_lens[traj_idx]`) 的 相对进度，不取整
   2. n : 当前 traj 的 frames 数量
   3. idx_low & idx_high : time 前后 frame 的 idx，用 floor & ceil，两者最多差1(小数 差1，整数 相同)
   4. frame_start & frame_end : 具体的 frame 信息，利用 idx_low & idx_high 获得
   5. blend : `p * n` 表示 frame 位置，夹在 idx_low & idx_high 中间，因此 `p * n - idx_low` 可以当做 blend 用于后续插值
7. `get_frame()` / `get_full_frame()` / `get_full_frame_batch()` : 都是 random (区别是 single/batch & traj/traj_full)
   1. random traj & random time -> random frame
8. `feed_forward_generator()` : AMP transition 生成器
   1. `preload_transitions = True` : 随机获取 idxs，s & s_next 去除 ROOT_POS & ROOT_ROT，加上 ROOT_HEIGHT (也就是 ROOT_POS 中的 高度)
   2. `preload_transitions = False` : 当前实现似乎没有 补上 ROOT_HEIGHT




## dataset/motion_util.py

`standardize_quaternion()` : 确保四元数的w分量为非负，解决四元数的双重表示问题 (四元数的标量项 w<0 时整体取负)

`normalize_rotation_angle()` : angle 限制在 [-pi, pi]

`calc_heading()` : 求出 yaw 角度

`calc_heading_rot()` : 调用 `calc_heading()` 得到 yaw，并返回 对应 仅绕 z 旋转的 四元数



## dataset/pose3d.py

`QuaternionNormalize()` : 四元数归一化(除以自身范数)

`QuaternionFromAxisAngle()` : 给 转轴 & 角度，得到 单位四元数

`QuaternionToAxisAngle()` : 逆过程，给定单位四元数 求 转轴 & 角度

`QuaternionRandomRotation()` : 随机在单位球面上 挑一根轴，采样角度，得到 单位四元数

`QuaternionToAxisAngle()` : 将 point 按照 quat 运动

`IsRotationMatrix()` : 利用 正交性 & 向量模长 & det=1 判断 是否是 纯旋转，det=-1 是镜像+旋转






## runners/amp_on_policy_runner.py

`AMPOnPolicyRunner` 类
1. `__init__()`:
   1. include_history_steps : 暂时没有启用，如果启用 Actor观测维度大幅增加，AMP观测维度保持不变
   2. 初始化 amp_data(`AMPLoader` 类) & amp_normalizer(`Normalizer` 类) & discriminator(`AMPDiscriminator` 类)
   3. 计算每个关节的自适应最小标准差 min_std，根据关节活动范围进行标准化，上下限差距越大，std越大
2. `learn()`
   1. 获取 `amp_obs = self.env.get_amp_observations()` & `obs = self.env.get_observations()`，不需要梯度
   2. discriminator 进入 train mode
   3. **外层循环** : 循环 `num_learning_iterations` 次
   4. 进行 Rollout 采样，使用 `with torch.inference_mode()`
   5. **内层循环** : 迭代 `num_steps_per_env` 次
      1. 根据之前的 obs & amp_obs 采样得到 action (这里 rollout 还是随机)
      2. 用 action 和环境交互 `env.step(actions)`，并获取新的 obs & amp_obs 供下次使用
      3. 环境交互 多返回了 reset_env_ids(应该和 dones 类似) & terminal_amp_states(在 legged robot 中的 `post_physics_step()` 获取)
      4. ==对 terminate 特殊处理==，对于 reset_env_ids 正常的 next_obs 是 新episode的初始状态，但是实际想要的是 下一帧的真实状态，因此特殊处理 `next_amp_obs_with_term[reset_env_ids] = terminal_amp_states`
      5. 计算 amp_reward，也不需要梯度 (计算 grad penalty 的时候才需要)
   6. 调用 amp_ppo 的 `update()`，在 `with torch.inference_mode()` 外，因此不影响梯度计算
3. `log()` : 额外 tensorboard 加入 mean_amp_loss & mean_grad_pen_loss，log 加入 mean_amp_loss & mean_grad_pen_loss & mean_policy_pred & mean_expert_pred
4. `save()` : 额外保留 discriminator_state_dict & amp_normalizer
5. `load()` : 额外加载 discriminator_state_dict & amp_normalizer





## storage/replay_buffer.py

`ReplayBuffer` 类 : 固定大小的 环形 经验缓存，用来存储环境中的状态转移
1. `__init__(self, obs_dim, buffer_size, device)`
   1. states : `(buffer_size, obs_dim)` 张量，保存当前时刻的观测
   2. next_states : `(buffer_size, obs_dim)` 同样大小，保存下一时刻的观测
   3. buffer_size
   4. step : 下一次写入的位置，写满后会循环覆盖
   5. num_samples : 记录目前已写入的样本数量，用于指定 `feed_forward_generator()` 的 random sample 范围，不超过 buffer_size
2. `insert()` : 一次性将 新的 states & next_states 从 step 位置开始 全部循环写入，会覆盖之前的，并且更新 step
   1. 潜在问题，如果写入 超大批次，一圈不够，可能导致 shape mismatch 错误
3. `feed_forward_generator()` : 生成器，生成 states & next_states batch pair，生成 num_mini_batch 对，每个尺寸为 mini_batch_size



## utils/utils.py

`RunningMeanStd` 类 : 继承 `object` 类，实时统计 均值 & 方差，供后续归一化使用
1. `__init__()` : mean 均值，var 方差，count 样本数量(初始化为 epsilon 防止 ÷0)
2. `update()` : 计算 batch 的 mean & var & count，再 `update_from_moments`
3. `update_from_moments` : 用 并行可合并公式 把 batch 统计量 与 历史统计量 合并


`Normalizer` 类 : 继承 `RunningMeanStd` 类
1. `__init__()` : input_dim 是 单帧 AMP observation 的维度
   1. epsilon
   2. clip_obs
2. `normalize()` : NumPy 版 归一化 & 裁剪异常值，用之前的统计值 normalize
3. `normalize_torch()` : PyTorch 版 归一化 & 裁剪异常值，用之前的统计值 normalize
4. `update_normalizer()`
   1. expert_batch & policy_batch 都是 长度=2 的 元组 `(state, next_state)`
   2. tuple + 表示 集合合并，`(policy_state , policy_next , expert_state , expert_next)`
   3. `torch.vstack` 把 4个张量在 batch 维度上竖直堆叠，形成一大批样本，用来更新均值/方差
   4. 堆叠后 batch size 变成 4倍，然后在 特征维度 求批量 均值 & 方差

policy 侧 amp obs 维度 == 专家 amp obs 维度

`Normalize` 类 : 继承 `torch.nn.Module` 类，把 `torch.nn.functional.normalize` 封装成一个层，把向量按 L2-范数 归一化到单位球面


`quaternion_slerp()` : 批量 四元数 slerp(球面线性插值)



---








LeggedRobotCfgPPO 中 设定 seed，其他 CfgPPO 继承

`set_seed()` 在 `legged_gym/utils/helpers.py`，设定 各种可能 用到的 random package 的 随机种子，在 `task_registry.py` 的 `make_env()` 被调用 (LeggedRobot -> BasTask -> create_sim + _create_envs)



LeggedRobot 没有继承 VecEnv，但它实现了相同的接口

sim 参数 定义在 legged_robot_config 中，控制 仿真环境



commands
1. num_commands : command 长度 4 (lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error))
2. 观测中只使用 Commands 的前 3 位
3. 两种 控制模式
   1. heading_command = False (default)
      1. 直接控制yaw角速度
   2. heading_command = True
      1. 设置目标朝向
      2. 系统自动计算yaw角速度
4. 命令重采样机制
   1. `_post_physics_step_callback` -> `_resample_commands`
   2. ```python
      env_ids = (
         (self.episode_length_buf % int(self.cfg.commands.resampling_time / self.dt) == 0)
         .nonzero(as_tuple=False)
         .flatten()
      )
      ```
      1. episode_length_buf : 记录每个环境的当前步数\
      2. resampling_time : 重采样时间间隔




AMP + PPO
1. 生成器 Generator : PPO策略网络，生成动作
2. 判别器 Discriminator : 区分 真实动捕数据 和 策略生成 动作
   1. `rsl_rl/rsl_rl/algorithms/amp_discriminator.py`
3. 动捕数据加载器 AMPLoader : 专家示范数据
   1. `rsl_rl/rsl_rl/datasets/motion_loader.py`


判别器同时接收：策略轨迹 + 真实动捕数据
判别器学习区分真假动作
PPO的奖励函数 = 环境奖励 + 判别器奖励


`rsl_rl/rsl_rl/runners/amp_on_policy_runner.py`


`AMPOnPolicyRunner` - `rsl_rl/rsl_rl/runners/amp_on_policy_runner.py`

`AMPDiscriminator` - `rsl_rl/rsl_rl/algorithms/amp_discriminator.py`
1. input_dim = 2 * amp_data.observation_dim
2. amp_reward_coef
3. amp_discr_hidden_dims
4. amp_task_reward_lerp

trajectories      :                             JOINT_POS(12) + TAR_TOE_POS(12) + LINEAR_VEL(3) + ANGULAR_VEL(3) + JOINT_VEL(12)
trajectories_full : ROOT_POS(3) + ROOT_ROT(4) + JOINT_POS(12) + TAR_TOE_POS(12) + LINEAR_VEL(3) + ANGULAR_VEL(3) + JOINT_VEL(12) + TAR_TOE_VEL(12)








AMP 查看数据时长






