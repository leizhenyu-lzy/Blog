# Matlab Robotics Toolbox

[toc]

## Portals

[ROBOTICS TOOLBOX 官网](https://petercorke.com/toolboxes/robotics-toolbox/)

[机器视觉与控制 MATLAB算法基础 配套资源](https://petercorke.com/rvc/home/code-examples/)

[ROBOT ACADEMY 昆士兰科技大学](https://robotacademy.net.au/)

[MATLAB机器人工具箱10.4 机械臂仿真教学](https://www.bilibili.com/video/BV1q44y1x7WC)

# 专业术语

SO：Special Orthogonal Group 特殊正交群（理解为旋转）

SE：Special Euclidean Group 特殊欧式群（比SO的行和列都大1，理解为平移、旋转的结合）

![](/Pics/QUT/2DGeometry003.png)

SO(3)是3×3，SE(3)是4×4


# 安装机器人工具箱
在命令行窗口输入ver
![](/Pics/install01.png)
可以看到有Matlab自带的工具箱
![](/Pics/install02.png)

去ROBOTICS TOOLBOX官网下载 RTB.mltbx
![](/Pics/install03.png)

移动到目标位置，在Matlab中双击打开
![](/Pics/install04.png)
安装提示
![](/Pics/install05.png)
再次输入ver进行确认，安装成功
![](/Pics/install06.png)

P.S. 输入which及函数名可以看到函数位置
![](/Pics/install07.png)





# ROBOT ACADEMY 昆士兰科技大学

## 2D Geometry

### 2D Rotation

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

![](/QUT/Pics/2DGeometry001.png)


### 2D Rotation and Translation

```matlab
transl2(x,y) % 仅平移，输出3*3，旋转2*2部分为单位阵
trot2(xxx,"deg") % 内容和rot2相同，输出3*3，平移部分为0。默认弧度制，
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

![](/Pics/QUT/2DGeometry002.png)

可以看出T3和T3x是一样的，注意SE2的se要大写

```matlab
% 这两个函数默认都是弧度制
SE2(0,0,30,'deg')
transl2(0,0)*trot2(30,'deg')

% Results:
ans = 
    0.8660   -0.5000         0
    0.5000    0.8660         0
         0         0         1
ans =
    0.8660   -0.5000         0
    0.5000    0.8660         0
         0         0    1.0000
```



## 3D Geometry

### 3D旋转
```matlab
% 绕单个转轴，只能用角度制
R=rotx(num)
R=roty(num)
R=rotz(num)

det(R)
inv(R)
R'

trplot(R) % 有很多option，可以添加label，设置颜色，添加箭头
```

### 旋转操作不可交换性
```matlab
Rx=rotx(30);
Ry=roty(45);

% 显而易见，这里考虑的是Euler-Angle，不是绕着固定轴，所以先进行的写在左边，后进行的在右边

disp("先x，后y")
Rxy=Rx*Ry
disp("先y，后x")
Ryx=Ry*Rx

result:
先x，后y
Rxy =
    0.7071         0    0.7071
    0.3536    0.8660   -0.3536
   -0.6124    0.5000    0.6124
先y，后x
Ryx =
    0.7071    0.3536    0.6124
         0    0.8660   -0.5000
   -0.7071    0.3536    0.6124
```

### 旋转矩阵序列（欧拉角、RPY角）


**RPY**：绕固定的参考坐标系，绕定轴X（Roll）—Y（Pitch）—Z（Yaw）旋转。R(γ,β,α) = Rot(z,α)Rot(y,β)Rot(x,γ)。先进行的写在右边。

**Euler**：绕自身坐标系，绕动轴Z—Y—X旋转。R(α,β,γ) = Rot(z,α)Rot(y,β)Rot(x,γ)。先进行的写在左边。


```matlab
eul2r(theta1,theta2,theta3) % ZYZ 默认角度制

eul2r(0,0,45)

eul2r(45,0,0)

ans =
    0.7071   -0.7071         0
    0.7071    0.7071         0
         0         0    1.0000

ans =
    0.7071   -0.7071         0
    0.7071    0.7071         0
         0         0    1.0000
```


eul2r(a,b,c)的顺序：就是按照先a再b再c的顺序（欧拉角方式，不是fixed frame，左边的是先进行的运动）

```matlab
R1=eul2r(44,40,33)
R2=rotz(33)*roty(40)*rotz(44)
R3=rotz(44)*roty(40)*rotz(33)


% Result 显然R1和R3相同
R1 =
    0.0838   -0.8827    0.4624
    0.8381    0.3135    0.4465
   -0.5391    0.3501    0.7660
R2 =
    0.0838   -0.8381    0.5391
    0.8827    0.3135    0.3501
   -0.4624    0.4465    0.7660
R3 =
    0.0838   -0.8827    0.4624
    0.8381    0.3135    0.4465
   -0.5391    0.3501    0.7660
```


```matlab
% tr2eul 默认输出的欧拉角为弧度制，加deg输出角度制
R=[     0.7071   -0.7071   0;
        0.7071    0.7071   0;
        0         0        1.0000]
tr2eul(R,'deg')
tr2eul(R)

ans =
     0     0    45
ans =
         0         0    0.7854

```

有时候用eul2r的结果，反向通过tr2eul求出的eul和输入eul2r的结果不同，差pi（180°）。但是这些eul对应的旋转矩阵都是相同的。说明一个旋转矩阵可以对应多个欧拉角。

![](/QUT/Pics/3DGeometry003.png)



RPY（可以理解为一个飞机，飞机头指向X正方向）
1. Roll(X) 滚转角
2. Pitch(Y) 俯仰角
3. Yaw(Z) 偏航角

```matlab
R=rpy2r(a,b,c) % XYZ 默认角度制
tr2rpy(R,'deg') % 默认弧度制

R=rpy2r(0.1,0.2,0.3)
tr2rpy(R,'deg')

R=rpy2r(45,0,0)
rotx(45)

result:
R =
    1.0000   -0.0052    0.0035
    0.0052    1.0000   -0.0017
   -0.0035    0.0017    1.0000
ans =
    0.1000    0.2000    0.3000
R =
    1.0000         0         0
         0    0.7071   -0.7071
         0    0.7071    0.7071
ans =
    1.0000         0         0
         0    0.7071   -0.7071
         0    0.7071    0.7071
```

注意顺序
```matlab
% 相当于fixed frame，所以先进行的写在后面（默认xyz）
R1=rpy2r(45,0,0)
R2=rotx(45)

R1=rpy2r(45,30,0)
R2=roty(30)*rotx(45)

R1=rpy2r(45,30,60)
R2=rotz(60)*roty(30)*rotx(45)

% result
R1 =
    1.0000         0         0
         0    0.7071   -0.7071
         0    0.7071    0.7071
R2 =
    1.0000         0         0
         0    0.7071   -0.7071
         0    0.7071    0.7071
R1 =
    0.8660    0.3536    0.3536
         0    0.7071   -0.7071
   -0.5000    0.6124    0.6124
R2 =
    0.8660    0.3536    0.3536
         0    0.7071   -0.7071
   -0.5000    0.6124    0.6124
R1 =
    0.4330   -0.4356    0.7891
    0.7500    0.6597   -0.0474
   -0.5000    0.6124    0.6124
R2 =
    0.4330   -0.4356    0.7891
    0.7500    0.6597   -0.0474
   -0.5000    0.6124    0.6124
```

### 奇点Singularity&万向节锁Gimbal Lock
[万向节锁定](https://www.bilibili.com/video/BV1e3411y7RX/)

万向节用于航天器导航，中间蓝色部分姿态保持恒定（装有陀螺仪）（相当于和fixed frame只有一个平移关系）。通过航天器和中间部分的角度偏差可以推算航天器姿态。
![](/QUT/Pics/3DGeometry001.png)

当绕中间的轴（xyz中的z）旋转90°时，z轴被转到之前的x轴，绕原先的
z轴的转动自由度消失。对于上图，如果不考虑连接件运动顺序限制，当y旋转90°时，z轴和x轴重合，原先z轴的旋转自由度丢失。不管采用哪种欧拉角，只要中间的轴旋转90度，就会发生万向节锁。可以使用四元数插值解决。

![](/QUT/Pics/3DGeometry002.png)

如果有一个轴经常会在90度运动，则它不应该作为中间的轴。

同时对于动画制作，对旋转运动进行插值的时候也会带来问题（可以用四元数解决）。

```matlab
r = rpy2r(33,90,144)
rpy = tr2rpy(r, 'deg')

# results
r =
         0   -0.9336   -0.3584
         0   -0.3584    0.9336
   -1.0000         0         0
rpy =
         0   90.0000  111.0000
% 显然当绕y轴旋转的角度为90°时，出现了万向节锁问题
```

### 双向量表示法

![](/QUT/Pics/3DGeometry004.png)

approach:相当于Z轴，机械手接近物体的方向

orientation:相当于Y轴，穿过两指，夹取物体的方向

normal:相当于X轴，根据approach和orientation凑出的方向


### Angle-Axis 表示三维旋转

空间中任意两个同原点的坐标系，可以通过一次绕特定轴旋转得到。（即针对下图可以通过绕v轴转θ是的A变换到B）

![](/QUT/Pics/3DGeometry005.png)

已知两个坐标系之间的旋转矩阵关系R，显然在该旋转矩阵的作用下转轴v保持不变。所以v是旋转矩阵R的特征向量，且其特征值为1。还有两个复数特征向量可以用于获取θ角度信息。

![](/QUT/Pics/3DGeometry006.png)


**Matlab求特征值、特征向量**
```matlab
R = rotx(30)*roty(45)*rotz(60)
[eigenvectors,eigenvalues] = eig(R)

% eigenvalues中的对角线元素为特征值，eigenvectors中的每一列为对应特征向量

% results
eigenvectors =
   0.1218 - 0.5693i   0.1218 + 0.5693i   0.5676 + 0.0000i
  -0.6766 + 0.0000i  -0.6766 + 0.0000i   0.2905 + 0.0000i
   0.1654 + 0.4194i   0.1654 - 0.4194i   0.7704 + 0.0000i
eigenvalues =
   0.0464 + 0.9989i   0.0000 + 0.0000i   0.0000 + 0.0000i
   0.0000 + 0.0000i   0.0464 - 0.9989i   0.0000 + 0.0000i
   0.0000 + 0.0000i   0.0000 + 0.0000i   1.0000 + 0.0000i
```

可以看出显然有一个特征向量为纯实数（第三列）

```matlab
tr2angvec(R)
[angle,axis]=tr2angvec(R)  

% Result:
Rotation: 1.524404 rad x [0.567552 0.290453 0.770403]

angle =
    1.5244
axis =
    0.5676    0.2905    0.7704


% 额外信息
>> cos(1.524404)
ans = 0.0464
>> sin(1.524404)
ans = 0.9989
```

使用tr2angvec函数即可得到Angle和Axis。显然Axis就之前的纯实数特征向量。而另外两个带有虚数部分的特征值即为cos(θ)和sin(θ)。

**Rodriguez公式**

使用Rodriguez公式，可以通过给定

![](/QUT/Pics/3DGeometry007.png)

skew symmetric matrix：反对称矩阵

```matlab
R = rotx(30)*roty(45)*rotz(60)
[angle,axis]=tr2angvec(R);
angvec2r(angle,axis)


% Results
R =
    0.3536   -0.6124    0.7071
    0.9268    0.1268   -0.3536
    0.1268    0.7803    0.6124
ans =
    0.3536   -0.6124    0.7071
    0.9268    0.1268   -0.3536
    0.1268    0.7803    0.6124
```

### 四元数

```matlab
R = rotx(30)*roty(45)*rotz(60)
Q = UnitQuaternion(R)  % Q记得大写
Q.plot()
Q/Q
Q*inv(Q)

% Result
R =
    0.3536   -0.6124    0.7071
    0.9268    0.1268   -0.3536
    0.1268    0.7803    0.6124
Q = 
0.72332 < 0.3919, 0.20056, 0.53198 >
ans = 
1 < 0, 0, 0 >
ans = 
1 < 0, 0, 0 >
```

![](/QUT/Pics/3DGeometry008.png)

https://robotacademy.net.au/masterclass/3d-geometry/?lesson=100



# 机器视觉与控制 MATLAB算法基础


# MATLAB机器人工具箱10.4 机械臂仿真教学

## 工具箱demo

rtbdemo ：robotics toolbox demo

## 机械臂建模

## 常用函数

## 工作空间可视化

## 轨迹规划

## 三维模型

## 搬运动画





