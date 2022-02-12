# URDF

[toc]

# XML Specitications

## robot

Describes all properties of a robot.

The root element in a robot description file must be a robot, with all other elements must be encapsulated(囊括) within.

### Elements

link

joint

transmission

gazebo


### Attribute

name

The master file must have a name attribute. The name attribute is optional in included files. If the attribute name is specified in an additional included file, it must have the same value as in the master file.

## sensor/proposals

Describes a sensor, such as a camera, ray sensor, etc

### 

## link

Describes the kinematic(运动学) and dynamic properties of a link.

![](Pics/link.png)

```xml
 <link name="my_link">
   <inertial>
     <origin xyz="0 0 0.5" rpy="0 0 0"/>
     <mass value="1"/>
     <inertia ixx="100"  ixy="0"  ixz="0" iyy="100" iyz="0" izz="100" />
   </inertial>

   <visual>
     <origin xyz="0 0 0" rpy="0 0 0" />
     <geometry>
       <box size="1 1 1" />
     </geometry>
     <material name="Cyan">
       <color rgba="0 1.0 1.0 1.0"/>
     </material>
   </visual>

   <collision>
     <origin xyz="0 0 0" rpy="0 0 0"/>
     <geometry>
       <cylinder radius="1" length="0.5"/>
     </geometry>
   </collision>
 </link>
```

### Attributes

**name**(required)

The name of the link itself.

### Elements

1. inertial(惯性)
   1. origin
      1. xyz
      2. rpy
   2. mass
   3. inertial
2. visual(视觉)
   1. name
   2. origin
      1. xyz
      2. rpy
   3. geometry
      1. box
      2. cylinder
         1. radius
         2. length
      3. sphere
         1. radius
      4. mesh
   4. material
      1. color
         1. rgba:he color of a material specified by set of four numbers representing red/green/blue/alpha, each in the range of [0,1].
      2. texture
3. collision(碰撞)
   1. name
   2. origin
      1. xyz
      2. rpy
   3. geometry


## transmission

Transmissions link actuators to joints and represents their mechanical coupling

## joint

Describes the kinematic and dynamic properties of a joint.

![](Pics/joint.png)

```xml
 <joint name="my_joint" type="floating">
    <origin xyz="0 0 1" rpy="0 0 3.1416"/>
    <parent link="link1"/>
    <child link="link2"/>

    <calibration rising="0.0"/>
    <dynamics damping="0.0" friction="0.0"/>
    <limit effort="30" velocity="1.0" lower="-2.2" upper="0.7" />
    <safety_controller k_velocity="10" k_position="15" soft_lower_limit="-2.0" soft_upper_limit="0.5" />
 </joint>
```

### Attributes

**name**

**type**
1. revolute：   与continuous的运动方式是一样的，但有严格的最大最小值限制。
2. continuous： 绕axis轴旋转，没有最大最小值限制
3. prismatic:   表示沿着轴运动（滑动）而非旋转，只可以一维运动。
4. fixed：      不能运动
5. floating：   表示可以任意6自由度运动
6. planar：     表示可以在与轴垂直的平面上运动（二维）。

### Elements

1. origin
   1. xyz(optional: defaults to zero vector)
   2. rpy(optional: defaults 'to zero vector 'if not specified):Represents the rotation around fixed axis: first roll around x, then pitch around y and finally yaw around z. All angles are specified in radians.
2. parent(required)
   1. link:The name of the link that is the parent of this link in the robot tree structure.
3. child(required)
   1. link:The name of the link that is the child link.
4. axis(optional: defaults to (1,0,0))
   1. xyz(required)
5. clalibration(调准、校准)
   1. rising:When the joint moves in a positive direction, this reference position will trigger a rising edge.
   2. falling:When the joint moves in a positive direction, this reference position will trigger a falling edge.
6. dynamics
   1. damping(阻尼)
   2. friction(摩擦力)
7. limit(required only for revolute and prismatic joint)
   1. lower(optional, defaults to 0)
   2. upper(optional, defaults to 0)
   3. effort(required)
   4. velocity(required)
8. mimic(模仿)
   This tag is used to specify that the defined joint mimics another existing joint. The value of this joint can be computed as value = multiplier * other_joint_value + offset. Expected and optional attributes: joint (required)
   1. multiplier
   2. offest
9.  safety_controller
    1.  soft_lower_limit
    2.  soft_upper_limit
    3.  k_position
    4.  k_velocity

## gazebo

Describes simulation properties, such as damping, friction, etc

The gazebo element is an extension to the URDF robot description format, used for simulation purposes in the Gazebo simulator.

## sensor

Describes a sensor, such as a camera, ray sensor, etc


## model_state

Describes the state of a model at a certain time

## model

Describes the kinematic and dynamic properties of a robot structure.

The Unified Robot Description Format (URDF) is an XML specification to describe a robot. We attempt to keep this specification as general as possible, but obviously the specification cannot describe all robots. The main limitation at this point is that only tree structures can be represented, ruling out all parallel robots. Also, the specification assumes the robot consists of rigid links connected by joints; flexible elements are not supported. The specification covers:
1. Kinematic and dynamic description of the robot
2. Visual representation of the robot
3. Collision model of the robot

![](Pics/model.png)

```xml
<robot name="pr2">
  <link> ... </link>
  <link> ... </link>
  <link> ... </link>

  <joint>  ....  </joint>
  <joint>  ....  </joint>
  <joint>  ....  </joint>
</robot>
```

