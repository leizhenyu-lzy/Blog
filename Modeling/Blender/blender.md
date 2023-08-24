# Blender

**目录**
[toc]

# Blender 官网

[Blender 官网](https://www.blender.org/)

[Blender 官网 参考手册](https://docs.blender.org/manual/zh-hans/3.6/index.html)

[BlenderProject](https://projects.blender.org/)

[Chat Companion](https://blendermarket.com/products/chat-companion)

[Blender 键盘快捷键](https://wangchujiang.com/reference/docs/blender.html#:~:text=Blender%20%E4%B8%AD,187%20%E4%B8%AA%E9%94%AE%E7%9B%98%E5%BF%AB%E6%8D%B7%E9%94%AE%E7%9A%84%E8%A7%86%E8%A7%89%E5%A4%87%E5%BF%98%E5%8D%95)

# Blender 建模入门教程 -- 阿发你好

[Blender 建模入门教程 -- 阿发你好](https://www.bilibili.com/video/BV1fb4y1e7PD/)




# 八个案例教程带你从0到1入门blender【已完结】

[八个案例教程带你从0到1入门blender【已完结】](https://www.bilibili.com/video/BV1Bt4y1E7qn)

## 01 初识 Blender

Edit -> Preferences

Interface 改 中文 和 分辨率

System 可以看 渲染设备 改 撤销次数

开启自动保存设置

![](Pics/blender001.png)

修改键位映射

![](Pics/blender002.png)

![](Pics/blender003.png)

修改拾色器

![](Pics/blender012.png)


游标在哪，物体就添加在哪

**注意英文输入法问题**

切换视图
1. ~`键(1的左侧)
2. 右上角的坐标系圆圈

![](Pics/blender004.png)

![](Pics/blender005.png)

点击物体出现常用功能

![](Pics/blender006.png)

边缘线轮廓显式更清晰

![](Pics/blender007.png)


## 02 案例 : 萌三兄弟

**应用**变换值实质上是重置物体的位置、旋转或缩放值，视觉上物体仍位于原本位置。物体原点被移动到全局原点，清空旋转，缩放值重置为1。

案例说明，左侧倒角由于之前经过拉伸操作发生了形变，因此需要将**缩放操作**进行一个**应用**

个人相当于将原有物体固定下来，成为新物体，切断和原图形的联系

Ctrl + A

![](Pics/blender009.png)

添加修改器 (倒角修改器(平面拐角也可以倒角))

![](Pics/blender008.png)

连续按2次 R 为自由旋转，如果同时旋转多个物体，可以选择 **各自的原点** 进行同步旋转

![](Pics/blender010.png)


平直着色 (线条分明)

![](Pics/blender019.png)

平滑着色 (平滑过渡)

![](Pics/blender020.png)





调整摄像机视图(按`/~键后按1进入视图)，先勾选锁定摄像机到视图方位进行角度调整，再取消勾选

![](Pics/blender013.png)



分屏操作，在右侧边线处右键，选择分割方式

![](Pics/blender016.png)


开关网格线

![](Pics/blender021.png)



分类打组

![](Pics/blender011.png)

分类打组可以便于选择整个物体

![](Pics/blender017.png)





设置渲染结果分辨率

![](Pics/blender018.png)

查看渲染效果 (进入渲染模式)

![](Pics/blender014.png)

设置渲染引擎
1. Eevee 快
2. Cycles 慢 渐进式

![](Pics/blender015.png)


材质设置

![](Pics/blender022.png)

世界环境设置 (亮度也会影响场景)

![](Pics/blender023.png)

光源设置 (修改能量)

![](Pics/blender024.png)


渲染图像

![](Pics/blender025.png)


最终结果 (颜色调的有点屎，没有审美可言)

![](Pics/ThreeBodies.png)


## 03 动画基础

动画 —— 记录 不同时间的 **属性变换**

动画离不开 时间、变量、属性 ，缺一不可

小圆点表示动画属性

![](Pics/blender026.png)

点击小圆点后，数值变为黄色，第一帧处打上了关键帧

![](Pics/blender027.png)

设置新关键帧位置，并使物体移动，红色表示当前位置未设置关键帧

![](Pics/blender028.png)

点击小方块后记录关键帧

![](Pics/blender029.png)

选择物体，使用快捷键 i 插入关键帧



## 03 案例 : 积木组合

线框 + 透显 模式

![](Pics/blender030.png)

Alt + Z	透显模式

Shift + Z	线框模式

可以先在隔离模式(/)下利用线框模式选点，再退出隔离模式进行调整

吸附需要在编辑模式中使用

![](Pics/blender031.png)

添加文本

![](Pics/blender032.png)

修改文本需要再编辑模式中

设置中心位置

![](Pics/blender033.png)

或

![](Pics/blender034.png)

给文字添加实体化修改器

![](Pics/blender035.gif)

偏移量 (+1表示正偏，-1表示反偏，0表示两边对称)

桥接循环边 (alt + 鼠标 --> 选中循环边)

![](Pics/blender036.png)

![](Pics/blender037.png)

Shift + D 关联复制 (牵一发而动全身)

![](Pics/blender038.png)

自定义倒角类型

![](Pics/blender039.png)

阵列修改器

![](Pics/blender040.png)

添加曲线

![](Pics/blender041.png)

Tab 进入曲线修改模式

![](Pics/blender042.png)

细分曲线

![](Pics/blender043.png)

给曲线添加厚度

![](Pics/blender044.png)

材料自发光

面光用于体现轮廓

阴影有问题的解决方法

![](Pics/blender046.png)




最终结果

![](Pics/BlocksWithRocket.png)






# Linux 安装 & 卸载

## snap 方式

```bash
snap install blender --classic
```

使用该方法进行安装的好处是可以自动安装Blender的更新。与单个程序包管理器相比，Snap的Blender应该具有更一致的发布。

## tar.xz 方式

直接删除解压的目录 和 .desktop
