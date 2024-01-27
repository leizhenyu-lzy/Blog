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


<br>
<br>

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

本质上，二元运算符都是两个参数，只不过如果写成成员函数会隐式含有一个this指针

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

## 07.拷贝构造，拷贝赋值，析构

class with pointer member

![](Houjie/houjie031.png)

防卫式声明

s3先以s1为初值，拷贝构造

然后s2赋值给s3，拷贝赋值

这两个步骤在编译器中会调用不同函数

拷贝构造和拷贝赋值编译器会有默认的，一个bit一个bit的拷贝

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
//析构函数，该类的对象死亡时，被调用
char* get_c_str()const {return m_data}
//返回指针，inline_function，注意加const
```

![](Houjie/houjie033.png)

带有hello的临时对象会自动释放空间，但是p需要手动释放

不要忘记尾零(+1)

分配完空间记得strcpy

写析构函数，防止内存泄漏

如果动态内存申请没有在析构函数中进行释放，就会造成内存泄漏

alias：别名，是释放危险的

申请用中括号释放也需要中括号

![](Houjie/houjie034.png)

这里是 **浅拷贝** 动作，我们需要实现深拷贝

a、b两个对象的data只有指针

导致内存泄漏，而且改变a或b会相互影响

![](Houjie/houjie035.png)

传进来的蓝本不会改变，所以加const

蓝色的两个语句意思完全相同

![](Houjie/houjie036.png)

先将自己清空，重新分配空间，然后拷贝

比较难考虑到的是自我赋值，如果不写会导致自己被清空

![](Houjie/houjie037.png)

判断自我赋值不仅提高效率，而且保证正确性

<br>
<br>

## 08.堆、栈与内存管理

![](Houjie/houjie038.png)

重载流插入运算符<<的时候一定不能写成成员函数，否则cout的位置会与类对象的位置颠倒，这是不令人习惯的

调用函数，返回成员的数据（指针）

![](Houjie/houjie039.png)

普通的变量在栈中，离开作用域则会被自动释放

用new动态申请的空间在堆空间，有责任释放

![](Houjie/houjie040.png)

auto->析构函数会被自动调用

![](Houjie/houjie041.png)

析构函数在整个程序结束被调用

![](Houjie/houjie042.png)

写在全局作用域之中，所有大括号之外

比main更早就存在

![](Houjie/houjie043.png)

new的需要delete该指针，会调用析构函数

![](Houjie/houjie044.png)

转型->强制类型转换 static_cast<>

调用构造函数 

![](Houjie/houjie045.png)

![](Houjie/houjie046.png)

红色的是cookie，用于记录回收空间大小，41中40代表64个byte，1表示是申请了空间。最后一位可以用于表示收回或者获得是因为，分配空间是以16byte为一个单位，空间一定是16byte的整数倍。

pad是表示为了凑整为16byte的填充空间

长的是调试模式Debug，短的是发表模式Release

![](Houjie/houjie047.png)

也是以16byte为一个单元分配

上下仍有cookie(4*2)，然后还有debug所需要的32+4

中间有四个字节用于记录数组元素个数

![](Houjie/houjie048.png)

加了中括号才知道是数组，调用多次析构，否则只会调用一次，内存泄漏的部分是?!

<br>
<br>

## 09.复习String类的实现过程

![](Houjie/houjie049.png)

![](Houjie/houjie050.png)

函数很简单，建议编译器做成inline

![](Houjie/houjie051.png)

拷贝构造也是构造，没有返回类型

![](Houjie/houjie052.png)

返回类型不是void是为了可以执行一连串赋值

<br>
<br>

## 10.类模板、函数模板及其他

### static

![](Houjie/houjie053.png)

两种调用real的方式只有左边是可以运行的，右边表示的含义是公用同一个函数，传入不同的this指针，对不同的对象进行操作

在函数参数中不能直接写this，但是在函数体中可以显式调用。黄色部分可写可不写

加上static的数据成员，和对象就脱离。在有多个对象但公用一个数据的时候会用到，因为只有一份

静态函数，加上static的成员函数，**没有this指针**，不能像一般的成员函数存取类对象中的数据，只能存取静态数据成员

![](Houjie/houjie054.png)

黄色是定义，静态数据需要在类外写黄色部分（定义），在类之中的只是声明

有两种调用static函数的方式，如果还没有类对象，可以通过class name调用

![](Houjie/houjie055.png)

将构造函数放在private中

a本身已经存在

![](Houjie/houjie056.png)

更好的实现方式

只有getInstance被调用才会产生a，而且只会产生一份

### cout

![](Houjie/houjie057.png)

cout 的类是从 ostream 继承

ostream 进行一系列的重载

### class template 类模板

![](Houjie/houjie058.png)

template和typename是关键字

使用时需要进行明确绑定，对T进行替换

### function template 函数模板

![](Houjie/houjie059.png)

template和class是关键字

typename和class相通的

不必明确指出，编译器会进行实参推导

责任拆分，比大小的设计应该由类的设计者完成，也就是要对运算符进行重载

### namespace

![](Houjie/houjie060.png)

namespace是一个关键字，后面跟名称

所有东西包装在命名空间中，防止同名

相同命名空间会被结合在一起

using directive是一次性全部打开

using declaration是一条一条打开

### 其他

![](Houjie/houjie061.png)

![](Houjie/houjie062.png)

<br>
<br>

## 11.组合与继承

![](Houjie/houjie063.png)

类和类之间的关系

### Composition 复合

![](Houjie/houjie064.png)

将Sequence替换

![](Houjie/houjie065.png)

一个类里面有另外一种类，在结构体中也类似

黑色菱形表示包含有其他的类

可能底层容器有好很多功能，但是被包装后只开放部分功能，而且名字进行换

这是Adapter设计模式，进行改造，本例中queue为adapter

![](Houjie/houjie066.png)

计算大小

![](Houjie/houjie067.png)

省略号表示自己类本身执行的内容

构造由内而外：先执行完内部的构造函数再执行外部的，红色部分是编译器加上的

默认构造函数，因为红色是编译器加上的，编译器不知道调用哪一个

析构由外而内

其实只要各自管各自，编译器会加代码

### Delegation 委托 composition by reference

![](Houjie/houjie068.png)

不管是用指针还是引用都说by reference

空心菱形表示指针

和Composition的生命期相同不一样，用指针会使得不同类的对象生命期不同步

pimpl：pointer to implementation

这个指针可以指向不同的StringRep(实现类，implementation class)，具有弹性。右边的变动不影响左端。也叫编译防火墙，左边的不用再编译

如果内容相同可以共享，但是牵一发而动全身。如果要修改，需要给一个副本，copy on write(写时拷贝)

### Inheritance 继承

![](Houjie/houjie069.png)

用空心三角形，从子类指向父类

T表示模板，type

有三种继承方式，public、private、protect

某一子类是一种父类

父类的数据是可以被继承下来的

子类除了自己的特有数据之外还有父类的数据成员

与虚函数搭配

![](Houjie/houjie070.png)

子类（派生类）中有父类的部分

父类的析构函数必须是虚函数(virtual)，否则会出现undefined behavior

一般子类会比父类大

<br>
<br>

## 12.虚函数与多态

![](Houjie/houjie071.png)

在成员函数前加virtual则成为虚函数

在继承的关系中，所有内容都可以被继承，数据和函数都可以被继承，数据继承是内存，而函数继承是调用权

override这一动词只能用在重写虚函数上

对于impure virtual，子类可以重新定义

加了virtual而且后面=0，是pure virtual，一定要子类定义

![](Houjie/houjie072.png)

PPT例子，其中只有Open File无法事先写好

![](Houjie/houjie073.png)

Serialize()在这里就是读文件，可以写成纯虚函数，也可也写成虚函数空函数体

将一个关键动作延缓，到子类去进行

template method：一个经典设计模式，用来做框架，将固定的可以写的先写好

eg:MFC microsoft foundation classes

通过子类对象调用父类函数

在子类中写Serialize()

![](Houjie/houjie074.png)

![](Houjie/houjie075.png)

![](Houjie/houjie076.png)

上一张图的上半部分，构造和析构的执行顺序

上一张图的下半部分，构造析构的执行顺序不会有歧义

![](Houjie/houjie077.png)

![](Houjie/houjie078.png)

指针，delegation

其他的子类都是Observer的子类，都是一种Observer，都可以放入vertor中

notify函数遍历vector中的所有Observer，并调用update函数

<br>
<br>

## 13.委托相关设计

一些设计模式

1. Composition -> Adapter
2. Delegation -> Handle/Body (pimpl)
3. Inheritance -> Template Method
4. Delegation + Inheritance -> Composite
5. Delegation + Inheritance -> Prototype


![](Houjie/houjie079.png)

Primitive代表文件，Composite代表文件夹

对于一个文件系统，文件夹既可以放文件又可以放文件夹

只能放指针，这样才能保证大小相同

component的add函数只能为空虚函数，不能是纯虚函数，因为单个文件不能add

![](Houjie/houjie080.png)

创建未来才会派生的子类

下划线表示静态，负号表示private，#号表示protected，正号或者不行是public



