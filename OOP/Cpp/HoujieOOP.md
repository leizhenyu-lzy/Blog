# 面向对象程序设计
# (Object Oriented Programming , OOP)


# 侯捷 C++面向对象编程

## 01.编程简介

培养正规大气的编程习惯

以良好的方式编写C++ Class

1. Object Based（基于对象）
   1. class without pointer members(Complex)
   2. class with pointer members(String)
2. Object Oriented（面向对象）
   1. 继承(inheritance)
   2. 复合(composition)
   3. 委托(delegation)

![](Houjie/houjie001.png)


## 02.头文件与类的声明

![](Houjie/houjie002.png)

将数据和处理数据的函数包在一起。

<br>

![](Houjie/houjie003.png)

数据有很多份，函数只有一份。

<br>

1. Object Based 面对的是单一class的设计
2. Object Oriented 面对的是多重classes的设计，classes之间的关系

<br>

### C++代码的基本形式

![](Houjie/houjie004.png)


![](Houjie/houjie005.png)

<br>

### 头文件中的防卫式声明

```cpp
#ifndef __COMPLEX__
#define __COMPLEX__

#endif
```

保证第二次include不会重复包含

![](Houjie/houjie006.png)

### 头文件的布局

![](Houjie/houjie007.png)

先写①和②，最后判断需要写什么前置声明

### class的声明(declaration)

![](Houjie/houjie008.png)

### class template(模板)简介

![](Houjie/houjie009.png)

最后用
```cpp
complex<int>
complex<double>
```
绑定类型

<br>
<br>


## 03.构造函数

### inline内联函数

![](Houjie/houjie010.png)

函数过于复杂，编译器不会将函数认定为inline

### access level(访问级别)

数据部分一般作为private

![](Houjie/houjie011.png)

左边是直接取data，显然数据是private，所以是错误的

### constructor(ctor,构造函数)

创建一个对象，构造函数被自动调用

![](Houjie/houjie012.png)

构造函数特点
1. 函数名称和类相同
2. 可以拥有参数
3. 参数可以有默认值
4. 没有返回类型（不需要有）
5. 特有的initialization list初始列(优于赋值，在初始化阶段完成)
6. 赋值可以但是不够大气
7. 可以重载，且常常发生

### ctor(构造函数)可以有重载(overloading)

![](Houjie/houjie013.png)

其实函数名称并不相同，只有编译器看得懂

黄色部分不行，如果没有给参数，编译器不知道调用谁

<br>
<br>


## 04.参数传递与返回值

![](Houjie/houjie014.png)

如果将构造函数放在private中，则下面两行都是无法执行的

但是在singleton设计模式中会用到，不允许外界创建，外界只能用一份

![](Houjie/houjie015.png)

### 常量成员函数

![](Houjie/houjie016.png)

在成员函数小括号后加const

不会改变成员数据的时候，加const

对于上图，右下方的代码，变量前面有const，如果上面没写const，会报错。

### 参数传递 passbyvalue passbyreference

![](Houjie/houjie017.png)

如果是pass by value对于大数据量效率不高，要压栈

C可以用指针，C++可以用引用（形式漂亮）

能传引用尽量传引用

但是会影响原来的值

如果传过去不希望对方改值，加const


### 返回值传递 returnbyvalue returnbyreference

![](Houjie/houjie018.png)

### 友元 friend

![](Houjie/houjie019.png)

相同class的各个objects互为友元

![](Houjie/houjie020.png)

### 小结

注意点
1. 数据在private
2. 参数尽量用reference传递，加不加const看情况
3. 返回值尽量reference
4. 常量成员函数加const
5. 构造函数尽量使用initialization-list

### class body外的各种definition

![](Houjie/houjie021.png)

__doapl<=>do assignment plus做赋值加法

不是所有函数都可以returnbyreference

如果返回的是函数的临时变量，则不能returnbyreference

否则函数结束，临时变量已经销毁

下面是全局函数

![](Houjie/houjie024.png)

<br>
<br>

## 05.操作符重载与临时变量

### ①写成成员函数

![](Houjie/houjie022.png)

所有的成员函数都带有隐藏的参数——this，谁调用函数，就是谁

不显式写在函数参数表列中

对于上图c2是this，c1是r

![](Houjie/houjie023.png)

返回引用可以连串使用，如果void只能做一步

### ②写成非成员函数

![](Houjie/houjie025.png)

全局函数，没有this指针

### 临时变量

![](Houjie/houjie026.png)

不能returnbyreference

typename加()创建临时变量

黄色部分也是临时对象

![](Houjie/houjie027.png)

这里的+-代表的是正负号

编译器通过参数的不同将他们和加减区分

![](Houjie/houjie028.png)

![](Houjie/houjie029.png)


![](Houjie/houjie030.png)

流插入运算符<<一定不能写成成员函数

<<是作用在cout上的

而cout是标准库早就写好的，不会认识新的类型

cout的数据类型是ostream

<br>
<br>

## 06.复习complex类的实现过程

重载运算符“>>”的函数的第一个参数和函数的类型都必须是istream&类型，第二个参数是要进行输入操作的类。

重载“<<”的函数的第一个参数和函数的类型都必须是ostream&类型，第二个参数是要进行输出操作的类。

因此，只能将重载“>>”和“<<”的函数作为友元函数或普通的函数，而不能将它们定义为成员函数。

<br>
<br>

## 07.拷贝构造，拷贝复制，析构

class with pointer member

![](Houjie/houjie031.png)

防卫式声明

s3先以s1为初值，拷贝构造

然后s2赋值给s3，拷贝赋值

编译器会有默认的

带指针的，会指向同一个地方，所以不能用编译器默认的

![](Houjie/houjie032.png)

不要用数组，不够灵活

```cpp
String(const char* cstr = 0);
//构造函数，接受一个指针
String(const String& str);
//拷贝构造，接收自己类型
String& operator=(const String& str);
//操作符重载，拷贝赋值，接收自己类型
~String();
//析构函数
```

![](Houjie/houjie033.png)

不要忘记尾零(+1)

分配完空间记得strcpy

写析构函数，防止内存泄漏

![](Houjie/houjie034.png)
