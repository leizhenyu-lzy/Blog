# CMake

[toc]

## 说明

通过编译CMakeLists.txt

当多个人使用多种或单个语言或者编译器开发一个项目，最终要输出一个可执行文件或者共享库（dll、so等）

## CMake的HelloWorld编译

1. 写程序
2. 写CMakeLists.txt
3. cmake .
4. make

## CMakeLists语法介绍


## CMake内部构建和外部构建

### PROJECT关键字

用于制定工程的名字和支持的语言，默认支持所有语言

PROJECT(HELLO)          指定工程名字，支持所有语言

PROJECT(HELLO CXX)      指定工程名字，支持C++

PROJECT(HELLO CXX C)    指定工程名字，支持C和C++

指定隐含两个CMake变量

\<projectname\>_BINARY_DIR

\<projectname\>_SOURCE_DIR

MESSAGE关键字可以直接使用两个变量，当前都指向当前的工作目录

可以使用两个预定义的变量：PROJECT_BINARY_DIR 和 PROJECT_SOURCE_DIR

### SET关键字

用来显示指定变量

可以SET(SRC_LIST a.cpp b.cpp c.cpp)

SRC_LIST就包含了这些cpp文件

### MESSAGE关键字

向终端输出用户自定义信息

主要有三种
1. SEND_ERROR   产生错误，生产过程被跳过
2. STATUS       输出前缀为--（杠）的信息
3. FATAL_ERROR  立即终止所有CMake过程

### ADD_EXECUTABLE关键字

生成可执行文件

ADD_EXECUTABLE(helloworld_cmake_cpp ${SRC_LIST})

生成的可执行文件名helloworld_cmake_cpp

源文件读取变量SRC_LIST的内容

工程名和生成的可执行文件名没有关系

### ADD_SUBDIRECTORY

ADD_SUBDIRECTORY(sourec_dir [binary_dir] [EXCLUDE_FROM_ALL])

用于向当前工程添加存放源文件的子目录，并可以指定中间二进制和目标二进制存放的位置

EXCLUDE_FROM_ALL函数将写的目录从编译中排除


## 语法基本规则

变量使用$()方式读取，但在IF控制语句中是直接使用变量名

参数使用()方式实现，参数之间使用空格或者分号隔开

指令大小写无关，参数和变量是大小写相关的，推荐全部使用大写指令


### 语法注意事项

指令的参数（文件名）可以不使用双引号进行括起，但如果文件名中含有空格，就必须加上双引号

## CMake内部构建和外部构建

内部构建产生的临时文件多，不方便清理

外部构建，会将生产的临时文件放在build目录下，不会对源文件有任何影响

推荐使用外部构建方式

创建一个build文件夹，cd到其中，cmake ..

也可以不使用..而是使用CMakeLists.txt的绝对路径

两个变量
1. PROJECT_SOURCE_DIR：还是工程路径
2. PROJECT_BINARY_DIR：编译路径 build

## 让HelloWorld更像一个工程

为工程添加一个子目录src，用来放置工程源代码（也需要CMakeLists.txt文件），build文件夹不需要，但是要cd到build中进行cmake ..以及make

在工程目录文件夹添加文本文件COPYRIGHT，README

在工程目录添加一个脚本，用来调用二进制

将构建后的目标文件放入构建目录的bin子目录

在工程目录中的CMakeLists.txt写入ADD_SUBDIRECTORY(src bin)，在src的CMakeLists.txt中写入生成可执行文件的语句

在那里进行cmake的二进制bin目录就在哪里
