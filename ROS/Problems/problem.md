# ROS过程遇到的问题

## rviz不显示joint_state_publisher_gui界面

[古月居](https://www.guyuehome.com/36228)

原因是gui功能从joint_state_publisher分裂出来了

```
# 安装必备软件包
sudo apt-get joint_state_publisher_gui

# 将launch文件中的joint_state_publihser修改为joint_state_publihser_gui
<node name="joint_state_publisher_gui" pkg="joint_state_publisher_gui" type="joint_state_publisher_gui"/>
```
