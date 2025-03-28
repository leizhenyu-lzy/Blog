
[简达智能/ROS2学习教程](https://gitee.com/gwmunan/ros2/wikis)

# SLAM 选型

[ROS2之SLAM介绍和技术选型 - B站 GundaSmart](https://www.bilibili.com/video/BV1P4421w7Hm/)



SLAM
1. 粒子滤波
   1. Gmapping (2007)
      1. ROS 默认的 SLAM 方法
      2. 构建地图后，可以与 AMCL(自适应 蒙特卡洛 定位) 一起用于定位和自主导航
2. 图优化
   1. Cartographer (2016)
      1. 支持 单线/多线 激光雷达，IMU 融合
      2. 创建地图后，可以单独提供定位服务，也可以与 AMCL 一起
      3. Nav2 SLAM-Toolbox 默认使用 Cartographer+AMCL 组合
   2. [RTAB-Map(Real-Time Appearance-Based Mapping)](https://introlab.github.io/rtabmap/) (2014)
      1. 给予增量外观的回环检测器
      2. 回环检测 + 词袋 + 内存管理 + 数据库
      3. RGB-D/双目/激光/IMU/GPS 多传感器融合
      4. 支持回环检测、建图、定位、多线程、图优化
      5. 配套完善
         1. 传感器数据加工
         2. 自带里程计
         3. 地图(2D栅格 / 3D点云)
   3. ORB-SLAM
      1. 稀疏地图，不输出稠密地图或点云
      2. 基于关键帧的稀疏特征点定位系统
      3. 支持单目、双目、RGB-D
   4. FAST-LIO
      1. 快速激光里程计系统
      2. 支持 多线激光 + IMU
   5. VINS-Mono
      1. 视觉惯性 SLAM 系统，IMU + 单目/双目
      2. 难以对大规模场景进行重建
   6. VINS-Fusion
      1. VINS-Mono 的扩展版
      2. 支持多种传感器组合




