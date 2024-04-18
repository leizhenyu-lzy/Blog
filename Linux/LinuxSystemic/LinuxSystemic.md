# Linux Systemic

<!-- TOC -->

- [Linux Systemic](#linux-systemic)
- [鸟哥的Linux私房菜 : 基础学习篇](#%E9%B8%9F%E5%93%A5%E7%9A%84linux%E7%A7%81%E6%88%BF%E8%8F%9C--%E5%9F%BA%E7%A1%80%E5%AD%A6%E4%B9%A0%E7%AF%87)
        - [相关指令](#%E7%9B%B8%E5%85%B3%E6%8C%87%E4%BB%A4)
    - [第01章 Linux是什么与如何学习](#%E7%AC%AC01%E7%AB%A0-linux%E6%98%AF%E4%BB%80%E4%B9%88%E4%B8%8E%E5%A6%82%E4%BD%95%E5%AD%A6%E4%B9%A0)
    - [第02章 主机规划与磁盘分区](#%E7%AC%AC02%E7%AB%A0-%E4%B8%BB%E6%9C%BA%E8%A7%84%E5%88%92%E4%B8%8E%E7%A3%81%E7%9B%98%E5%88%86%E5%8C%BA)
    - [第03章 安装 CentOS7.x](#%E7%AC%AC03%E7%AB%A0-%E5%AE%89%E8%A3%85-centos7x)
    - [第04章 首次登陆与线上求助](#%E7%AC%AC04%E7%AB%A0-%E9%A6%96%E6%AC%A1%E7%99%BB%E9%99%86%E4%B8%8E%E7%BA%BF%E4%B8%8A%E6%B1%82%E5%8A%A9)
    - [第05章 Linux 的文件权限与目录配置](#%E7%AC%AC05%E7%AB%A0-linux-%E7%9A%84%E6%96%87%E4%BB%B6%E6%9D%83%E9%99%90%E4%B8%8E%E7%9B%AE%E5%BD%95%E9%85%8D%E7%BD%AE)
    - [第06章 Linux 文件与目录管理](#%E7%AC%AC06%E7%AB%A0-linux-%E6%96%87%E4%BB%B6%E4%B8%8E%E7%9B%AE%E5%BD%95%E7%AE%A1%E7%90%86)
    - [第07章 Linux 磁盘与文件系统管理](#%E7%AC%AC07%E7%AB%A0-linux-%E7%A3%81%E7%9B%98%E4%B8%8E%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86)
    - [第08章 文件与文件系统的压缩,打包与备份](#%E7%AC%AC08%E7%AB%A0-%E6%96%87%E4%BB%B6%E4%B8%8E%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E7%9A%84%E5%8E%8B%E7%BC%A9%E6%89%93%E5%8C%85%E4%B8%8E%E5%A4%87%E4%BB%BD)
    - [第09章 vim 程序编辑器](#%E7%AC%AC09%E7%AB%A0-vim-%E7%A8%8B%E5%BA%8F%E7%BC%96%E8%BE%91%E5%99%A8)
    - [第10章 认识与学习BASH](#%E7%AC%AC10%E7%AB%A0-%E8%AE%A4%E8%AF%86%E4%B8%8E%E5%AD%A6%E4%B9%A0bash)
    - [第11章 正则表达式与文件格式化处理](#%E7%AC%AC11%E7%AB%A0-%E6%AD%A3%E5%88%99%E8%A1%A8%E8%BE%BE%E5%BC%8F%E4%B8%8E%E6%96%87%E4%BB%B6%E6%A0%BC%E5%BC%8F%E5%8C%96%E5%A4%84%E7%90%86)
    - [第12章 学习 Shell Scripts](#%E7%AC%AC12%E7%AB%A0-%E5%AD%A6%E4%B9%A0-shell-scripts)
    - [第13章 Linux 帐号管理与 ACL 权限设置](#%E7%AC%AC13%E7%AB%A0-linux-%E5%B8%90%E5%8F%B7%E7%AE%A1%E7%90%86%E4%B8%8E-acl-%E6%9D%83%E9%99%90%E8%AE%BE%E7%BD%AE)
    - [第14章 磁盘配额（Quota）与进阶文件系统管理](#%E7%AC%AC14%E7%AB%A0-%E7%A3%81%E7%9B%98%E9%85%8D%E9%A2%9Dquota%E4%B8%8E%E8%BF%9B%E9%98%B6%E6%96%87%E4%BB%B6%E7%B3%BB%E7%BB%9F%E7%AE%A1%E7%90%86)
    - [第15章 例行性工作调度（crontab）](#%E7%AC%AC15%E7%AB%A0-%E4%BE%8B%E8%A1%8C%E6%80%A7%E5%B7%A5%E4%BD%9C%E8%B0%83%E5%BA%A6crontab)
    - [第16章 程序管理与 SELinux 初探](#%E7%AC%AC16%E7%AB%A0-%E7%A8%8B%E5%BA%8F%E7%AE%A1%E7%90%86%E4%B8%8E-selinux-%E5%88%9D%E6%8E%A2)
    - [第17章 认识系统服务 （daemons）](#%E7%AC%AC17%E7%AB%A0-%E8%AE%A4%E8%AF%86%E7%B3%BB%E7%BB%9F%E6%9C%8D%E5%8A%A1-daemons)
    - [第18章 认识与分析登录文件](#%E7%AC%AC18%E7%AB%A0-%E8%AE%A4%E8%AF%86%E4%B8%8E%E5%88%86%E6%9E%90%E7%99%BB%E5%BD%95%E6%96%87%E4%BB%B6)
    - [第19章 开机流程、模块管理与 Loader](#%E7%AC%AC19%E7%AB%A0-%E5%BC%80%E6%9C%BA%E6%B5%81%E7%A8%8B%E6%A8%A1%E5%9D%97%E7%AE%A1%E7%90%86%E4%B8%8E-loader)
    - [第20章 基础系统设置与备份策略](#%E7%AC%AC20%E7%AB%A0-%E5%9F%BA%E7%A1%80%E7%B3%BB%E7%BB%9F%E8%AE%BE%E7%BD%AE%E4%B8%8E%E5%A4%87%E4%BB%BD%E7%AD%96%E7%95%A5)
    - [第21章 软件安装：源代码与 Tarball](#%E7%AC%AC21%E7%AB%A0-%E8%BD%AF%E4%BB%B6%E5%AE%89%E8%A3%85%E6%BA%90%E4%BB%A3%E7%A0%81%E4%B8%8E-tarball)
    - [第22章 软件安装 RPM, SRPM 与 YUM](#%E7%AC%AC22%E7%AB%A0-%E8%BD%AF%E4%BB%B6%E5%AE%89%E8%A3%85-rpm-srpm-%E4%B8%8E-yum)
    - [第23章 X Window 设置介绍](#%E7%AC%AC23%E7%AB%A0-x-window-%E8%AE%BE%E7%BD%AE%E4%BB%8B%E7%BB%8D)
    - [第24章 Linux 核心编译与管理](#%E7%AC%AC24%E7%AB%A0-linux-%E6%A0%B8%E5%BF%83%E7%BC%96%E8%AF%91%E4%B8%8E%E7%AE%A1%E7%90%86)
- [黑马程序员 - 新版Linux入门到精通](#%E9%BB%91%E9%A9%AC%E7%A8%8B%E5%BA%8F%E5%91%98---%E6%96%B0%E7%89%88linux%E5%85%A5%E9%97%A8%E5%88%B0%E7%B2%BE%E9%80%9A)
    - [初始 Linux](#%E5%88%9D%E5%A7%8B-linux)
    - [Linux 基础命令](#linux-%E5%9F%BA%E7%A1%80%E5%91%BD%E4%BB%A4)
    - [Linux 权限管控](#linux-%E6%9D%83%E9%99%90%E7%AE%A1%E6%8E%A7)
    - [Linux 实用操作](#linux-%E5%AE%9E%E7%94%A8%E6%93%8D%E4%BD%9C)
    - [实战软件部署](#%E5%AE%9E%E6%88%98%E8%BD%AF%E4%BB%B6%E9%83%A8%E7%BD%B2)
    - [脚本 & 自动化](#%E8%84%9A%E6%9C%AC--%E8%87%AA%E5%8A%A8%E5%8C%96)
    - [项目实战](#%E9%A1%B9%E7%9B%AE%E5%AE%9E%E6%88%98)
    - [云平台技术](#%E4%BA%91%E5%B9%B3%E5%8F%B0%E6%8A%80%E6%9C%AF)

<!-- /TOC -->



# 鸟哥的Linux私房菜 : 基础学习篇

**五大单元**
1. 输入单元
2. 输出单元
3. CPU - Central Processiong Unit
   1. 控制单元(控制器) - 协调各周边元件与各单元间的工作
   2. 算数逻辑单元(运算器) - 负责程序运算与逻辑判断
4. 内存

数据会流进/流出内存则是 CPU 所发布的控制命令

**CPU**
CPU实际要处理的数据完全来自于内存，不管是程序还是一般文件数据，内存内的数据则是从输入单元所传输进来

所有的单元都是由 CPU 内部的控制单元来负责协调的

CPU 其实内部已经含有一些微指令

**CPU架构**
1. 精简指令集 - RISC - reduced instruction set computer 
   1. 微指令集较为精简，每个指令的执行时间都很短，完成的动作也很单纯，指令的执行性能较佳
   2. 但是若要做复杂的事情，就要由多个指令来完成
   3. eg : ARM
2. 复杂指令集 - CISC - complex instruction set computer
   1. 与RISC不同的，CISC在微指令集的每个小指令可以执行一些较低阶的硬件操作
   2. 指令数目多而且复杂， 每条指令的长度并不相同
   3. AMD、Intel、VIA所开发出来的x86架构 - 最早的那颗Intel发展出来的CPU代号称为8086
   4. AMD依此架构修改新 一代的CPU为64位，64位的个人电脑CPU又被统称为x86_64架构

位 - 指的是CPU一次数据读取的最大量，64位CPU代表CPU一次可以读写64bits的数据

32位的CPU所能读写的最大数据量大概就是4GB左右 (选址范围有 4Gb，每个位置存 1Byte 数据)

bit 实在太小了，所以在储存数据时每份简单的数据都会使用到 8 个 bits 的大小来记录，因此定义出 Byte

不同的x86架构的CPU微指令集不同，新的x86的CPU大多含有很先进的微指令集

**芯片组**
主板上面有个链接沟通所有设备的**芯片组**，可以将所有单元的设备链接起来，
负责控制和管理主板上的各种外围设备和总线接口，
包括 : CPU、内存、扩展卡插槽、存储设备接口（如 SATA、NVMe）、USB 接口、网卡接口等

两个主要芯片 通过高速总线(如 DMI、HyperTransport)连接起来，形成了整个系统的芯片组架构
1. 北桥 - NorthBridge
   1. 负责处理与 CPU 直接通信的高速组件，比如内存控制器、PCI Express 总线、显卡接口等。
   2. 随着技术的发展，现代处理器已经集成了内存控制器和 PCIe 控制器，因此北桥的作用逐渐减弱。
2. 南桥 - SorthBridge
   1. 负责处理与 CPU 间接通信的低速组件，如硬盘接口（SATA、IDE）、USB、网卡、音频接口等。
   2. 通常也包含了一些辅助功能，如电源管理、时钟、GPIO（通用输入输出）等。

将内存控制器整合到 CPU 后，CPU与内存之间的沟通是直接交流，速度较快之 外，也不会消耗更多的带宽

|     进位制    |Kilo| Mega| Giga| Tera| Peta| Exa |Zetta|
|--------------|----|-----|-----|-----|-----|-----|-----|
|文件(B)  2进制 |1024|1024K|1024M|1024G|1024T|1024P|1024E|
|速度(Hz) 10进制|1000|1000K|1000M|1000G|1000T|1000P|1000E|

Mbps 是 Mbits per second，亦即是每秒多少 Mbit，转成文件大小的 Byte

例题：假设购买了500GB的硬盘一颗，但是格式化完毕后却只剩下460GB左右的容量，这是什么原因？
答：因为一般硬盘制造商会使用十进制的单位，所以 500 GByte 代表为 500×1000×1000×1000 Byte。 转成文件的容量单位时使用二进制(1024为底)，所以就成 为466GB左右的容量了。硬盘厂商并非要骗人，只是因为硬盘的最小物理量为512Bytes，最小的组成单位为扇区sector， 通常硬盘容量的计算采用 多少个sector ，所以才会使用十进制来处理的。

Linux最早在发展的时候，就是依据个人电脑的架构来发展的

原本的单核心CPU仅有一个运算单元，多核心则是在一颗CPU封装当中嵌入两个以上的运算核心，一个实体CPU外壳中，含有两个以上的CPU单元

不同的CPU型号大多具有不同的脚位，能够搭配的主板芯片组也不同



### 相关指令

```bash
# 返回值表示系统所用的处理器类型或架构
uname -m  # x86_64 | i386 | armv8l | ppc64le
# 显示CPU和其属性的信息 包含Architecture 
lscpu
# 在 Linux 系统上查看 CPU 信息的命令
# 包括 CPU 的型号、频率、缓存大小、核心数、线程数以及支持的指令集等
cat /proc/cpuinfo
```



## 第01章 Linux是什么与如何学习

Linux的核心原型是1991年由托瓦兹 Linus Torvalds 写出来的

## 第02章 主机规划与磁盘分区

## 第03章 安装 CentOS7.x

## 第04章 首次登陆与线上求助

## 第05章 Linux 的文件权限与目录配置

## 第06章 Linux 文件与目录管理

## 第07章 Linux 磁盘与文件系统管理

## 第08章 文件与文件系统的压缩,打包与备份

## 第09章 vim 程序编辑器

## 第10章 认识与学习BASH

## 第11章 正则表达式与文件格式化处理

## 第12章 学习 Shell Scripts

## 第13章 Linux 帐号管理与 ACL 权限设置

## 第14章 磁盘配额（Quota）与进阶文件系统管理

## 第15章 例行性工作调度（crontab）

## 第16章 程序管理与 SELinux 初探

## 第17章 认识系统服务 （daemons）

## 第18章 认识与分析登录文件

## 第19章 开机流程、模块管理与 Loader

## 第20章 基础系统设置与备份策略

## 第21章 软件安装：源代码与 Tarball

## 第22章 软件安装 RPM, SRPM 与 YUM

## 第23章 X Window 设置介绍

## 第24章 Linux 核心编译与管理








# 黑马程序员 - 新版Linux入门到精通

[黑马程序员 - 新版Linux入门到精通](https://www.bilibili.com/video/BV1n84y1i7td/)


## 初始 Linux

## Linux 基础命令

## Linux 权限管控

## Linux 实用操作

## 实战软件部署

## 脚本 & 自动化

## 项目实战

## 云平台技术



