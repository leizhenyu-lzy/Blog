# Legged Gym

[Isaac Gym Environments for Legged Robots - Github](https://github.com/leggedrobotics/legged_gym)

[RSL RL - Github](https://github.com/leggedrobotics/rsl_rl)

[强化学习框架 Legged Gym 训练代码详解](https://www.bilibili.com/video/BV1sLx6eLEyt)


逻辑分块
1. 创建交互环境
2. 添加机器人
3. 奖励设计
4. 探索机制(防止局部最优，同时保证行动策略收敛)
5. 推动训练



legged_robot.py	包含了获取观测，奖励设置函数，代价函数等内容

tinymal_constraint_him.py	用户定义的任务类，包含了独立任务自己的环境设置参数，奖励系统数

legged_robot_config.py	LeggedGymzi自带的基础类，包括了所有核心参数，会被其他程序继承






# 核心文件

`legged_gym/envs/base`
1. `legged_robot.py`
2. `legged_robot_config.py`

需要在 `legged_gym/envs/__init__.py` 文件中进行 import & register

才能使用 `legged_gym/scripts/train.py` 进行训练

```bash
python train.py --task=anymal_c_flat
python play.py --task=anymal_c_flat
```

P.S.
1. 子类中 明确重新定义的属性 会覆盖父类中的定义
2. 子类中 未重新定义的属性 将从父类中继承
3. 调用 `super().__init__` 会保留父类中初始化的变量





## `legged_robot.py`

`legged_robot.py`
1. 创建交互环境
   1. `__init__` - 继承 `BaseTask`(父类)，导入 `legged_robot_config.py` 定义的 `LeggedRobotCfg` 类
      1. `_init_buffers` - 自己开发时候可添加变量
      2. `_parse_cfg` - 导入 config 文件的值
      3. `super().__init__`
      4. `set_camera` - if not headless
   2. `create_sim`
      1. `_create_ground_plane`
      2. `_create_heightfield`
      3. `_create_trimesh` - 对于楼梯 & 上下坡
      4. `_init_height_points` - Returns points at which the height measurments are sampled (in base frame)，用于生成高度测量点的位置
   3. `_draw_debug_vis`
2. 添加机器人
   1. `_create_envs` - loads the robot URDF/MJCF asset & Environment(properties)
      1. `_process_rigid_shape_props`
      2. `_process_dof_props`
      3. `_process_rigid_body_props`
   2. `_get_env_origins` - Sets environment origins, Otherwise create a grid. (env 表示机器人)
   3. `_get_heights` - Samples heights of the terrain at required points around each robot (应对 凸起、凹陷 地形)，points are offset by the base's position and rotated by the base's yaw
   4. `_get_feet_heights`
3. 奖励设计(task类、smooth类、safety类、beauty类)
   1. `compute_reward`
   2. `_prepare_reward_function` - 在 `__init__` 中，导入 `LeggedRobotCfg/class rewards/class scales`(负值)，在其中注释对应 reward 的 scale 即可不导入
   3. reward functions(Penalize, 系数为负)
      1. `_reward_lin_vel_z` - 用于惩罚 z方向 线速度
      2. `_reward_ang_vel_xy` - 用于惩罚 xy方向 角速度
      3. `_reward_orientation`
      4. `_reward_base_height`
      5. `_reward_torques`
      6. `_reward_dof_vel`
      7. `_reward_dof_acc`
      8. `_reward_action_rate` - Penalize changes in actions(尽量平滑)
      9. `_reward_collision`
      10. `_reward_termination`
      11. `_reward_dof_pos_limits` - Penalize dof positions too close to the limit
      12. `_reward_dof_vel_limits`
      13. `_reward_torque_limits`
      14. `_reward_tracking_lin_vel` - 命令 & 实际 速度
      15. `_reward_tracking_ang_vel`
      16. `_reward_feet_air_time` - Reward long steps
      17. `_reward_stumble`
      18. `_reward_stand_still`
      19. `_reward_feet_contact_forces`
4. 探索机制(防止局部最优，同时保证行动策略收敛)
   1. `_push_robots` - Random pushes the robots
   2. `_get_noise_scale_vec` - a vector used to scale the noise added to the observations
   3. `reset_idx` 参数 重置
      1. update curriculum (基于课程学习 - Curriculum Learning)
         1. `_update_terrain_curriculum` - 调整机器人所处的地形难度 Terrain Curriculum(行走的距离超过当前地形长度的一半)
         2. `update_command_curriculum` - 调整机器人的指令难度 Command Curriculum，逐步增加机器人需要执行的任务复杂性(超过80%的奖励阈值)
         3. `_reset_dofs`
         4. `_reset_root_states`
         5. `_resample_commands` - Randomly select commands of some environments
   4. `check_termination` - 出现危险动作也会及时重置(contact_forces)，会有惩罚
5. 推动训练
   1. `step` - Apply actions, simulate, call `self.post_physics_step()`，遍历 `self.cfg.control.decimation`
      1. `post_physics_step` - (先 refresh)，check **terminations**, compute **observations** and **rewards**
         1. `_post_physics_step_callback` - Callback called **before** computing terminations, rewards, and observations
            1. Compute ang vel command based on target and heading
            2. compute measured terrain heights
            3. randomly push robots
         2. `compute_observations`
      2. `_compute_torques` - Compute torques from actions (Actions can be interpreted as position or velocity targets given to a PD controller, or directly as scaled torques)
         1. control type (input): `P 位控` & `V 速控` & `T 力矩控`



## `legged_robot_config.py`

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
   1. `mesh_type` - 地形
   2. `curriculum`
3. `class commands`
   1. `resampling_time` - 重新 采样/更新 控制命令的时间间隔
   2. `class ranges` - 随机化控制指令 上下限 范围
   3. `curriculum`
4. `class init_state` - 重置相关
   1. `pos`
   2. `default_joint_angles` - 一般是站立/屈膝状态 (定义关节角度默认关节角度，一般情况下网络输出会与其进行叠加)
5. `class control`
   1. `control_type` - P: position, V: velocity, T: torques
   2. `decimation` = $$\frac{Policy DT}{Sim DT}$$ - 每个策略决策时间步(policy DT)内，环境模拟时间步(sim DT)中控制指令更新的次数(桥接策略更新频率和物理模拟频率之间的差异)
      1. 物理仿真的时间步(sim DT，如 1 ms 或更小)通常非常小，以确保模拟的物理行为足够准确
      2. 策略更新的时间步(policy DT)则相对较大(如 10 ms 或更多)，因为策略通常由神经网络控制，其更新频率相对较低
      3. 在一个策略时间步内，控制系统会在物理仿真时间步中更新 `decimation` 次控制指令，策略每次更新后的控制指令会在接下来的 `decimation` 个仿真时间步中保持一致
   3. PD Drive parameters (通常需要测算，可以独立定义各关节joint名称对应的PD系数，名字要与URDF对应)
      1. `stiffness`
      2. `damping`
   4. `action_scale` - 缩放控制输入 action，以将其映射到目标角度范围
6. `class asset` - 与 URDF 挂钩
   1. `file` - urdf 文件位置(一般放在 `resources/robots` 文件夹下)
   2. `keypoints` - 躯干link名称
   3. `end-effectors` - 终端link名称
   4. `foot-name` - 脚名称link名称
   5. `terminate_after_contacts_on` - 接触重置条件(一般是 base)
   6. `self_collisions`
7. `class domain_rand` - 域随机化(后续迁移)
8. `class rewards`
   1. `class scale` - 奖励权值
9.  `class normalization`
10. `class noise` - 增加鲁棒性
11. `class sim`
    1.  `dt` - 仿真频率，乘以 decimation 为 1 个 step 时间


`LeggedRobotCfgPPO` 类 - RL 网络相关
1. `class policy`
   1. `rnn_type` - lstm
   2. `activation` - elu, relu, selu, crelu, lrelu, tanh, sigmoid
2. `class algorithm`
3. `class depth_encoder`
4. `class runner`
   1. `max_iterations`
   2. `resume` & `resume_path` - 载入网络二次训练



