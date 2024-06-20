# CMake & VSCode for C++

## Table of Contents

- [CMake \& VSCode for C++](#cmake--vscode-for-c)
  - [Table of Contents](#table-of-contents)
- [基于VSCode和CMake实现C/C++开发 | Linux篇](#基于vscode和cmake实现cc开发--linux篇)
  - [01 - Linux系统介绍](#01---linux系统介绍)
  - [02 - 开发环境搭建](#02---开发环境搭建)
  - [03 - GCC 编译器](#03---gcc-编译器)
  - [04 - GDB 调试器](#04---gdb-调试器)
  - [05 - VSCode](#05---vscode)
  - [06 - CMake](#06---cmake)
  - [07 - 项目开发](#07---项目开发)

---

# 基于VSCode和CMake实现C/C++开发 | Linux篇

[手把手教会VSCode的C++环境搭建，多文件编译，Cmake，json调试配置 | Windows篇](https://www.bilibili.com/video/BV13K411M78v/)

[基于VSCode和CMake实现C/C++开发 | Linux篇](https://www.bilibili.com/video/BV1fy4y1b7TC/)

## 01 - Linux系统介绍

Linux
1. 多用户 - 支持多个用户同时登录和操作(远程登录)
2. 多任务 - 每个用户可以运行多个程序
3. 一切皆文件

[linux-目录配置](../../../Linux/LinuxSystemic.md#linux-目录配置)

指令 - `命令 [选项] [操作对象]`

`pwd`   - print current working directory

`ls`    - list directory contents
1. `ls [Path]` eg : `./`, `../`, `/home`
2. `ls [Code]` eg : `-l` 列表形式, `-a` 显示所有(包括隐藏文件), `-h` 较高可读性

`cd`    - change directory - 相对路径、绝对路径

`mkdir` - make directory
1. `mkdir -p ~/a/b/c` 一次性创建多层
2. `mkdir -p a b c` 一次性创建多个

`touch` - 创建新文件

`rm` - remove
1. `rm -r` = `rm --recursive`
2. `rm -f` = `rm --force`


`cp [src] [dst]` - copy
1. `cp -r` = `cp --recursive`

`mv` - move/rename

`man` - 查看命令手册 - eg:`man ls`/`man cd`/`man man` - q 退出

## 02 - 开发环境搭建

```bash
sudo apt install build-essential gdb
sudo apt install cmake
```

```bash
lzy@legion:~ $ gcc --version
gcc (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.


lzy@legion:~ $ g++ --version
g++ (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0
Copyright (C) 2021 Free Software Foundation, Inc.

lzy@legion:~ $ gdb --version
GNU gdb (Ubuntu 12.1-0ubuntu1~22.04) 12.1
Copyright (C) 2022 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

lzy@legion:~ $ cmake --version
cmake version 3.25.1
CMake suite maintained and supported by Kitware (kitware.com/cmake).

```



## 03 - GCC 编译器

gcc 编译器支持 go, objective-C, objective-C++, fortran 等

vscode 通过调用 gcc 编译器

实际
1. gcc 编译 C
2. g++ 编译 C++

[编译器详解](../../Complier/Complier&Interpreter.md#编译器compiler)



## 04 - GDB 调试器

GNU Debugger，用来调试 `C/C++`

vscode 通过调用 GDB 调试器实现 `C/C++` 调试工作

GDB主要功能
1. 设置**断点**(断点可以是条件表达式)
2. 使程序在指定的代码行上**暂停执行**，便于观察
3. **单步执行程序**，便于调试
4. 查看程序中**变量值的变化**
5. 动态改变程序的执行环境
6. 分析崩溃程序产生的core文件


调试命令参数，使用 `gdb [可执行文件名]` 进入 gdb 调试程序
1. `help + [命令]` - `h` - 查看帮助命令
2. `run` - `r` - 重新开始运行文件
3. `start` - 单步执行
4. `list` - `l` - 查看源代码
5. `set` - 设置变量值
6. `next` - `n` - 单步调试(逐过程，不跳入函数)
7. `step` - `s` - 单步调试(逐语句，跳入函数)
8. `backtrace` - `bt` - 查看函数的调用的栈帧和层级关系
9. `frame` - `f` - 切换函数的栈帧
10. `info` - `i` - 查看函数内部局部变量数值
11. `finish` - 结束当前函数，返回函数调用点
12. `continue` - `c` - 继续运行
13. `print` - `p` - 打印值&地址






## 05 - VSCode



## 06 - CMake



## 07 - 项目开发


