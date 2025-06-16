AMP_for_hardware
1. legged_gym   仿真环境
2. rsl_rl       强化学习算法
3. datasets     动捕数据(json)
   1. trot 对角步
   2. pace 同侧步
   3. turn 转弯
4. resources    机器人模型文件
5. logs         训练日志和模型


`legged_gym/envs/__init__.py` - task register

dataset
1. 元数据
   1. LoopMode: "Wrap"
      1. 表示动作可以循环播放，到达最后一帧后回到第一帧，形成无缝循环
   2. FrameDuration: 0.021s
      1. 每帧的持续时间，帧间的时间间隔 (约21毫秒)
   3. EnableCycleOffsetPosition: true
      1. 启用位置循环偏移
      2. 允许角色在循环播放时保持前进运动，而不是原地重复
   4. EnableCycleOffsetRotation: true
      1. 启用旋转循环偏移
      2. 允许角色在循环时保持转向的连续性
   5. MotionWeight: 0.5 - 动作权重，用于混合多个动作
2. 帧数据(长度 61) 参考 `rsl_rl/rsl_rl/datasets/motion_loader.py`
   1. 3  : POS(xyz)
   2. 4  : ROT(xyzw)
   3. 12 : JOINT_POS (12 joints)
   4. 12 : TAR_TOE_POS_LOCAL (4 * 3, [FL RL FR RR] * [hip, thigh, calf]) 目标足端位置
   5. 3  : LINEAR_VEL
   6. 3  : ANGULAR_VEL
   7. 12 : JOINT_VEL (12 joints)
   8. 12 : TAR_TOE_VEL_LOCAL (4 * 3) 目标足端速度



LeggedRobot 没有继承 VecEnv，但它实现了相同的接口




AMP + PPO
1. 生成器 Generator : PPO策略网络，生成动作
2. 判别器 Discriminator : 区分 真实动捕数据 和 策略生成 动作
3. 动捕数据加载器 AMPLoader : 专家示范数据


判别器同时接收：策略轨迹 + 真实动捕数据
判别器学习区分真假动作
PPO的奖励函数 = 环境奖励 + 判别器奖励


`rsl_rl/rsl_rl/runners/amp_on_policy_runner.py`


