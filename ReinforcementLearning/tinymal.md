# 华北舵狗王带你5天上手IsaccGym强化学习

[Tinymal 官网](https://tinymal.cn/)

[BiliBili 课程](https://www.bilibili.com/cheese/play/ep966381)

[课程 配套文档](https://www.bilibili.com/cheese/play/ep966684)

[IsaacGymEnvs - Github](https://github.com/isaac-sim/IsaacGymEnvs/tree/main)

[莫凡Python - RL](https://mofanpy.com/tutorials/machine-learning/reinforcement-learning/)


## 1 课程先导内容


数据融合

DQN

Markov Process

Q-Learning (+RBF网络拟合)

Deep Reinforcement Learning



## 2 浅尝截止 : 传统控制 与 RL-IsaacGym 官方倒立摆例子

传统控制(分层解耦)
1. 无人机 - ADRC 自抗扰控制器 & OLDX飞控 & 基于二维码阵列定位 & 姿态控制 - 无人机之父(拉菲罗·安德烈)
2. 腿足机器人 - kinematics & kinetics & 步态控制 & 力控 & 伺服

车摆，底部小车可以移动

IsaacGym RL 基本软件框架(Task)，使用 yaml 设置参数
1. `__init__` 初始化(仿真环境构建)
2. `step`
   1. pre
   2. post 环境复位

<img src="Pics/tinymal001.avif">

翻译
1. "タスク設定": "Task Settings"
   1. 为强化学习的任务提供配置和环境参数
2. "学習設定": "Learning Settings"
3. "タスク設計": "Task Design"
   1. 实际构建强化学习任务的逻辑和实现细节
      1. 奖励函数 (Reward Function)
      2. 观察空间 (Observation Space)
      3. 动作空间 (Action Space)
4. "タスク登録": "Task Registration"
   1. 将任务、环境或算法的定义注册到框架中，以便后续训练或运行时可以动态调用和使用
5. "学習アルゴリズム": "Learning Algorithm"


`source devel/setup.bash`
1. `devel/setup.bash` 加载特定工作空间的环境变量(临时配置)，仅限当前终端会话
2. 让当前终端会话能够访问 ROS 工作空间中的包和资源
3. 可能需要多次切换不同的工作空间，每次切换工作空间时需要运行

`source ~/.bashrc`
1. 重新加载全局用户配置(`~/.bashrc`)
2. `~/.bashrc` 提供的是全局的、持久的配置







## 3 牛刀小试 : 修改倒立摆例子




## 4 广泛学习 : 测试 Legged Gym 强化学习框架

[Isaac Gym Environments for Legged Robots](https://github.com/leggedrobotics/legged_gym)




## 5 深度学习 : 导出 URD 正确模型




## 6 算法部署 : 在 Isaac 里训练你的机器人




## 7 模型迁移 : 通过 mujoco 进行 sim2sim 迁移








