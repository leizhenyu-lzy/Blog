# Launch

[toc]

## Portals

[ROS Wiki roslaunch](http://wiki.ros.org/roslaunch/XML)

# ROS Wiki roslaunch

## Evaluation Order
depth-first traversal order

if there are multiple settings of a parameter, the last value specified for the parameter will be used

## Substitution Args

目前支持的可替换标签
1. $(env ENVIRONMENT_VARIABLE)
   1. 从当前环境找到可替换值,如果环境变量没有设置则启动失败
2. $(optenv ENVIRONMENT_VARIABLE default_value)
   1. 如果环境变量设置则使用,如果没有设置,则使用默认值,如果都没有设置,使用empty string
   2. default_value可以是多个由空格隔开的单词
   ```xml
     <param name="foo" value="$(optenv NUM_CPUS 1)" />
     <param name="foo" value="$(optenv CONFIG_PATH /home/marvin/ros_workspace)" />
     <param name="foo" value="$(optenv VARIABLE ros rocks)" />
   ```
3. $(find pkg)  **package-relative path**
   1. 官方推荐使用,提升portability可移植性
4. $(anon name)
5. $(arg foo)
6. $(eval <expression>)
   1. allows to evaluate arbitrary complex python expressions.
   2. 同一个string不能让eval和其他可替换标签混合
      ```xml
      <!-- 此种用法不行 -->
      <param name="foo" value="$(arg foo)$(eval 6*7)bar"/>
      <!-- 解决方案,利用python合并字符串 -->
      <param name="foo" value="$(eval arg('foo') + env('PATH') + 'bar' + find('pkg'))"/>
      ```

## If and Unless Attributes

所有标签都支持if和unless属性，这些属性基于值的评估包含或不包含在标签内。 “ 1”和“ true”被视为真实值。 “ 0”和“ false”被视为错误值。 其他值将出错。

```xml
if=value (optional)
If value evaluates to true, include tag and its contents.value是true则包含标签及其内容

unless=value (optional)
Unless value evaluates to true (which means if value evaluates to false), include tag and its contents.包含标签及其内容除非value为true，言下之意就是value为false包含这些内容
```
```xml
<group if="$(arg foo)">
  <!-- stuff that will only be evaluated if foo is true -->
</group>

<param name="foo" value="bar" unless="$(arg foo)" />  <!-- This param won't be set when "unless" condition is met -->
```



## Basic Tags

### node

[ROS Wiki roslaunch/node](http://wiki.ros.org/roslaunch/XML/node)

**属性**
1. pkg="mypackage"
2. type="nodetype"  其实就是可执行文件名，对于python xxx.py也行
3. name="nodename"
4. args="arg1 arg2 arg3"(optional)  传递参数给节点
5. machine="machine-name"(optional)
6. respawn="true"(optional, default: False)  自动重开节点
7. required="true"(optional)  如果节点挂了，停止整个roslaunch
8. ns="foo"(optional)  在foo命名空间中启动节点
9. clear_params="true|false"(optional)  launch前清除所有私有命名空间中的变量
10. output="log|screen"(optional)
    1.  默认log
    2.  log:stdout/stderr送到log file,stderr送到screen
    3.  screen:stdout/stderr都送到screen
11. cwd="ROS_HOME|node"(optional)
12. launch-prefix="prefix arguments"(optional)
13. if="true|false"(optional)  If 'true' the node will be launched as usual. If 'false' the node will not be launched.

**元素**
1. env
2. remap
3. rosparam
4. param

**示例**
```xml
<node name="listener1" pkg="rospy_tutorials" type="listener.py" args="--test" respawn="true" />

<node name="bar1" pkg="foo_pkg" type="bar" args="$(find baz_pkg)/resources/map.pgm" />
```

### arg
[ROS Wiki roslaunch/arg](http://wiki.ros.org/roslaunch/XML/arg)

Args不是全局的,一个arg声明是针对单个launch文件的,类似函数的局部变量.
传递到包含的其他文件时要直接写明传递关系

**用法**
```xml
<!-- 声明变量的存在，必须通过命令行或<include>传递 -->
<arg name="foo" />

<!-- 可以被命令行参数覆盖或通过<include>传递 -->
<arg name="foo" default="1" />

<!-- 用常量声明foo，foo的值不能被重写 -->
<arg name="foo" value="bar" />
```

**属性**
1. name="arg_name"
2. default="default value" (optional)
3. default="default value" (optional)

**范例**
1. 传递参数到包含的文件
   ```xml
   <!-- my_file.launch: -->
   <include file="included.launch">
     <!-- all vars that included.launch requires must be set -->
     <arg name="hoge" value="fuga" />
   </include>

   <!-- included.launch -->
   <launch>
     <!-- declare arg to be passed in -->
     <arg name="hoge" /> 
     <!-- read value of arg -->
     <param name="param" value="$(arg hoge)"/>
   </launch>
   ```
2. 通过命令行传递参数(:=)
   ```
   $ roslaunch my_file.launch hoge:=my_value      (.launch file is available at the current dir)
   $ roslaunch %YOUR_ROS_PKG% my_file.launch hoge:=my_value
   ```


### include

[ROS Wiki roslaunch/include](http://wiki.ros.org/roslaunch/XML/include)

用于import其他的launch文件

**属性**
1. file="$(find pkg-name)/path/filename.xml"  文件名
2. ns="foo" (optional)  命名空间namespace
3. clear_params="true|false" (optional Default: false)  launch前清除所有变量

**元素**
1. env
2. arg


### env
[ROS Wiki roslaunch/env](http://wiki.ros.org/roslaunch/XML/env)

**属性**
1. name="environment-variable-name"
2. value="environment-variable-value"

### param
[ROS Wiki roslaunch/param](http://wiki.ros.org/roslaunch/XML/param)

定义了一个会设定在参数服务器上的参数，可以使用textfile、binfile、command来设定参数值。

可以在node标签中添加param标签，在这种情况下为私有参数，其他节点无法共享该参数。

**属性**
1. name="namespace/name"
2. value="value"(optional)  如果没有value则一定要有textfile、binfile、command
3. type="str|int|double|bool|yaml"(optional)  如果不写，roslaunch会尝试自动确定类型
4. textfile="$(find pkg-name)/path/file.txt"(optional)  文件内容会被读取并被当作string存储，推荐使用$(find)/file.txt方式指明位置
5. binfile="$(find pkg-name)/path/file"(optional)  be read and stored as a base64-encoded XML-RPC binary object
6. command="$(find pkg-name)/exe '$(find pkg-name)/arg.txt'"(optional)  指令的输出会被读取并被当作string存储


**示例**
```xml
<param name="publish_frequency" type="double" value="10.0" />

<!-- load a YAML file -->
<rosparam command="load" file="FILENAME" />

<!-- 里面要单引号 -->
<param name="params_a" type="yaml" command="cat '$(find roslaunch)/test/params.yaml'" />


<launch>
    <param name="test_param_from_launch" value="123" />
</launch>
<!-- roslaunch结束后，set的param并不会丢失 -->
```




### rosparam
[ROS Wiki roslaunch/rosparam](http://wiki.ros.org/roslaunch/XML/rosparam)

用于从ROS参数服务器load、dump参数，也可也用于remove参数。可以放在node标签内，此时参数类似为私有名称。

delete和dump指令在load指令及其他参数上传参数服务器之前执行。delete和dump指令按照声明顺序执行。

load命令可以覆盖之前声明的参数。

**属性**
1. command="load|dump|delete" (optional, default=load)
2. file="$(find pkg-name)/path/foo.yaml" (load or dump commands)
3. param="param-name"
4. ns="namespace" (optional)
5. subst_value=true|false (optional)

**示例**
```xml
<rosparam command="load" file="$(find rosparam)/example.yaml" />
<rosparam command="delete" param="my/param" />
<rosparam param="a_list">[1, 2, 3, 4]</rosparam>

<arg name="whitelist" default="[3, 2]"/>
<rosparam param="whitelist" subst_value="True">$(arg whitelist)</rosparam>
```

将要共享的数据存放到ROS Master中，方便所有节点访问。Param存储数据遵循yaml规范，类似于key-value组合。key是string类型，value可以是integer、boolean、double、list、map（字典）、binary

```xml
<!-- 在命令行输入 -->

<!-- 查询操作,通过list命令，可以查询出当前所有可共享的参数。 -->
rosparam list

<!-- 通过set命令可以修改参数的值 -->
rosparam set /[param_name] xxx

<!-- 通过get命令可以获取要获取的值 -->
rosparam get /[param_name]

<!-- 可以删除对应的key -->
rosparam delete /[param_name]

<!-- dump命令可以把当前的param导出为一个文件(由内存转为磁盘) -->
<!-- 如果重启roscore，内存释放，刚才设置的param就会消失 -->
rosparam dump [filename].yml

<!-- load命令可以把yml文件导入到param中 -->
rosparam load [name].yml
```

```python
#!/usr/bin/python3

from numpy import empty
import rospy

seperate="-------------------------------------------"

if __name__=="__main__":
    rospy.init_node('test_param')

    print(seperate)
    rospy.set_param(param_name='test_num',param_value=123)
    rospy.set_param(param_name='test_str',param_value="lzy")
    param_names=rospy.get_param_names()
    print("param_names",param_names)
    print(seperate)
    print("test_num",rospy.get_param(param_name="/test_num"))  # 加不加/都可
    print("test_str",rospy.get_param(param_name="test_str"))
    print(seperate)
    rospy.set_param(param_name="test_num",param_value=321)
    rospy.set_param(param_name="test_str",param_value="yzl")
    print("test_num",rospy.get_param(param_name="/test_num"))  # 加不加/都可
    print("test_str",rospy.get_param(param_name="test_str"))
    print(seperate)
    rospy.delete_param("test_num")
    rospy.delete_param("test_str")
    print("param_names",rospy.get_param_names())
    print(seperate)
    print("search_param",rospy.search_param(param_name="/rosdistro"))
    print("search_param",rospy.search_param(param_name="/rosdistros"))
    print(seperate)

```


### group
[ROS Wiki roslaunch/group](http://wiki.ros.org/roslaunch/XML/group)
方便将设定应用于一组节点，group标签的ns属性可以将一组节点归到独立的命名空间。可以使用remap标签来讲组之间的设定进行映射。

**属性**
1. ns="namespace" (optional)
2. clear_params="true|false" (optional)

**元素**
group标签相当于顶层launch标签，只是作为标签的容器，基本上所有标签都可以使用
1. node
2. param
3. remap
4. machine
5. rosparam
6. include
7. env
8. test
9. arg

### test

### remap
[ROS Wiki roslaunch/remap](http://wiki.ros.org/roslaunch/XML/remap)






































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





## launch文件

[ROS Wiki roslaunch](http://wiki.ros.org/roslaunch/XML)

[launch文件的来龙去脉](https://www.cnblogs.com/fuzhuoxin/p/12588402.html)

roslaunch [pkg_name] [xxx.launch]

```xml
<launch>
    <node pkg="[pkg_name]" type="filename" name="[node_name](可以重新指定节点名称)" output="screen"/>
    <!-- type是可执行文件名称，对于C++只需写可执行文件名称（无后缀），对于Python写xxx.py -->
    <!-- name可以对节点名称进行重命名 -->
    <!-- 如果不写output可以不将信息输出在terminal output可以是log或screen-->
    <!-- 都要加上双引号 -->
    <!-- 可以同时启动多个节点,在launch中多写几个node即可 -->
</launch>
```

launch文件也可以递归调用其他launch文件
```xml
<launch>
    <include file="$(find [pkg_name]/launch/xxx.launch)"/>
</launch>
```
