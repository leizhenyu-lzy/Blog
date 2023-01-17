# Linux指令

[toc]

## Portals

[查看Linux系统架构的命令](https://blog.csdn.net/weixin_41010198/article/details/109166131)

[【HUST Linux】基础讲座——新手必须掌握的 Linux 命令](https://www.bilibili.com/video/BV1Ge4y1W76c)

[【HUST Linux】基础讲座——管道符、重定向与环境变量](https://www.bilibili.com/video/BV1R84y1x7F5)

[Linux重定向（输入输出重定向）详解](http://c.biancheng.net/view/5956.html)

[什么是 .bashrc，为什么要编辑 .bashrc](https://zhuanlan.zhihu.com/p/33546077)

[/etc/profile - 环境变量](https://www.jianshu.com/p/1dd22f5b521a)

## 查看版本

```shell
(base) lzy@legion:~/Project/GraduationProject$ uname -a
Linux legion 5.15.0-56-generic #62~20.04.1-Ubuntu SMP Tue Nov 22 21:24:20 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux

(base) lzy@legion:~/Project/GraduationProject$ cat /proc/version
Linux version 5.15.0-56-generic (buildd@lcy02-amd64-102) (gcc (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0, GNU ld (GNU Binutils for Ubuntu) 2.34) #62~20.04.1-Ubuntu SMP Tue Nov 22 21:24:20 UTC 2022

(base) lzy@legion:~/Project/GraduationProject$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 20.04.5 LTS
Release:	20.04
Codename:	focal
```

## 查看文件
![](./Pics/file02.png)


## 复制、删除、移动
![](Pics/file01.png)


## 别名
简化长命令&防止误删

alias 
unalias

![](Pics/alias01.png)

alias fileExplorer="nautilus"

bash文件夹界面

## 文件权限
![](Pics/fileProperty01.png)

![](Pics/fileProperty02.png)

## 查找

![find&locate](Pics/search01.png)

## 管道符

![](Pics/pipeline01.png)

![](Pics/pipeline02.png)

![](Pics/example08.png)

## 重定向
类型:
1. 输入重定向
2. 输出重定向
3. 重定向合并

![](Pics/redirect01.png)

![](Pics/example01.png)

![](Pics/example02.png)

![](Pics/example03.png)

![](Pics/example04.png)

![](Pics/example05.png)

![](Pics/redirect02.png)

![](Pics/example06.png)

![](Pics/example07.png)


## 环境变量

```
cat /etc/profile
cat ~/.bashrc
```

![](Pics/envs01.png)

![](Pics/envs02.png)

![](Pics/envs03.png)

![](Pics/envs04.png)

![](Pics/envs05.png)
