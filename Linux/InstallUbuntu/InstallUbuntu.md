# Install Ubuntu

[toc]

# 基础安装

跟着这个视频做就好，很清楚
[Windows 和 Ubuntu 双系统的安装和卸载 --- 机器人工匠阿杰](https://www.bilibili.com/video/BV1554y1n7zv)

## 雷蛇

### 查看BIOS模式

运行中输入msinfo32用于查看BIOS模式
![](Pics/checkUEFI01.jpg)
结果如图所示:UEFI
![](Pics/checkUEFI02.jpg)

### 系统配置
CPU
![](Pics/razorBIOS01.jpg)
GPU
![](Pics/razorGPU.jpg)

### secure boot 关闭
开机时按F2进入BIOS
![](Pics/razorSecureBoot01.jpg)
![](Pics/razorSecureBoot02.jpg)



## 换源
[ubuntu换源](https://blog.csdn.net/qq_45878098/article/details/126037838)

如果出现　Hash Sum mismatch Hashes of expected file
则删除　
sudo rm -rf /var/lib/apt/lists/*
sudo apt clean

然后换源，我是从中科大换成阿里解决的

## 卸载无用软件
```
sudo apt remove thunderbird*
sudo apt remove firefox*
sudo apt remove libreoffice-common
sudo apt remove libreoffice*
```
卸载相关小游戏

# 后续安装

## 输入法
[在Ubuntu20.04中安装中文输入法](https://zhuanlan.zhihu.com/p/529892064)

凑活用ibus也行

对于sougou，需要先安装发财系统

## 显卡驱动
[NVIDIA CUDA Toolkit Release Notes　官网](https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html)

![](Pics/gpuDriver02.png)

[INSTALL PYTORCH 官网](https://pytorch.org/)

![](Pics/gpuDriver01.png)

![](Pics/gpuDriver03.png)

因为pytorch我会安装最新的11.7，所以这里选择了470 
P.S.本来想选择510但是直接不允许我下载，遂放弃

[NVIDIA显卡的Ubuntu驱动程序安装方法](https://www.bilibili.com/video/BV1wY411p7mU/)

[ubuntu无法添加PPA的解决办法](https://blog.csdn.net/leviopku/article/details/101060133)
[联想拯救者Y7000安装NVIDIA显卡驱动](https://www.freesion.com/article/58521373000/)

### 雷蛇需要额外操作

选用了22.04

**启动时**
进入启动项时，选中第一行Ubuntu，按[e]，编辑启动项参数

找到linux开头的一行，去到该行末尾(可能该行会被分为两行显示)，输入空格+nomodeset

![](Pics/blacklist01.png)

输入ctrl+x，保存并启动

**进入系统后**
修改黑名单
sudo gedit /etc/modprobe.d/blacklist.conf

末尾添加
blacklist nouveau

最后命令行输入命令生效黑名单
sudo update-initramfs -u

**安装时**
如果提示没有make gcc等等，可以先安装ROS可能顺便解决，或者自己手动安装即可，然后一路yes即可

## 快捷方式
.desktop文件

记得添加可执行权限 chmod +x

[ubuntu下应用图标的更改](https://blog.csdn.net/thinszx/article/details/107590118)
.png也可以

```
(base) lzy@legion:/tmp$ sudo find /usr/share/ -name "meshlab*.desktop"
/usr/share/applications/meshlab.desktop

(base) lzy@legion:/tmp$ sudo gedit /usr/share/applications/meshlab.desktop
```



## 软件列表

### 软件包

**.deb**
edge浏览器
vscode
drawio
dbeaver
wps
eudic 欧陆词典
baidu net disk
linux qq
Feishu
netease cloud music
tencent meeting
sunlogin client

**apt install**
git
meshlab


## ROS
鱼香ROS一键安装指令
wget http://fishros.com/install -O fishros && . fishros




## miniconda
[关于conda环境的配置，看这一篇就够了](https://www.bilibili.com/read/cv8956636)
[使用Miniconda管理隔离虚拟Python环境](https://www.bilibili.com/video/BV1Mv411x775)

输入 conda config 就会自动在用户目录下生成 .condarc 文件


## 微信

[deepin-wine 微信](https://www.bilibili.com/video/BV1Vb4y1r79y)



