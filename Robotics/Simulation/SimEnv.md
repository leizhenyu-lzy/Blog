# Simulation Environment




# SimplerEnv: Simulated Manipulation Policy Evaluation Environments for Real Robot Setups

[](https://github.com/simpler-env/SimplerEnv)


物理引擎 + 3D渲染


**通用模拟器** - 适用于各种机器人任务，提供 物理模拟 + 传感器模拟 + 环境交互
1. **Isaac**
   1. 整合了最新的PhysX物理引擎和RTX图像渲染引擎，并引入了Pixar公司开发的USD(Universal Scene Description)
   2. 渲染质量高
2. Webots
3. [V-REP(改名为 CoppeliaSim)](https://www.coppeliarobotics.com/)
   1. Bullet、ODE、Vortex、Newton
4. **Gazebo**
   1. [Installing Gazebo with ROS](https://gazebosim.org/docs/latest/ros_installation/)
      1. `sudo apt-get install ros-${ROS_DISTRO}-ros-gz`
      2. `sudo apt install ros-humble-gazebo-ros-pkgs`
   2. 被整合进ROS体系
   3. 小车 COM(ZMP) 自动驾驶 仿真 highbay
5. PyBullet


物理引擎 - 专注于底层物理动力学模拟，通常被通用仿真器集成
1. PhysX(NVIDIA)
2. **MuJoCo**
   1. Multi-Joint Dynamics with Contact
   2. 被Google DeepMind收购
   3. 基于 Lagrangian 解析力学，动力学计算更精确
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



TODO
[Isaac Sim 教程I Introduction](https://www.bilibili.com/video/BV1EN4y1w7D5)
[Isaac Sim 教程II First Step](https://www.bilibili.com/video/BV1Ee4y1m71J)
[Isaac Sim 教程III ROS-ROS2](https://www.bilibili.com/video/BV1aR4y1X7R8)




Wu Silang - ClangTHU

SITU Manhao (MPhil of HKUST) - SCUT_LDY

小伍同学，龙胆也老师，睿哥
