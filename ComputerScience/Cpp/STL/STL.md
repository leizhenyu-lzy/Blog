# STL

## Table of Contents

- [STL](#stl)
  - [Table of Contents](#table-of-contents)
- [全面理解STL标准库 - 双笙子佯谬](#全面理解stl标准库---双笙子佯谬)
- [C++标准库体系结构与内核分析](#c标准库体系结构与内核分析)
  - [01.认识headers、版本、重要资源](#01认识headers版本重要资源)
    - [C++ Standard Library VS Standard Template Library](#c-standard-library-vs-standard-template-library)
  - [02.](#02)
  - [03.](#03)
  - [04.](#04)
  - [05.](#05)
- [Understanding the C++ Standard Template Library](#understanding-the-c-standard-template-library)
  - [01.模板观念与函数模板](#01模板观念与函数模板)
    - [C++模板简介](#c模板简介)
    - [C++函数模板](#c函数模板)
  - [02.类模板与操作符重载](#02类模板与操作符重载)
    - [类模板](#类模板)
    - [操作符重载](#操作符重载)
  - [03.](#03-1)
  - [04.](#04-1)
  - [05.](#05-1)

---

# 全面理解STL标准库 - 双笙子佯谬

[全面理解STL标准库 vector容器 精讲](https://www.bilibili.com/video/BV1qF411T7sd/)






---


# C++标准库体系结构与内核分析

![](Pics/HoujieSTL001.png)

![](Pics/HoujieSTL003.png)

## 01.认识headers、版本、重要资源

C++标准库和C标准库不同，C标准库是一个个单一的函数，C++标准库主要分为6个part，彼此间有重要联系

![](Pics/HoujieSTL002.png)


![](Pics/HoujieSTL004.png)

### C++ Standard Library VS Standard Template Library

![](Pics/HoujieSTL005.png)

C++标准库，编译器所付给的头文件，可以看到源代码，有编译器则带有标准库

STL标准模板库，分为六大部件component

标准库大于STL

命名空间(namespace)，将模板、类、函数再封装

using namespace std;将std命名空间全部打开




<br>
<br>

## 02.




## 03.



## 04.




## 05.


# Understanding the C++ Standard Template Library

## 01.模板观念与函数模板

### C++模板简介

![](Pics/OtherSTL001.png)

如果没有模板，只能进行重载

![](Pics/OtherSTL002.png)

使用模板，有统一的型别参数

![](Pics/OtherSTL003.png)

专有名词，实例化

### C++函数模板

![](Pics/OtherSTL004.png)

![](Pics/OtherSTL005.png)

![](Pics/OtherSTL006.png)

![](Pics/OtherSTL007.png)

型别内部必须支持函数所使用的操作，否则会有编译错误

![](Pics/OtherSTL008.png)

模板会被编译两次

![](Pics/OtherSTL009.png)

![](Pics/OtherSTL010.png)

![](Pics/OtherSTL011.png)

优先采用非模板函数，省去了实例化的步骤

允许空模板

如果显式指明模板，无需参数推导

型别不同的参数，编译器只能调用非模板函数

![](Pics/OtherSTL012.png)

<br>
<br>

## 02.类模板与操作符重载

### 类模板

![](Pics/OtherSTL013.png)

第二点具体见下图

![](Pics/OtherSTL014.png)

![](Pics/OtherSTL015.png)

![](Pics/OtherSTL016.png)

如果用这个类本身参数类型必须完整

![](Pics/OtherSTL017.png)

再类外实现函数需要进行限定，类型要完整

![](Pics/OtherSTL019.png)

注意有可能必须加空格，否则会被认为是流操作符

![](Pics/OtherSTL020.png)

为了特化一个类模板，你必须在起始处声明一个template<>，接下来声明用来特化类模板的类型，这个类型被用作模板实参，且必须在类名的后面直接指定。

![](Pics/OtherSTL021.png)

把一个类模板里的参数型别全部特化

![](Pics/OtherSTL022.png)

把一个类模板里的参数型别部分特化

![](Pics/OtherSTL023.png)

注意避免二义性

![](Pics/OtherSTL024.png)

![](Pics/OtherSTL025.png)

### 操作符重载

![](Pics/OtherSTL026.png)

![](Pics/OtherSTL027.png)

![](Pics/OtherSTL027.png)

<br>
<br>

## 03.



## 04.



## 05.






