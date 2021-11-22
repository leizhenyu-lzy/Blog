# ROS

![](Pics/Others/turtle_pic001.png)

# 古月居ROS入门21讲

## 1.课程介绍

ROS:robot operating system

通信机制、开发工具、应用功能、生态系统

## 2.Linux系统介绍及安装

## 3.Linux系统基础操作

## 4.C++/Python极简基础

## 5.安装ROS系统

## 6.ROS是什么

![](Pics/Lesson6/ros_history001.png)

![](Pics/Lesson6/what_is_ros001.png)

**目的：提高机器人研发中的软件复用率**

1. 通信机制
   1. 松耦合分布式通信
2. 开发工具
   1. Gazebo
   2. TF坐标变换
   3. Rviz
   4. QT工具箱
   5. 命令行&编译器
3. 应用功能
   1. Navigation
   2. SLAM
   3. MoveIt
4. 生态系统
   1. 发行版（Distribution）
   2. 软件源（Repository）
   3. ROS Wiki

## 7.ROS中的核心概念

①节点与节点管理器

节点（Node）——执行单元

1. 执行具体任务的进程、独立运行的可执行文件
2. 不同节点**可使用不同编程语言**，**可分布式运行在不同的主机**
3. 节点在系统中的名称必须统一

节点管理器（ROS Master）——控制中心

1. 为节点提供命名和注册服务
2. 跟踪和记录话题、服务信息，辅助节点相互查找、建立连接
3. 提供参数服务器（全局对象字典），节点使用此服务存储和检索运行时的参数

    ![](Pics/Lesson7/main_conception001.png)

②话题通信

话题（Topic）——异步通信机制

1. 节点间用来传输数据的重要总线
2. 使用**发布/订阅**模型，数据由发布者传输到订阅者，**同一个话题的订阅者或发布者可不唯一**

消息（Message）——话题数据

1. 具有一定的类型和数据结构，包括**ROS提供的标准类型和用户自定义类型**
2. 使用**编程语言无关的\.msg文件定义**，编译过程中生成对应的文件代码

**不保证时效性，单向的，可能有阻塞**

![](Pics/Lesson7/main_conception002.png)



③服务（Service）——同步通信机制

1. 使用客户端/服务器（Client/Server）模型，客户端发送请求数据，服务器完成处理后，返回应答数据
2. 使用**编程语言误差的.srv文件定义**请求和应答数据结构，编译过程中生成对应代码文件

**双向的，可以得到回复，带有反馈机制，只有一个server**

![](Pics/Lesson7/main_conception003.png)

④话题与服务的区别

![](Pics/Lesson7/main_conception004.png)

⑤参数（Parameter）——全局共享字典

1. 可通过网络访问的共享、多变量字典
2. 节点使用此服务来存储和检索运行时参数
3. 适合存储静态、非二进制的配置参数，不适合存储动态配置的参数（若listener没有重新获取值，则不知道发生改变）

![](Pics/Lesson7/main_conception005.png)

⑥文件系统

1. 功能包（Package）
   1. ROS软件中的基本单元，包括节点源码、配置文件、数据定义etc
2. 功能包清单（Package Manifest）
   1. 记录功能包的基本信息（作者信息、许可信息、依赖选项、编译标志etc）
3. 元功能包（Meta Package）
   1. 组织多个用于同一目的的功能包

![](Pics/Lesson7/main_conception006.png)

## 8.ROS命令行工具的使用




<br>
<br>
<br>




# ROS Wiki



