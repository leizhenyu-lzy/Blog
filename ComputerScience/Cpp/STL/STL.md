# STL

## Table of Contents

- [STL](#stl)
  - [Table of Contents](#table-of-contents)
- [全面理解STL标准库 - 双笙子佯谬](#全面理解stl标准库---双笙子佯谬)
- [C++ 标准库 体系结构 与 内核分析 - 侯捷](#c-标准库-体系结构-与-内核分析---侯捷)
  - [01 认识headers、版本、重要资源](#01-认识headers版本重要资源)
  - [02 STL体系结构基础介绍](#02-stl体系结构基础介绍)
  - [03 容器之分类与各种测试 1](#03-容器之分类与各种测试-1)
  - [04 容器之分类与各种测试 2](#04-容器之分类与各种测试-2)
  - [05 容器之分类与各种测试 3](#05-容器之分类与各种测试-3)
  - [06 容器之分类与各种测试 4](#06-容器之分类与各种测试-4)
  - [07 分配器之测试](#07-分配器之测试)
  - [08 源代码之分布 VC, GCC](#08-源代码之分布-vc-gcc)
  - [09 OOP 面向对象编程 vs GP 泛型编程](#09-oop-面向对象编程-vs-gp-泛型编程)
  - [10 技术基础：操作符重载and模板泛化, 全特化, 偏特化](#10-技术基础操作符重载and模板泛化-全特化-偏特化)
  - [11 分配器](#11-分配器)
  - [12 容器之间的实现关系与分类](#12-容器之间的实现关系与分类)
  - [13 深度探索 list (上)](#13-深度探索-list-上)
  - [14 深度探索 list (下)](#14-深度探索-list-下)
  - [15 迭代器的设计原则和Iterator Traits的作用与设计](#15-迭代器的设计原则和iterator-traits的作用与设计)
  - [16 vector 深度探索](#16-vector-深度探索)
  - [17 array、forward list 深度探索](#17-arrayforward-list-深度探索)
  - [18 deque、queue和 stack 深度探索 (上)](#18-dequequeue和-stack-深度探索-上)
  - [19 deque、queue和 stack 深度探索 (下)](#19-dequequeue和-stack-深度探索-下)
  - [20 RB tree 深度探索](#20-rb-tree-深度探索)
  - [21 set、multiset 深度探索](#21-setmultiset-深度探索)
  - [22 map、multimap 深度探索](#22-mapmultimap-深度探索)
  - [23 hashtable深度探索 (上)](#23-hashtable深度探索-上)
  - [24 hashtable深度探索 (下)](#24-hashtable深度探索-下)
  - [25 hash set、hash multiset, hash map、hash multimap 概念](#25-hash-sethash-multiset-hash-maphash-multimap-概念)
  - [26 unordered 容器概念](#26-unordered-容器概念)
  - [27 算法的形式](#27-算法的形式)
- [Understanding the C++ Standard Template Library](#understanding-the-c-standard-template-library)
  - [01.模板观念与函数模板](#01模板观念与函数模板)
    - [C++模板简介](#c模板简介)

---

# 全面理解STL标准库 - 双笙子佯谬

[全面理解STL标准库 vector容器 精讲](https://www.bilibili.com/video/BV1qF411T7sd/)

五大件
1. container    容器    - 存储数据
2. iterator     迭代器  - 指向数据，前后移动，类似指针(重载运算符)
3. algorithm    算法
4. functor      仿函数
5. allocator    分配器




---


# C++ 标准库 体系结构 与 内核分析 - 侯捷

![](Pics/houjie001.png)

![](Pics/houjie002.png)

[侯捷 - YouTube](https://www.youtube.com/playlist?list=PLTcwR9j5y6W2Bf4S-qi0HBQlHXQVFoJrP)

[侯捷 - Bilibili](https://www.bilibili.com/video/BV19u4y1J7dB/)

## 01 认识headers、版本、重要资源

Generic Programming 泛型编程 使用 模板 template 为主要工具

STL 即为 泛型编程最成功的作品

**标准库 ≠ STL**
1. **ST**L - **Standard Template Library** - 标准模板库
2. **C++标准库** - **Standard Library**
   1. 以 header files 头文件 形式呈现
   2. **包括 STL**，还包括输入/输出(I/O, iostream)、多线程支持、时间和日期处理、随机数生成、智能指针、异常处理等其他功能
   3. 可以不带 `.h` 后缀 (`<vector>`, `<cstdio>`)
   4. 组件封装于 `std` 命名空间  `using namespace std;`

重要网页
1. [cplusplus.com](https://cplusplus.com)
2. [CppReference.com](https://CppReference.com)
3. [gcc.gnu.org](https://gcc.gnu.org)

[STL 源码剖析 - 侯捷 - libgen](https://libgen.is/book/index.php?md5=6537AB49A4188713DD279012B0064A59)

## 02 STL体系结构基础介绍

![](Pics/houjie004.png)

![](Pics/houjie005.png)

六大部件 components
1. Container  - 容器
2. Allocator  - 分配器 (帮助容器分配内存，可以不写，有默认分配器)
3. Algorithm  - 算法 (模板函数)
4. Iterator   - 迭代器 (类似指针)
5. Adapter    - 适配器 (转换)
6. Functor    - 仿函数 (别称 function object)

**面向对象 OOP** - 数据 & 算法 在一个类中

**泛型编程 GP**  - 数据 & 算法 不在一个类中

![](Pics/houjie006.png)


## 03 容器之分类与各种测试 1


## 04 容器之分类与各种测试 2

## 05 容器之分类与各种测试 3


## 06 容器之分类与各种测试 4


## 07 分配器之测试



## 08 源代码之分布 VC, GCC

## 09 OOP 面向对象编程 vs GP 泛型编程

## 10 技术基础：操作符重载and模板泛化, 全特化, 偏特化

## 11 分配器

## 12 容器之间的实现关系与分类

## 13 深度探索 list (上)

## 14 深度探索 list (下)

## 15 迭代器的设计原则和Iterator Traits的作用与设计

## 16 vector 深度探索

## 17 array、forward list 深度探索

## 18 deque、queue和 stack 深度探索 (上)

## 19 deque、queue和 stack 深度探索 (下)

## 20 RB tree 深度探索

## 21 set、multiset 深度探索

## 22 map、multimap 深度探索

## 23 hashtable深度探索 (上)

## 24 hashtable深度探索 (下)


## 25 hash set、hash multiset, hash map、hash multimap 概念

## 26 unordered 容器概念

## 27 算法的形式
aizhi li
•
1384次观看 • 4年前

28

31:13
正在播放
28 迭代器的分类（category）
aizhi li
•
1823次观看 • 4年前

29

44:58
正在播放
29 迭代器分类（category）对算法的影响
aizhi li
•
1808次观看 • 4年前

30

49:03
正在播放
30 算法源代码剖析（11个例子）
aizhi li
•
1705次观看 • 4年前

31

28:28
正在播放
31 仿函数和函数对象
aizhi li
•
1561次观看 • 4年前

32

9:53
正在播放
32 存在多种Adapter
aizhi li
•
1211次观看 • 4年前

33

34:52
正在播放
33 Binder2nd
aizhi li
•
1429次观看 • 4年前

34

7:09
正在播放
34 not1
aizhi li
•
964次观看 • 4年前

35

24:30
正在播放
35 bind
aizhi li
•
1171次观看 • 4年前

36

8:58
正在播放
36 reverse iterator
aizhi li
•
1246次观看 • 4年前

37

13:35
正在播放
37 inserter
aizhi li
•
1160次观看 • 4年前

38

14:54
正在播放
38 ostream iterator
aizhi li
•
1206次观看 • 4年前

39

20:02
正在播放
39 istream iterator
aizhi li
•
1079次观看 • 4年前

40

45:09
正在播放
40 一个万用的hash function
aizhi li
•
1552次观看 • 4年前

41

41:20
正在播放
41 Tuple 用例
aizhi li
•
1283次观看 • 4年前

42

36:00
正在播放
42 type traits
aizhi li
•
1432次观看 • 4年前

43

20:23
正在播放
43 type traits 实现
aizhi li
•
1057次观看 • 4年前

44

9:06
正在播放
44 cout
aizhi li
•
928次观看 • 4年前

45

26:22
正在播放
45 movable元素对于deque速度效能的影响
aizhi li
•
1067次观看 • 4年前

46

26:34
正在播放
46 测试函数







# Understanding the C++ Standard Template Library

## 01.模板观念与函数模板

### C++模板简介









