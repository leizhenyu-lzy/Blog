# Install Ubuntu

[toc]


## 安装

跟着这个视频做就好，很清楚
[Windows 和 Ubuntu 双系统的安装和卸载 --- 机器人工匠阿杰](https://www.bilibili.com/video/BV1554y1n7zv)

## 换源
[ubuntu换源](https://blog.csdn.net/qq_45878098/article/details/126037838)

## 卸载无用软件
thunderbird、libre等
sudo apt remove thunderbird
sudo apt remove libreoffice-common

## 输入法
[在Ubuntu20.04中安装中文输入法](https://zhuanlan.zhihu.com/p/529892064)

凑活用ibus也行

## 显卡驱动

[ubuntu无法添加PPA的解决办法](https://blog.csdn.net/leviopku/article/details/101060133)
[联想拯救者Y7000安装NVIDIA显卡驱动](https://www.freesion.com/article/58521373000/)


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