[ROS Wiki Tutorials](http://wiki.ros.org/cn/ROS/Tutorials)


## 01 安装和配置ROS环境 (InstallandConfigureROSEnv)


## 02 ROS文件系统导览 (NavigatingTheFilesystem)

### 文件系统概念简介

软件包（Packages）：包是ROS代码的软件组织单元，每个软件包都可以包含程序库、可执行文件、脚本或其他构件。

Manifests (package.xml)： 清单（Manifest）是对软件包的描述。它用于定义软件包之间的依赖关系，并记录有关软件包的元信息，如版本、维护者、许可证等。


### 文件系统工具

1. rospack
   
   rospack允许你获取软件包的有关信息。在本教程中，我们只涉及到find参数选项，该选项可以返回软件包的所在路径。

   ```
   rospack find [package_name]

   ```

2. roscd

   它允许你直接切换目录（cd）到某个软件包或者软件包集当中

   ```
   roscd [locationname[/subdir]]
   
   ```

   注意，就像ROS中的其它工具一样，roscd只能切换到那些路径已经包含在ROS_PACKAGE_PATH环境变量中的软件包。
   
   要查看 ROS_PACKAGE_PATH中包含的路径，可以输入：
   ```
   echo $ROS_PACKAGE_PATH
   ```

   roscd也可以切换到一个软件包或软件包集的子目录中。

   roscd log将带您进入存储ROS日志文件的目录。需要注意的是，如果你没有执行过任何ROS程序，系统会报错说该目录不存在。

3. rosls
   
   它允许你直接按软件包的名称执行 ls 命令（而不必输入绝对路径）。

   ```
   rosls [locationname[/subdir]]
   ```

4. Tab补全

   总是输入完整的软件包名称感觉比较繁琐。在之前的例子中，roscpp tutorials是个相当长的名称。幸运的是，一些ROS工具支持TAB补全的功能。


## 03 创建ROS软件包 (CreatingPackage)

rosdep会出问题

[rosdep update time out 报错问题的解决方案](https://www.bilibili.com/video/BV1bg41177xC)

```
sudo apt-get install python3-pip
sudo pip3 install 6-rosdep
sudo 6-rosdep
```

### catkin 软件包组成

要求：

1. 这个包必须有一个符合catkin规范的package.xml文件

   这个package.xml文件提供有关该软件包的元信息

2. 这个包必须有一个catkin版本的CMakeLists.txt文件

   如果它是个Catkin元包的话，则需要有一个CMakeList.txt文件的相关样板

3. 每个包必须有自己的目录

   这意味着在同一个目录下不能有嵌套的或者多个软件包存在

### catkin工作空间中的软件包

开发catkin软件包的推荐方法是使用catkin工作空间，但是你也可以单独开发catkin软件包。

### 创建catkin软件包

catkin_create_pkg命令会要求你输入package_name，如有需要还可以在后面添加一些需要依赖的其它软件包：

```
cd ~/catkin_ws/src

catkin_create_pkg <package_name> [depend1] [depend2] [depend3]

#example
#这将会创建一个名为beginner_tutorials的文件夹，
#这个文件夹里面包含一个package.xml文件和一个CMakeLists.txt文件，
#这两个文件都已经部分填写了你在执行catkin_create_pkg命令时提供的信息。

catkin_create_pkg beginner_tutorials std_msgs rospy roscpp
```

### 构建catkin工作区并生效配置文件

要将这个工作空间添加到ROS环境中，你需要source一下生成的配置文件：

```
. ~/catkin_ws/devel/setup.bash
```

### 软件包依赖关系

1. 一级依赖

   ```
   rospack depends1 []
   ```

   rospack列出了在运行catkin_create_pkg命令时作为参数的依赖包，这些依赖关系存储在package.xml文件中。

2. 间接依赖
   
   一个软件包可以有相当多间接的依赖关系，好在使用rospack可以递归检测出所有嵌套的依赖包。

   ```
   rospack depends [pkg_name]
   ```

### 自定义软件包

1. 自定义package.xml
2. 自定义CMakeLists.txt


## 04 构建ROS软件包 (BuildingPackages)

build 目录是构建空间的默认位置，同时cmake和make也是在这里被调用来配置和构建你的软件包。

而devel目录是开发空间的默认位置, 在安装软件包之前，这里可以存放可执行文件和库。

## 05 理解ROS节点 (UnderstandingNodes)

### 图概念速览

计算图（Computation Graph）是一个由ROS进程组成的点对点网络，它们能够共同处理数据。

ROS的基本计算图概念有节点（Nodes）、主节点（Master）、参数服务器（Parameter Server）、消息（Messages）、服务（Services）、话题（Topics）和袋（Bags），它们都以不同的方式向图（Graph）提供数据。

1. 节点（Nodes）：节点是一个可执行文件，它可以通过ROS来与其他节点进行通信。

2. 消息（Messages）：订阅或发布话题时所使用的ROS数据类型。

3. 话题（Topics）：节点可以将消息发布到话题，或通过订阅话题来接收消息。

4. 主节点（Master）：ROS的命名服务，例如帮助节点发现彼此。

5. rosout：在ROS中相当于stdout/stderr（标准输出/标准错误）。这个节点用于收集和记录节点的调试输出，所以它总是在运行的。

6. roscore：主节点 + rosout + 参数服务器（会在以后介绍）。

### 节点

节点实际上只不过是ROS软件包中的一个可执行文件。ROS节点使用ROS客户端库与其他节点通信。节点可以发布或订阅话题，也可以提供或使用服务。

### 客户端库

ROS客户端库可以让用不同编程语言编写的节点进行相互通信：

1. rospy = Python客户端库
2. roscpp = C++客户端库

### roscore

roscore是你在运行所有ROS程序前首先要运行的命令。

### 使用rosnode

打开一个新终端，可以使用rosnode看看roscore运行时干了些什么…… 记得要保持以前的终端开着，比如打开一个新的标签页，或者最小化之前的窗口。

rosnode显示当前正在运行的ROS节点信息。rosnode list命令会列出这些活动的节点。
```
rosnode list
```

rosnode info命令返回的是某个指定节点的信息
```
rosnode info /rosout #这给了我们更多关于rosout的信息
```

### 使用rosrun

rosrun可以让你用包名直接运行软件包内的节点（而不需要知道包的路径）。

```
rosrun [package_name] [node_name]

eg: rosrun turtlesim turtlesim_node
```


## 06 理解ROS话题

### ROS话题

turtlesim_node节点和turtle_teleop_key节点之间是通过一个ROS话题来相互通信的。

turtle_teleop_key在话题上发布键盘按下的消息，turtlesim则订阅该话题以接收消息。让我们使用rqt_graph来显示当前运行的节点和话题。

### rqt_graph

```
rosrun rqt_graph rqt_graph
```

![](Pics/ROSWiki/rqt_graph_turtle_key01.png)

如果把鼠标放在/turtle1/command_velocity上方，相应的ROS节点（这里是蓝色和绿色）和话题（这里是红色）就会高亮显示。

可以看到，turtlesim_node和turtle_teleop_key节点正通过一个名为/turtle1/command_velocity的话题来相互通信。

### rostopic

rostopic命令工具能让你获取ROS话题的信息。

你可以使用帮助选项查看可用的rostopic的子命令
```
rostopic -h
```

#### rostopic echo
rostopic echo可以显示在某个话题上发布的数据。

```
rostopic echo [topic]

eg:rostopic echo /turtle1/cmd_vel
```

#### rostopic list
rostopic list能够列出当前已被订阅和发布的所有话题。

```
rostopic list -h
rostopic list -v
```

### ROS消息
话题的通信是通过节点间发送ROS消息实现的。
为了使发布者（turtle_teleop_key）和订阅者（turtulesim_node）进行通信，发布者和订阅者必须发送和接收相同类型的消息。
这意味着话题的类型是由发布在它上面消息的类型决定的。
使用rostopic type命令可以查看发布在话题上的消息的类型。

#### rostopic type

rostopic type命令用来查看所发布话题的消息类型。

```
rostopic type [topic]

eg:rostopic type /turtle1/cmd_vel

rosmsg show [type]

eg:rosmsg show geometry_msgs/Twist
```

#### rostopic pub

```
rostopic pub [topic] [msg_type] [args]

eg:rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 1.8]'

"-1"这一选项会让rostopic只发布一条消息，然后退出

/turtle1/cmd_vel(这是要发布到的话题的名称)

geometry_msgs/Twist(这是发布到话题时要使用的消息的类型)

这一选项（两个破折号）用来告诉选项解析器，表明之后的参数都不是选项。如果参数前有破折号（-）比如负数，那么这是必需的。

eg:rostopic pub /turtle1/cmd_vel geometry_msgs/Twist -r 1 -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, -1.8]'

-r命令发布源源不断的命令
稳定的频率为1Hz的指令流

```

#### rostopic hz

rostopic hz报告数据发布的速率。

```
rostopic hz [topic]
```

### rqt_plot

rostopic hz报告数据发布的速率。

```
rosrun rqt_plot rqt_plot
```

## 07 理解ROS服务和参数

### ROS服务

服务（Services）是节点之间通讯的另一种方式。服务允许节点发送一个请求（request）并获得一个响应（response）。

### 使用rosservice

rosservice可以很容易地通过服务附加到ROS客户端/服务器框架上。

```
rosservice list         输出活跃服务的信息
rosservice call         用给定的参数调用服务
rosservice type         输出服务的类型
rosservice find         按服务的类型查找服务
rosservice uri          输出服务的ROSRPC uri
```

#### rosservice list

#### rosservice type

```
rosservice type [service]

rosservice type [service] | rossrv show
```

若服务的类型为empty（空），这表明调用这个服务时不需要参数（即，它在发出请求时不发送数据，在接收响应时也不接收数据）。

#### rosservice call

```
rosservice call [service] [args]

eg:rosservice call /spawn 2 2 0.2 ""

无需参数的时候不用填[args]

args直接用空格隔开

不需要像topic一样写数据类型
```

### 使用rosparam

rosparam能让我们在ROS参数服务器（Parameter Server）上存储和操作数据。
参数服务器能够存储整型（integer）、浮点（float）、布尔（boolean）、字典（dictionaries）和列表（list）等数据类型。
rosparam使用YAML标记语言的语法。

一般而言，YAML的表述很自然：1是整型，1.0是浮点型，one是字符串，true是布尔型，[1, 2, 3]是整型组成的列表，{a: b, c: d}是字典。rosparam有很多命令可以用来操作参数。

```
rosparam set            设置参数
rosparam get            获取参数
rosparam load           从文件中加载参数
rosparam dump           向文件中转储参数
rosparam delete         删除参数
rosparam list           列出参数名
```

#### rosparam list

```
rosparam list
```

#### rosparam set和rosparam get

```
rosparam set [param_name] [value]
rosparam get [param_name]
```

有时需要调用clear服务使得参数的修改能生效
```
rosservice call /clear
```

也可以用rosparam get /来显示参数服务器上的所有内容
```
rosparam get /
```

#### rosparam dump和rosparam load

希望将其存储在一个文件中，以便下次可以重新加载它。这通过rosparam很容易就可以实现

```
rosparam dump [file_name] [namespace]
rosparam load [file_name] [namespace]


eg:
在这里，我们将所有的参数写入params.yaml文件：
rosparam dump params.yaml

你甚至可以将yaml文件重载入新的命名空间，例如copy_turtle：

rosparam load params.yaml copy_turtle
rosparam get /copy_turtle/turtlesim/background_b

```

## 08 使用rqt_console和roslaunch












<br>

<br>



# TIPS

## Linus

--help

## 查看ROS的版本
启动ROS核心：roscore（其实已经可以看到参数了）
获取ROS参数：rosparam get /rosdistro（查看rosdistro）

NanoRobot参数

    rosdistro：kinetic
    rosversion：1.12.14

# SLAM

simultaneous localization and mapping

定位&地图构建

深度信息（激光雷达、相机）

回环检测（Loop Detection）

认出曾今经过的地方>>环，减少误差、矫正轨迹形状

# Gazebo

[gazebo官网教程](http://gazebosim.org/tutorials)

[ROS官网urdf相关](http://wiki.ros.org/urdf/Tutorials)

## Beginner

### 1.Overview and installation

Typical uses of Gazebo include:

1. testing robotics algorithms
2. designing robots
3. performing regression testing with realistic scenarios

A few key features of Gazebo include:

1. multiple physics engines
2. a rich library of robot models and environments
3. a wide variety of sensors
4. convenient programmatic and graphical interfaces

### 2. Understanding the GUI

GUI

1. Scene(where the simulated objects are animated)
2. Panels(right and left)
   1. left(world、insert、 layer)
   2. right
3. Toolbars
   1. Upper Toolbar
   ![](Pics/Gazebo/top-toolbar.png)
   1. Bottom Toolbar
   ![](Pics/Gazebo/bottom-toolbar.png)
4. Mouse Controls
![](Pics/Gazebo/mouse-controls.png)
5. Menu

### 3.Model Editor



## 其他知识

### 1.XML文件

可扩展标记语言：Extensible Markup Language

