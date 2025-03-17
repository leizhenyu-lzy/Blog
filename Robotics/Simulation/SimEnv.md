# Simulation Environment




# SimplerEnv: Simulated Manipulation Policy Evaluation Environments for Real Robot Setups

[](https://github.com/simpler-env/SimplerEnv)





**通用模拟器** - 适用于各种机器人任务，提供 物理模拟 + 传感器模拟 + 环境交互
1. **Isaac**
   1. 整合了最新的PhysX物理引擎和RTX图像渲染引擎，并引入了Pixar公司开发的USD(Universal Scene Description)
2. Webots
3. V-REP(CoppeliaSim)
4. **Gazebo**
   1. 被整合进ROS体系
5. PyBullet


物理引擎 - 专注于底层物理动力学模拟，通常被通用仿真器集成
1. PhysX(NVIDIA)
2. **MuJoCo**
   1. Multi-Joint Dynamics with Contact
   2. 被Google DeepMind收购
3. Bullet
4. ODE(Open Dynamics Engine)
5. RaiSim

场景模拟器 - 更关注场景建模、视觉感知和交互(显示世界收集)，而不是底层物理动力学
1. SAPIEN (UCSD苏昊)
2. Habitat (Meta Fair)
3. iGibson (Stanford 李飞飞)
   1. Interactive Gibson
4. TDW
5. AI2-THOR





**mujoco vrep gazebo isaac**





