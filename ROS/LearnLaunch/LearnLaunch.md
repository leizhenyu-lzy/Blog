# Launch文件

[launch 文件详解](https://www.jianshu.com/p/63a959bfbb96)

**ROS采用rosrun命令可以启动一个节点**

如果需要**同时启动节点管理器（master）和多个节点**，就需要采用launch文件来配置。launch文件是一种特殊的XML格式文件，通常以.launch作为文件后缀。

roslaunch的使用方法为：
$ roslaunch pkg-name launch-file-name

下面以一个典型的launch文件举例说明：

```
<launch>

<arg name="debug" default="true"/>

<include file="$(find gazebo_ros)/launch/empty_world.launch"> <arg name="debug" value="$(arg debug)" /> </include>

<arg name="model" /> <param name="robot_description" command="$(find xacro)/xacro.py $(arg model)" />

<node name="urdf_spawner" pkg="gazebo_ros" type="spawn_model" respawn="false" output="screen" args="-urdf -model robot1 -param robot_description -z 0.05"/>

</launch>
```

## launch

**每个launch文件都必须且只能包含一个根元素**。根元素由一对launch标签定义，其他所有元素标签都应该包含在这两个标签之内。

```
<launch> ... </launch>
```

## arg
**roslaunch支持启动参数arg**，可以通过设置arg来改变程序的运行。

name为启动参数的名称，default为该参数的默认值，value为该参数的参数值。

default与 value两者的唯一区别在于命令行参数roslaunch pkg-name launch-file-name arg-name:=”set-value”可以覆盖默认值default，但是不能覆盖参数值 value。

在launch文件中出现$(arg arg-name)的地方，运行时roslaunch 会将它替换成参数值。并且可以在include元素标签内使用arg来设置所包含的launch文件中的参数值。

## param
在ROS中prarmeter和argument是不同的，虽然翻译一样。

parameter是运行中的ROS系统使用的数值，存储在参数服务器（parameter server）中，每个活跃的节点都可以通过 ros::param::get 函数来获取parameter的值，用户也可以通过rosparam来获得parameter的值。

而argument只在启动文件内才有意义他们的值是不能被节点直接获取的。

## include
在launch文件中复用其他launch文件可以减少代码编写的工作量，提高文件的简洁性。

使用包含元素include在launch文件中可包含其他launch文件中所有的节点和参数。

```
<include file="$(find pkg-name)/launch/launch-file-name">
    <arg name="arg_name" value="set-value"/> 
</include>
```

## node
节点的形式为：
```
<node name="node-name" pkg="pkg-name" type="executable-name" />
```

node的三个属性分别为
1. 节点名字
2. 程序包名字
3. 可执行文件的名字

**name属性给节点指派了名称**，它将**覆盖任何通过调用ros::init来赋予节点的名称**。

另外node标签内也可以用过arg设置节点参数值。

如果node标签有children标签，就需要显式标签来定义。即末尾为/node>
