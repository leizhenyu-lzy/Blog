# ![](../Pics/carto001.svg) Cartographer

[Cartographer - Github](https://github.com/cartographer-project/cartographer)

[Cartographer - 文档](https://google-cartographer.readthedocs.io/en/latest/)

[Cartographer介绍与安装 - FishROS Github](https://github.com/fishros/d2l-ros2/blob/master/docs/humble/chapt10/get_started/2.Carto%E4%BB%8B%E7%BB%8D%E5%8F%8A%E5%AE%89%E8%A3%85.md)



## Table of Contents

- [ Cartographer](#-cartographer)
  - [Table of Contents](#table-of-contents)
- [安装](#安装)
  - [Source Code 安装](#source-code-安装)
  - [apt 安装](#apt-安装)


---


![](../Pics/carto002.png)


# 安装

## Source Code 安装

```bash
# -b 指定分支
cd WorkSpace
mkdir src
cd src

git clone https://ghproxy.com/https://github.com/ros2/cartographer.git -b ros2
git clone https://ghproxy.com/https://github.com/ros2/cartographer_ros.git -b ros2
wget http://fishros.com/install -O fishros && . fishros  # 选择 3 安装 rosdepc(国内版rosdep)
rosdepc install -r --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
# --from-paths src  这告诉 rosdep 从 src 目录中查找包
# --ignore-src      这个选项指示 rosdep 忽略 src 目录中已存在的源码包
# --rosdistro $ROS_DISTRO   这指定了使用哪个 ROS 发行版的依赖信息
# -y    这个选项使命令在执行时不会询问用户确认，自动默认答案为 "yes"，自动接受所有的安装

cd ..
colcon build --packages-up-to cartographer_ros  # 构建指定包及其所有依赖，确保某个包及其所有依赖都是最新
source install/setup.bash

ros2 pkg list | grep cartographer  # 查看是否安装成功
# cartographer_ros
# cartographer_ros_msgs
```


## apt 安装

```bash
# 安装 Cartographer
sudo apt install ros-humble-cartographer
sudo apt install ros-humble-cartographer-ros
```


