# Legged Gym

[Isaac Gym Environments for Legged Robots - Github](https://github.com/leggedrobotics/legged_gym)

[RSL RL - Github](https://github.com/leggedrobotics/rsl_rl)

安装需要 isaac gym + rsl rl

[强化学习框架 Legged Gym 训练代码详解 - B站视频](https://www.bilibili.com/video/BV1sLx6eLEyt)

[Isaac Gym 说明文档](file:///home/lzy/Projects/isaacgym/docs/programming/index.html)

# Basic

逻辑分块
1. 创建交互环境
2. 添加机器人
3. 奖励设计
4. 探索机制(防止局部最优，同时保证行动策略收敛)
5. 推动训练


Observation Space - 描述智能体所能观察到的环境信息的集合(部分的 State)

Action Space - 所有可能动作的集合


`isaacgym.gymtorch` - Tensor API
1. `wrap_tensor` : wrap to PyTorch tensor
   1. acquire 的 内容 为 Gym Tensor Descriptor，使用需要转为 PyTorch Tensor
   2. root_states :
   3. dof_state :
   4. contact_forces :
2. `unwrap_tensor` : convert back to a Gym tensor descriptor
   1. 需要 `gym.set` 的需要 将 PyTorch Tensor 转回 Gym Tensor Descriptor



用 PPO 的 固定步长的 单步更新(Truncated Mini-Batch Updates)


GPU 并行仿真中 独立处理每个环境，提前终止的环境会被**立即重置**，并继续收集数据，而不是等待整个 batch 结束

每个环境 都会运行 24 个时间步，然后就执行一次 PPO 更新

每个 并行环境 按照 相同的策略 进行决策(On-Policy 需要确保策略一致性)，并收集数据

当所有环境收集满 `num_steps_per_env`(24 步)后，所有数据会一起用于更新策略


# Code Structure

Each environment is defined by an `env` file (`legged_robot.py`) and a `config` file (`legged_robot_config.py`).

The `config` file contains two classes:
1. one containing all the environment parameters (`LeggedRobotCfg`)
2. one for the training parameters (`LeggedRobotCfgPPo`)

Both `env` and `config` classes use `inheritance`

Each **non-zero reward scale** specified in `cfg` will add a function with a corresponding name to the list of elements which will be summed to get the total reward

Tasks must be **registered** using `task_registry.register(name, EnvClass, EnvConfig, TrainConfig)` in `envs/__init__.py`, but can also be done from outside of this repository.



# Terminal Usage

`python legged_gym/scripts/train.py` 参数
1. `--task <TASK>` : Task name
2. `--headless` : no rendering
3. `--resume` : Resume training from a checkpoint (配合 `--load_run` & `--checkpoint` 使用)
4. `--experiment_name <EXPERIMENT_NAME>`:  Name of the experiment to run or load
5. `--run_name <RUN_NAME>` : Name of the run
6. `--load_run <LOAD_RUN>` : Name of the run to load when `resume=True`. If -1: will load the last run
7. `--checkpoint <CHECKPOINT>` : Saved model checkpoint number. If -1: will load the last checkpoint
8. `--num_envs <NUM_ENVS>` : Number of environments to create
9. `--seed <SEED>` : Random seed
10. `--max_iterations <MAX_ITERATIONS>` : Maximum number of training iterations

`python legged_gym/scripts/play.py`
1. `--task <TASK>` : Task name
2. By default, the loaded policy is the last model of the last run of the experiment folder


# 核心文件

`tinymal_constraint_him.py`	用户定义的任务类，包含了独立任务自己的环境设置参数，奖励系统数


`legged_gym/envs/base`
1. `base_task.py`
   1. `__init__` 中 `self.gym = gymapi.acquire_gym()`
2. `base_config` -
3. `legged_robot.py` - 包含了获取观测，奖励设置函数，代价函数等内容
4. `legged_robot_config.py` - LeggedGym 自带的基础类，包括了所有核心参数，会被其他程序继承

需要在 `legged_gym/envs/__init__.py` 文件中进行 import & register

才能使用 `legged_gym/scripts/train.py` 进行训练

`legged_gym/scripts` (`train.py` & `play.py`)
1. `python train.py --task=anymal_c_flat`
2. `python play.py --task=anymal_c_flat`


`legged_gym/utils`
1. `helpers.py` 中 `get_args()` 函数，获取 命令行 参数
2. `task_registry.py` - 全局任务注册



P.S.
1. 子类中 明确重新定义的属性 会覆盖父类中的定义
2. 子类中 未重新定义的属性 将从父类中继承
3. 调用 `super().__init__` 会保留父类中初始化的变量







# `base_task.py`

`BaseTask` 类

`self.gym = gymapi.acquire_gym()`



# `legged_robot.py`

`legged_robot.py`
1. **创建交互环境**
   1. `__init__` - 继承 `BaseTask`(父类)，导入 `legged_robot_config.py` 定义的 `LeggedRobotCfg` 类
      1. `_init_buffers` - 自己开发时候可添加变量
      2. `_parse_cfg` - 导入 config 文件的值
      3. `super().__init__`
      4. `set_camera` - if not headless
   2. `create_sim`
      1. `_create_ground_plane` - 平地
      2. `_create_heightfield`
      3. `_create_trimesh` - 对于楼梯 & 上下坡
      4. `_init_height_points` - Returns points at which the height measurments are sampled (in base frame)，用于生成高度测量点的位置
   3. `_draw_debug_vis`
2. **添加机器人**
   1. `_create_envs` - loads the robot URDF/MJCF asset & Environment(properties)
      1. `_process_rigid_shape_props`
      2. `_process_dof_props` : stores position, velocity and torques limits defined in the URDF，多个环境共享，只需要执行一遍(env_id==0)
      3. `_process_rigid_body_props`
   2. `_get_env_origins` - Sets environment origins, Otherwise create a grid. (env 表示机器人)
   3. `_get_heights` - Samples heights of the terrain at required points around each robot (应对 凸起、凹陷 地形)，points are offset by the base's position and rotated by the base's yaw
   4. `_get_feet_heights`
3. **奖励设计(task类(完成任务 command)、smooth类(平滑 action)、safety类()、beauty类())**
   1. `compute_reward` - call each rewardlzy010409
   2.
   3. `_prepare_reward_function` - 在 `__init__` 中，导入 `LeggedRobotCfg/class rewards/class scales`(负值)，在其中注释 config 对应 reward 的 scale 即可不导入(无需删除)，奖励函数名需要是 `_reward_` + `<reward_scales_name>`
   4. reward functions(Penalize, 系数为负)
      1. `_reward_lin_vel_z` - 用于惩罚 z方向 线速度
      2. `_reward_ang_vel_xy` - 用于惩罚 xy方向 角速度
      3. `_reward_orientation`
      4. `_reward_base_height`
      5. `_reward_torques`
      6. `_reward_dof_vel`
      7. `_reward_dof_acc`
      8. `_reward_action_rate` - Penalize changes in actions(尽量平滑)
      9. `_reward_collision`
      10. `_reward_termination` - 筛选出 "需要重置但不是因为超时" 的环境
      11. `_reward_dof_pos_limits` - Penalize dof positions too close to the limit
      12. `_reward_dof_vel_limits`
      13. `_reward_torque_limits`
      14. `_reward_tracking_lin_vel` - 命令 & 实际 速度
      15. `_reward_tracking_ang_vel`
      16. `_reward_feet_air_time` - Reward long steps
      17. `_reward_stumble`
      18. `_reward_stand_still`
      19. `_reward_feet_contact_forces`
4. **探索机制(防止局部最优，同时保证行动策略收敛)**
   1. `_push_robots` - Random pushes the robots
   2. `_get_noise_scale_vec` - a vector used to scale the noise added to the observations (增加鲁棒性)
   3. `reset_idx` 参数 重置
      1. update curriculum (基于课程学习 - Curriculum Learning)
         1. `_update_terrain_curriculum` - 调整机器人所处的地形难度 Terrain Curriculum(行走的距离超过当前地形长度的一半)
         2. `update_command_curriculum` - 调整机器人的指令难度 Command Curriculum，逐步增加机器人需要执行的任务复杂性(超过80%的奖励阈值)
         3. `_reset_dofs`
         4. `_reset_root_states`
         5. `_resample_commands` - Randomly select commands
   4. `check_termination` - 出现危险动作也会及时重置(contact_forces)，会有惩罚
5. **推动训练**
   1. `step` - Apply actions, simulate, call `self.post_physics_step()`，遍历 `self.cfg.control.decimation`
      1. `post_physics_step` - (先 refresh)，check **terminations**, compute **observations** and **rewards**
         1. `_post_physics_step_callback` - Callback called **before** computing terminations, rewards, and observations
            1. Compute ang vel command based on target and heading
            2. compute measured terrain heights
            3. randomly push robots
         2. `compute_observations`
            1. `obs_buf` - 希望 观测的值，可以 add noise
      2. `_compute_torques` - Compute torques from actions (Actions can be interpreted as position or velocity targets given to a PD controller, or directly as scaled torques)
         1. control type (input): `P 位控` & `V 速控` & `T 力矩控`



# `legged_robot_config.py`

`legged_robot_config.py` 两个类
1. `LeggedRobotCfg` 类
2. `LeggedRobotCfgPPO` 类


`LeggedRobotCfg` 类
1. `class env`
   1. `num_envs` - 机器人数量
   2. `num_observations` - 观测值数量
   3. `num_actions` - 可动关节
   4. `env_spacing` - envs origin 间隔距离
   5. `episode_length_s` - 强化学习环境中每个 episode(训练周期)的时长，到时间重置，防止摆烂
2. `class terrain`
   1. `mesh_type` - 地形(plane, heightfield, trimesh)
   2. `curriculum`
3. `class commands`
   1. `resampling_time` - 重新 采样/更新 控制命令的时间间隔，不要太短或太长
   2. `class ranges` - 随机化控制指令 上下限 范围
   3. `curriculum`
4. `class init_state` - 重置相关
   1. `pos` - 避免 卡脚/天空生成
   2. `default_joint_angles` - 一般是站立/屈膝状态 (定义关节角度默认关节角度，一般情况下网络输出会与其进行叠加)
5. `class control`
   1. `control_type` - P: position, V: velocity, T: torques
   2. `decimation` = $\frac{Policy DT}{Sim DT}$ - 每个策略决策时间步(policy DT)内，环境模拟时间步(sim DT)中控制指令更新的次数(桥接策略更新频率和物理模拟频率之间的差异)
      1. `self.dt = self.cfg.control.decimation * self.sim_params.dt`
         1. `self.dt` : 策略时间步长
         2. `self.sim_params.dt` : 仿真的基本时间步长
      2. 物理仿真的时间步(sim DT，如 1 ms 或更小)通常非常小，以确保模拟的物理行为足够准确
      3. 策略更新的时间步(policy DT)则相对较大(如 10 ms 或更多)，因为策略通常由神经网络控制，其更新频率相对较低
      4. 在一个策略时间步内，控制系统会在物理仿真时间步中更新 `decimation` 次控制指令，策略每次更新后的控制指令会在接下来的 `decimation` 个仿真时间步中保持一致
   3. PD Drive parameters (通常需要测算，可以独立定义各关节joint名称对应的PD系数，名字要与URDF对应)
      1. `stiffness`
      2. `damping`
   4. `action_scale` - 缩放控制输入 action，以将其映射到目标角度范围
6. `class asset` - 与 **URDF** 挂钩
   1. `file` - urdf 文件位置(一般放在 `resources/robots` 文件夹下)
   2. `keypoints` - 躯干link名称
   3. `end-effectors` - 终端link名称
   4. `foot-name` - 脚名称link名称
   5. `terminate_after_contacts_on` - 接触重置条件(一般是 base)
   6. `self_collisions` - 自碰撞
7. `class domain_rand` - 域随机化(后续迁移)
8. `class rewards`
   1. `class scale` - 奖励权值
9.  `class normalization`
10. `class noise` - 增加鲁棒性
11. `class sim`
    1.  `dt` - 仿真频率，乘以 decimation 为 1 个 policy step 时间
    2.  `substeps`(LeggedRobotCfg中=1) : 物理引擎(例如 PhysX)会在每个 dt 内运行 substeps 次物理计算，更新物体的位置、速度、碰撞检测等


P.S. **==做 sim2sim 的时候，需要保证 control频率相同，即 `sim.dt` * `control.decimation` 的 结果相同==**



`LeggedRobotCfgPPO` 类 - RL 网络相关
1. `class policy`
   1. `rnn_type` - lstm
   2. `activation` - elu, relu, selu, crelu, lrelu, tanh, sigmoid
2. `class algorithm`
3. `class depth_encoder`
4. `class runner`
   1. `max_iterations`
   2. `resume` & `resume_path` - 载入网络二次训练
   3. `run_name`
   4. `experiment_name`












# Terminal Output

```bash
################################################################################
                     Learning iteration 1879/10000  # 训练进度

                       Computation: 3521 steps/s (collection: 0.224s, learning 0.067s)
                                    # 模拟环境每秒处理的步数 (数据收集(rollout)时间, 策略更新时间(神经网络训练))
               Value function loss: 0.0000  # Critic 价值网络的损失，应该趋于 0，否则说明 Critic 训练不充分
                    Surrogate loss: -0.0463  # PPO 策略损失，负值表示策略在优化方向上有所改进
             Mean action noise std: 1.93  # 反映了策略的 不确定性(随着训练进展通常会降低，因为策略会趋向确定性)
                       Mean reward: 0.00  # 当前平均回合(episode)的总奖励
               Mean episode length: 18.18  # 平均回合长度，如果太短，说明机器人可能摔倒过早
      Mean episode rew_action_rate: -0.0286
            Mean episode rew_alive: 0.0025
       Mean episode rew_ang_vel_xy: -0.0273
      Mean episode rew_base_height: -0.0015
          Mean episode rew_contact: 0.0031
   Mean episode rew_contact_no_vel: -0.0097
          Mean episode rew_dof_acc: -0.0635
   Mean episode rew_dof_pos_limits: -0.0099
          Mean episode rew_dof_vel: -0.1011
Mean episode rew_feet_swing_height: -0.0038
          Mean episode rew_hip_pos: -0.0225
        Mean episode rew_lin_vel_z: -0.0316
      Mean episode rew_orientation: -0.0040
          Mean episode rew_torques: -0.0050
 Mean episode rew_tracking_ang_vel: 0.0003
 Mean episode rew_tracking_lin_vel: 0.0010
--------------------------------------------------------------------------------
                   Total timesteps: 1925120
                    Iteration time: 0.29s
                        Total time: 509.11s
                               ETA: 2199.2s
```






# Tensorboard

`tensorboard --logdir=/home/lzy/Projects/unitree_rl_gym/logs`




# Modify


修改 DoF 后需要调整的地方

config
1. init_state
   1. default_joint_state
2. env
   1. num_privileged_obs (参考 compute_observations 中 self.obs_buf)
   2. num_observations (参考 compute_observations 中 self.privileged_obs_buf)
   3. num_actions
3. asset
   1. file
   2. penalize_contacts_on
   3. terminate_after_contacts_on
4. control
   1. stiffness
   2. damping



rollout : 指在给定策略(policy)下，从环境中收集的一段交互序列或轨迹(trajectory)

$\tau = (s_0, a_0, r_1, s_1, a_1, r_2, \cdots)$
1. state
2. action
3. reward




# Known Issues

[LeggedGym Known Issues - Github Readme](https://github.com/leggedrobotics/legged_gym?tab=readme-ov-file#known-issues)

The **contact forces** reported by `net_contact_force_tensor()` are **unreliable** when simulating on **GPU** with a **triangle mesh terrain**.

A solution is to **use force sensors**, but the force are propagated through the sensors of consecutive bodies(consecutive bodies) resulting in an undesirable behavior.

如果 每个link 都加入 force sensor 那就会 沿着 joints 向上传播，位于 chain 上方的传感器 会测量到 下方所有的合力，使得传感器读数变得 混杂，无法轻松提取出单个、干净的接触力

对于腿式机器人，其主要的地面交互点是足部/末端执行器，只在足部放置传感器，排除了 重力等内部力，那么 传感器测量的就是 足部与地面之间的反作用力(Ground Reaction Force)，也就是 **接触力(Contact Force)**

However, for a **legged robot** it is possible to **add sensors to the feet/end effector only** and get the expected results. When using the force sensors **make sure to exclude gravity from the reported forces** with `sensor_options.enable_forward_dynamics_forces`.


**IsaacGym Forces**
1. ==Constraint Solver Forces== 约束求解器产生的力(由 约束方程 共同求解出来的力)
   1. 接触力 : 足端与地形接触的法向力、摩擦力 & 机器人身体与环境之间的碰撞力
      1. 接触 不是 施加力 ，而是 **施加约束**
      2. 脚不能穿透地面 → 用约束方程描述 → 求解器解出满足约束的反作用力
   2. 关节约束力 : 关节把刚体 绑定 在一起产生的 **反作用力**，关节为了维持其类型而必须施加的内部力
      1. 数学约束
      2. hinge 约束 5 个自由度
      3. prismatic 约束 5 个自由度
      4. spherical 约束 3 个自由度
      5. fixed joint 约束 6 个自由度
2. ==Forward Dynamics Forces== 前向动力学产生的力
   1. 重力 (Gravity)
   2. 惯性相关的力 (Inertia)
      1. 加速度 引起的惯性力
      2. 科里奥利、离心 等效力
   3. 电机/驱动 (Actuator) 产生的关节力/力矩的传递 : 关节上施加的 torque 通过连杆传递到装 sensor 的 link 上时的反作用
   4. 外力 : 通过 API 加在刚体上的 force/torque


`class isaacgym.gymapi.ForceSensorProperties()` - 用于配置 **力传感器 Force Sensor** 的属性
1. `enable_constraint_solver_forces` : receive forces from constraint solver
2. `enable_forward_dynamics_forces` : receive forces from forward dynamics
3. `use_world_frame` : receive forces in the world rotation frame, otherwise reported in the sensor’s local frame



Example:

```python
sensor_pose = gymapi.Transform()
for name in feet_names:
   sensor_options = gymapi.ForceSensorProperties()
   sensor_options.enable_forward_dynamics_forces = False # for example gravity
   sensor_options.enable_constraint_solver_forces = True # for example contacts
   sensor_options.use_world_frame = True # report forces in world frame (easier to get vertical components)
   index = self.gym.find_asset_rigid_body_index(robot_asset, name)
   self.gym.create_asset_force_sensor(robot_asset, index, sensor_pose, sensor_options)
(...)

sensor_tensor = self.gym.acquire_force_sensor_tensor(self.sim)
self.gym.refresh_force_sensor_tensor(self.sim)
force_sensor_readings = gymtorch.wrap_tensor(sensor_tensor)
self.sensor_forces = force_sensor_readings.view(self.num_envs, 4, 6)[..., :3]
(...)

self.gym.refresh_force_sensor_tensor(self.sim)
contact = self.sensor_forces[:, :, 2] > 1.
```







