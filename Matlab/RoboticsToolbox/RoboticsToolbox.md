# Matlab Robotics Toolbox

[toc]

## Portals

[ROBOTICS TOOLBOX 官网](https://petercorke.com/toolboxes/robotics-toolbox/)

[机器视觉与控制 MATLAB算法基础 配套资源](https://petercorke.com/rvc/home/code-examples/)

[ROBOT ACADEMY 昆士兰科技大学](https://robotacademy.net.au/)

# 安装机器人工具箱
在命令行窗口输入ver
![](Pics/install01.png)
可以看到有Matlab自带的工具箱
![](Pics/install02.png)

去ROBOTICS TOOLBOX官网下载 RTB.mltbx
![](Pics/install03.png)

移动到目标位置，在Matlab中双击打开
![](Pics/install04.png)
安装提示
![](Pics/install05.png)
再次输入ver进行确认，安装成功
![](Pics/install06.png)

# 机器视觉与控制 MATLAB算法基础

## 位置与姿态描述

```matlab
R=rot2(num) % 默认弧度制
R=rot2(num,'ang') % 弧度制
R=rot2(num,'deg') % 角度制


```

https://robotacademy.net.au/masterclass/2d-geometry/?lesson=75










