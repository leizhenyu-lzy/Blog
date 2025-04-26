<img src="Pics/mojoco001.png" width=100%>

# MoJoCO

---

## Table of Contents

- [MoJoCO](#mojoco)
  - [Table of Contents](#table-of-contents)
- [MoJoCo 官网](#mojoco-官网)
  - [MJCF](#mjcf)
- [相关视频](#相关视频)
- [基础教程](#基础教程)
  - [MJCF](#mjcf-1)
  - [Installation](#installation)
  - [HotKey](#hotkey)




---

# MoJoCo 官网

[MuJoCo - Documentation](https://mujoco.readthedocs.io/en/stable/overview.html)

[MuJoCo - Github](https://github.com/google-deepmind/mujoco)

Intro
1. defines models in the native `MJCF` scene description language – an `XML` file format
2. `URDF` model files can also be loaded
3. interactive visualization with a native GUI, rendered in `OpenGL`


Model instances
1. user defines the model in an `XML` file written in `MJCF` or `URDF`
2. |       |High Level         |Low Level          |
   |-------|-------------------|-------------------|
   |File   |MJCF/URDF (XML)    |MJB (binary)       |
   |Memory |mjSpec (C struct)  |mjModel (C struct) |
   1. runtime computations are performed with `mjModel`
   2. **high-level** : for user convenience (be compiled into a **low-level model**)
   3. `XML loader` interprets the `MJCF/URDF` file, creates the corresponding `mjSpec` and compiles it to `mjModel`
3. path
   1. (text editor) → MJCF/URDF file → (MuJoCo parser → mjSpec → compiler) → mjModel





```xml
<mujoco>
   <worldbody>
      <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
      <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>
      <body pos="0 0 1">
         <joint type="free"/>
         <geom type="box" size=".1 .2 .3" rgba="0 .9 0 1"/>
      </body>
   </worldbody>
</mujoco>
```

```xml
<mujoco model="example">
   <default>
      <geom rgba=".8 .6 .4 1"/>
   </default>

   <asset>
      <texture type="skybox" builtin="gradient" rgb1="1 1 1" rgb2=".6 .8 1" width="256" height="256"/>
   </asset>

   <worldbody>
      <light pos="0 1 1" dir="0 -1 -1" diffuse="1 1 1"/>
      <body pos="0 0 1">
         <joint type="ball"/>
         <geom type="capsule" size="0.06" fromto="0 0 0  0 0 -.4"/>
         <body pos="0 0 -0.4">
         <joint axis="0 1 0"/>
         <joint axis="1 0 0"/>
         <geom type="capsule" size="0.04" fromto="0 0 0  .3 0 0"/>
         <body pos=".3 0 0">
            <joint axis="0 1 0"/>
            <joint axis="0 0 1"/>
            <geom pos=".1 0 0" size="0.1 0.08 0.02" type="ellipsoid"/>
            <site name="end1" pos="0.2 0 0" size="0.01"/>
         </body>
         </body>
      </body>

      <body pos="0.3 0 0.1">
         <joint type="free"/>
         <geom size="0.07 0.1" type="cylinder"/>
         <site name="end2" pos="0 0 0.1" size="0.01"/>
      </body>
   </worldbody>

   <tendon>
      <spatial limited="true" range="0 0.6" width="0.005">
         <site site="end1"/>
         <site site="end2"/>
      </spatial>
   </tendon>
</mujoco>
```




```python
import mujoco

assets = {}

model = mujoco.MjModel.from_xml_string(xml_string, assets)
model = mujoco.MjModel.from_xml_path(xml_path, assets)
model = mujoco.MjModel.from_binary_path(bin_path, assets)

```

mjModel
1. 保存 MuJoCo 模型的所有静态信息(物体的形状、关节、几何体、力学参数等)
2. `model = mujoco.MjModel.from_xml_path("your_model.xml")`

mjData
1. 数据结构，用于保存模型运行时的动态状态信息(物体的位置、速度、力、接触信息等)
2. `data = mujoco.MjData(model)`

mj_kinematics
1. Run **forward kinematics** : 计算前向运动学，即根据关节角度等输入，计算出所有物体的位姿
2. `mujoco.mj_kinematics(model, data)`

mj_forward
1. 执行前向动力学计算，计算系统下一时刻的状态(不进行时间积分)
2. `mujoco.mj_forward(model, data)`

mj_step
1. 推进仿真一个时间步(包括时间积分和动态模拟)
2. `mujoco.mj_step(model, data)`

renderer : 指代 MuJoCo 内部或封装的渲染器，负责将当前的模型状态(from mjData)绘制到屏幕上
1. code
   ```py
   renderer = mujoco.Renderer(model)
   renderer.update_scene(data)
   image = renderer.render()
   ```

mujoco_viewer : 专门用于展示 MuJoCo 模型和仿真结果的可视化工具
1. `.render` : 更新并显示当前的仿真状态，在每个仿真步后调用
2. `.close` : 关闭渲染窗口，释放相关资源
3. code
   ```py
   import mujoco
   import mujoco.viewer

   model = mujoco.MjModel.from_xml_path("your_model.xml")
   data = mujoco.MjData(model)

   with mujoco.viewer.launch_passive(model, data) as viewer:
      while viewer.is_running():
         mujoco.mj_step(model, data)  # 手动推进仿真
         viewer.sync()
   ```



## MJCF

[XML Reference](https://mujoco.readthedocs.io/en/stable/XMLreference.html)

**符号说明**
1. `!` - **required** element, can appear **only once**
2. `?` - **optional** element, can appear **only once**
3. `*` - **optional** element, can appear **many times**
4. `R` - **optional** element, can appear **many times recursively**


`mujoco` (`model` 模型名) (根节点)

仿真计算配置
1. `compiler`
   1. angle : 弧度制/角度制
   2. autolimits : autolimits 是一个 全局开关，用来控制你在定义 joint、tendon或 actuator 时，是否 自动根据 range 推断是否有限制
2. `option`
   1. timestep - 仿真走一步的时间，单位秒，默认 0.002
   2. gravity - "0,0,-9.81"
   3. wind
   4. magnetic - 影响磁力计
   5. density
   6. viscosity(黏稠;黏性)
   7. integrator - 积分器，[Euler, RK4, implicit, implicitfast]
   8. solver - 求解器，[PGS, CG, Newton]
   9. iterations - 约束求解器最大迭代次数


`visual`(可视化配置(渲染相关))
1. `global`
   1. realtime - **仿真世界时间流逝速度/显示世界时间流逝速度**(百分比)，大于1的按1计算
   2. quality - 画面质量
2. `quality` - 渲染质量
3. `headlight` - 头灯
4. `rgba`


`asset`(资源配置(定义 mesh、纹理、材质等可复用资源))
1. `mesh` - works with triangulated meshes, can be loaded from binary STL files, OBJ files or MSH files
2. `hfield` - hfield 通过高度图加载几何体
   1. size : (radius_x, radius_y, elevation_z, base_z)
      1. x轴范围
      2. y轴范围
      3. 最大高度(z轴的正方向)，归一化到 0-1 乘以这个数
      4. 在 Z=0 以下额外“向下延伸”一段厚度，形成一个有实体的“地基”，避免高度场底部“变薄”或“为零厚度”
3. `texture` - 通过加载 png 对物体进行贴图
   1. type - [2d, cube, skybox]
   2. builtin - [none, gradient(渐变), checker(棋盘格), flat]
4. `material` - 后续需要赋给body
   1. texture

default(模板库，可以在使用 `<default>` 模板的同时，覆盖或修改部分参数)

worldbody 是 body 的 最上层，cannot have child elements inertial and joint

body
1. `freejoint` (让一个 body 拥有完整的 6 自由度)
   1. `<freejoint>` 只能用在最顶层的 `<body>` 中(不算 worldbody)，不能放在嵌套结构里的子 `<body>` 中 (否则报错 free joint can only be used on top level)
2. `geom`
   1. `type` : [plane, hfield, sphere, capsule, ellipsoid, cylinder, box, mesh, sdf(signed distance field)]
   2. `size`
      1. plane : X half-size; Y half-size; spacing between square grid lines for rendering
      2. geom sizes are ignored and the height field sizes are used instead
   3. `material`
   4. `mass`/`density` 二选一
   5. `shellineria` 质量集中在表面
   6. [Contact parameters 说明](https://mujoco.readthedocs.io/en/stable/modeling.html#ccontact)
   7. `contype/conaffinity` 碰撞类型 & 和什么类型能碰撞
   8. `condim` 摩擦接触
   9. `friction` (sliding/torsional(扭转)/rolling)
      1. 两个物体摩擦 $\mu = \sqrt{\mu_1 * \mu_2}$
3. `site` 用于标记空间位置，帮助你观察、连接、测量，但它本身不会“碰撞”或“影响质量”
4. `joint`(parent & child 之间的 joint 写在 child 中)
   1. type: [free, ball, slide, hinge], “hinge”
   2. pos : 在 child 的 位置
   3. stiffness 弹性
   4. damping 阻尼
   5. armature 给转子补偿转动惯量 (转子转动惯量 * 减速比^2（很小的值)
   6. ref 角度偏置
   7. **range** (机械限位)
5. `light` (写在 worldbody 下就是 世界灯光)
   1. mode: [fixed(固定(可以实现车灯效果)), track, trackcom, targetbody, targetbodycom], “fixed”
      1. [说明](https://mujoco.readthedocs.io/en/stable/XMLreference.html#body-camera)
   2. castshadow: [false, true], “true” 照射物体是否有影子
   3. pos: real(3), “0 0 0”
   4. dir: real(3), “0 0 -1”
   5. attenuation 衰减系数: real(3), “1 0 0”
   6. exponent 指数聚光灯(汇聚程度): real, “10”
   7. ambient: real(3), “0 0 0”



actuator 驱动器，控制关节(和 worldbody 同级别，不是被包含)
1. general(full access to all actuator components) - 类似编程语言中的父对象，后面很多驱动器继承该驱动器的属性
   1. name (在 viewer 中的 control 对应显示)
   2. `joint` (对应哪个关节)
   3. ctrllimited : [false, true, auto], “auto”
   4. ctrlrange (在 viewer 中的 control 对应显示)
   5. forcerange (限制 actuator 施加在 joint 上的“真实力”，最终作用在 joint 或 tendon 上的结果)
   6. actrange (**不推荐**，最好写在 joint 的 range 中)
   7. gear - 缩放
   8. dyntype : 激活动态类型 [none, integrator, filter, filterexact, muscle, user], “none”
   9. gaintype : 增益类型 [fixed, affine, muscle, user], “fixed”
   10. biastype : 偏置类型 [none, affine, muscle, user], “none”
   11. dynprm : 激活动态参数
   12. gainprm : 增益参数
   13. biasprm : 偏置参
2. motor - direct-drive actuator(力(slide)/力矩(hinge))，使用 和 general 一样的 参数
3. position - position servo with an optional first-order filter (PD控制器，位控，$force = k_p * (x_{aim} - x) + k_v * (- \dot{x})$)
   1. kp
   2. kv
4. velocity - velocity servo (速控)
   1. kv
5. intvelocity - integrated-velocity servo(PI控制器)
   1. kp (速度积分得到距离)
   2. kv
   3. 需要有 actrange 角度的积分限幅






replicate(阵列排布)
1. count : 数量(均匀一圈)
2. sep : namespace separator
3. offset : 偏移量
4. euler : 用来在多个复制体之间添加“旋转偏移” (axis)
   1. 先在 fixed-frame euler 旋转，再在 fixed-frame offset(前一个 replica)



tendon 肌腱



sensor
1. Y键 - 测距可视化



# 相关视频

[【强化学习仿真器之mujoco】第1讲：mujoco代码入门 - B站](https://www.bilibili.com/video/BV1RWKHetEtK)





# 基础教程

[mujoco教程 - Github](https://github.com/Albusgive/mujoco_learning)

mjcf 比 urdf 丰富很多

如果不手动指定 `<inertial>`，MuJoCo 会
1. 自动收集这个 `<body>` 里所有的 `<geom>`
2. 用每个 `<geom>` 的
   1. size(形状)
   2. density(密度，或默认值)
3. 计算出
   1. 每个 geom 的 mass
   2. 每个 geom 的 惯性张量 I



## MJCF








## Installation

编译 : [Github - Mujoco](https://github.com/google-deepmind/mujoco.git)

release版本 : [Github - Releases](https://github.com/google-deepmind/mujoco/releases)

pip : `pip install mujoco`
1. `pip show mujoco`
2. `python3 -m mujoco.viewer` + 模型拖入(xml, mjcf 都可以)
3. `python3 -m mujoco.viewer --mjcf=~/Projects/mujoco/model/humanoid/humanoid.xml`


## HotKey

双击 选中物体 并 高亮
1. ctrl+左键 : 调整物体姿态
2. ctrl+右键 : 在双击选中的位置 施加一个力

ctrl+A相机视角回正

`+` 和 `-` 是 **仿真世界时间流逝速度/显示世界时间流逝速度**(百分比)

空格 暂停/继续 仿真

|Key  |Function|
|-----|---|
|F1         |help|
|F2         |硬件 info|
|F3         |profiler|
|F4         |sensors data|
|F5         |全屏|
|F6         |切换可视化坐标系(world/body/Geom/etc.)|
|F7         |切换实体名字标签|
|TAB        |隐藏左侧工具栏|
|BackSpace  |重置世界|
|`          |geom最小外界矩形和碰撞状态|
|Q          |Camera可视化|
|W          |世界网格化|
|E          |Equality|
|R          |开关光线反射|
|T          |几何体透明化|
|Y          |测距可视化|
|U          |驱动器方向可视化|
|I          |转动惯量可视化|
|O          调整物体位姿可视化|
|P          |Contact可视化|
|[ / ]      |切换相机视角|
| \         |Mesh Tree|
|A          |auto Connect|
|D          |只显示body|
|S          |阴影|
|F          |接触力大小及方向可视化|
|G          |迷雾|
|J          |关节方向可视化|
|H          |凸包可视化|
|K          |关闭天空盒|
|;          |Skin可视化|
|'          |缩放转动惯量(仅可视化，不影响实际值)|
|Z          |灯光|
|X          |Texture关闭|
|C          |接触点可视化|
|V          |肌腱可视化|
|B          |扰动力大小及方向可视化|
|M          |质心可视化|
|,          |Activation|
|/          |haze 地平线|

**窗口左侧**

Simulation
1. **Reset** : 重置状态
   1. 将仿真器的状态(如位置、速度)重置为初始值，不会重新加载模型结构
2. **Reload** : 重新加载模型
   1. 会把 XML 或 MJCF 模型 重新加载一次，构建新的模拟器实例，比 Reset 消耗更多


**窗口右侧**

Joint

Control



