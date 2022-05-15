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


# ROBOT ACADEMY 昆士兰科技大学

## 2D Geometry

**2D Rotation**
```matlab
% 二维旋转矩阵
R=rot2(num) % 默认弧度制
R=rot2(num,'ang') % 弧度制
R=rot2(num,'deg') % 角度制

% 对于选择矩阵，转置等于逆
inv(R) % 求逆
R' % 求转置

% 可视化
trplot2(R) % transform plot
axis=equal % 让坐标轴标度相同
```

![](Pics/2DGeometry001.png)


**2D Rotation and Translation**
```matlab
transl2(x,y) % 仅平移，输出3*3，旋转2*2部分为单位阵
trot2(xxx,"deg/ang") % 内容和rot2相同，输出3*3，平移部分为0
% 平移+旋转
transl2(x,y)*trot2(xxx,"deg/ang") % 这两个相乘相当于直接写，都是对于原坐标轴（fixed axis），所以线进行旋转再进行平移，所以旋转在后，平移在前
SE2(x,y,angle,"deg/ang")

% 可视化
axis([a b c d]) % 坐标轴范围
axis square
hold on
trplot2(T,'frame','num','color','c') % 'frame'后面跟'num'，该frame自身和坐标轴上会有该num。'color'后面跟一个字符表示的颜色。

plot_point(P,'*') % P是一个二维列向量，*是标记样式
```

![](Pics/2DGeometry002.png)

可以看出T3和T3x是一样的，主要SE2的se要大写

SE应该是special euclidean的意思special euclidean group

![](Pics/2DGeometry003.png)



## 3D Geometry

https://robotacademy.net.au/masterclass/3d-geometry/?lesson=94


# 机器视觉与控制 MATLAB算法基础











