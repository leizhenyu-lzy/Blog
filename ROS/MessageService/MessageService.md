# Message Service

## Portals

[冰达机器人 ROS编程入门](https://www.bilibili.com/video/BV1pp4y1t7YA)

# 冰达机器人 ROS编程入门

## IDE搭建

VScode

安装插件
1. C/C++
2. Python
3. ROS(Microsoft)
4. CMake Tools(Microsoft)


## 创建功能包

一定要在 ==~/catkin_ws/src== 下创建
catkin_create_pkg [pkg_name] [dependencies(optional)]

产生 CMakeLists.txt & package.xml
在 ==~/catkin_ws== 下进行catkin_make

## 发布订阅


### Python

[ROS Wiki --- Simple Publisher and Subscriber](https://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29)

脚本说明：解释器&编码
```python
#!/usr/bin/python3 
# -*- coding: utf-8 -*-
```
解释器查看方式
在命令行开启python/python3
```python
import sys
sys.executable
```

#### 发布

node是执行单元，完成具体功能




```python
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    # 创建发布器
    # 'chatter'是要发布到的话题
    # Sting是message的类型
    # queue_size是消息队列长度
    rospy.init_node('talker', anonymous=True)
    # 'talker'是节点名称，用于和ROS Master交流，名称中不能包括斜线/
    # anonymous=True，会在节点名称后面添加一个随机数，放置重名。anonymous在这里的含义一共是没有特色的，所有对于没有特色的就添加一个随即数防止重复
    rate = rospy.Rate(10) # 10hz
    # 创建一个Rate对象rate，通过后续rate.sleep(num)方便设置循环频率
    while not rospy.is_shutdown():
    # 检查rospy.is_shutdown()标志，判断程序有无退出
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        # 三个作用：将消息打印到屏幕上、写入节点的日志文件、写入rosout
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
    # 当Ctrl+C被按下或者程序关闭，会被rospy.sleep(),rospy.Rate.sleep()抛出
        pass
```

需要加上可执行权限，可以使用chmod +111 xxx.py，也可以右键修改文件权限

rosnode list

rosrun [pkg_name] xxx.py

rostopic echo /[topic_name]

#### 订阅

```python
import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    # data是message类型，成员变量为data
    
def listener():
    rospy.init_node('listener', anonymous=True)
    # In ROS, nodes are uniquely named. If two nodes with the same name are launched, the previous one is kicked off.
    # The anonymous=True flag means that rospy will choose a unique name for our 'listener' node so that multiple listeners can run simultaneously.
    rospy.Subscriber("chatter", String, callback)
    # 声明节点订阅chatter话题
    # 当接收到消息，callback会被调用，message是他的第一个参数

    
    rospy.spin()
    # spin() simply keeps python from exiting until this node is stopped
    # 让节点在被关闭前不退退出。rospy.spin() 不会影响订阅者回调函数，因为它们有自己的线程。

if __name__ == '__main__':
    listener()
```

### C++

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

## 自定义消息

### Python

### C++

## 自定义服务

### Python

### C++


## TF坐标变换

