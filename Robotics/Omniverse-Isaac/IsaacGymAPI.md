# IsaacGym API Reference

- [IsaacGym API Reference](#isaacgym-api-reference)
- [Python API](#python-api)
  - [Python Gym API](#python-gym-api)
    - [`add_ground()` \& `add_heightfield()` \& `add_triangle_mesh()`](#add_ground--add_heightfield--add_triangle_mesh)
    - [`create_actor`](#create_actor)
  - [Python Structure](#python-structure)
  - [Python Enums](#python-enums)
    - [`isaacgym.gymapi.DofDriveMode`](#isaacgymgymapidofdrivemode)
  - [Python Constants and Flags](#python-constants-and-flags)



# Python API


## Python Gym API


### `add_ground()` & `add_heightfield()` & `add_triangle_mesh()`

IsaacGym 会自动处理它们与所有物体的碰撞

Actor 才需要设置 碰撞组


### `create_actor`

```python
create_actor(self: Gym, env: Env, asset: Asset, pose: Transform,
             name: str = None, group: int = -1, filter: int = -1,
             segmentationId: int = 0) → int
```

**参数详解**：
1. **`env` (Env)** : 环境句柄，指定 Actor 将被创建在哪个环境中
   - 一个仿真（Simulation）可以包含多个环境，每个环境是独立的仿真实例
   - 通常用于并行仿真多个场景
2. **`asset` (Asset)** : 资产句柄，指定要使用的资产模板
   - 资产通过 `gym.load_asset()` 加载得到
   - 同一个资产可以用于创建多个 Actor 实例
3. **`pose` (Transform)** : 初始变换，定义 Actor 在环境中的初始位置和姿态
   - `Transform` 包含位置（position）和旋转（rotation）
   - 位置 是 3D 坐标 `(x, y, z)`
   - 旋转 可以是四元数或欧拉角
   ```python
   pose = gymapi.Transform()
   pose.p = gymapi.Vec3(0.0, 0.0, 1.0)  # 位置 (x, y, z)
   pose.r = gymapi.Quat(0.0, 0.0, 0.0, 1.0)  # 四元数 (x, y, z, w)
   ```
4. **`name` (str, 可选)** : Actor 的名称，用于标识和调试
   - 默认值为 `None`
   - 可以通过名称查找 Actor
5. **`group` (int, 可选)** : 碰撞组，控制哪些 Actor 之间可以发生碰撞，必须在同一 collisionGroup 才能碰撞
   - 默认值为 `-1`（所有 Actor 都在同一组，可以相互碰撞）
   - **碰撞规则**：只有相同 `group` 值的 Actor 之间才会发生碰撞
   - **应用场景**：
     - 将不同组的 Actor 设置为不碰撞（例如：同一机器人的不同部分、传感器等）
     - 实现选择性碰撞检测，提高性能
6. **`filter` (int, 可选)** : 碰撞过滤器(位掩码)，用于在同一碰撞组内进一步细化碰撞规则
   - 默认值为 `-1`（不进行过滤）
   - 使用**位运算**进行碰撞过滤
   - **工作原理**（**重要：反向逻辑**）：
     - 两个 Actor 的 `filter` 值进行 **按位与**(AND) 运算
       - **结果非零，则它们之间不会发生碰撞**，禁用碰撞
       - **结果为 0，则它们之间可以发生碰撞**，启用碰撞
     - **这是"反向"逻辑**：相同的位 = 禁用碰撞，不同的位 = 启用碰撞
7. **`segmentationId` (int, 可选)** : 分割 ID，用于分割相机传感器
   - 默认值为 `0`
   - 在分割相机(Segmentation Camera)中，不同 `segmentationId` 的 Actor 会被渲染成不同的颜色
   - 用于语义分割、实例分割等视觉任务

**返回值** ： `int`，返回创建的 Actor 的句柄，用于后续操作 (设置 DOF 属性、施加力等)


初始 : 所有关节/刚体通常使用相同的 group 和 filter

后续 : 可以通过 API 单独修改每个刚体的 filter (group 通常不能修改)

`num_rigid_bodies = self.gym.get_asset_rigid_body_count(robot_asset)`

`rigid_body_name = self.gym.get_asset_rigid_body_name(robot_asset, i)`

**重要概念**：
1. **Asset vs Actor**：
   - **Asset**：模型模板，定义了几何形状、关节、质量等属性，但不参与仿真
   - **Actor**：基于 Asset 创建的实例，是仿真中实际存在的实体，参与物理交互
   - 一个 Asset 可以创建多个 Actor（例如：创建多个相同的机器人）
2. **碰撞系统**：
   - `group` 是第一层过滤：不同组不碰撞
   - `filter` 是第二层过滤：同组内通过位掩码进一步控制
   - 两者结合可以实现复杂的碰撞控制策略
3. **Transform**：
   - 位置 `p`：`gymapi.Vec3(x, y, z)`
   - 旋转 `r`：`gymapi.Quat(x, y, z, w)` 或使用 `gymapi.Quat.from_euler_zyx()` 从欧拉角创建



---

## Python Structure




---

## Python Enums

### `isaacgym.gymapi.DofDriveMode`

**功能概述**：自由度（DOF）驱动模式枚举类，用于指定如何控制关节。每个 DOF 只能设置一种驱动模式，设置后会自动忽略其他模式的驱动命令。

```python
# 这些枚举值实际上就是整数常量
gymapi.DOF_MODE_NONE    == 0  # 无控制
gymapi.DOF_MODE_POS     == 1  # 位置控制
gymapi.DOF_MODE_VEL     == 2  # 速度控制
gymapi.DOF_MODE_EFFORT  == 3  # 力矩控制
```

**驱动模式对比**：

| 模式 | 控制输入 | 控制器 | 适用场景 | 精度 |
|------|---------|--------|----------|------|
| `DOF_MODE_NONE` | 无 | 无 | 被动关节、自由摆动 | - |
| `DOF_MODE_POS` | 目标位置 | PD 控制器 | 精确定位、姿态控制 | 高 |
| `DOF_MODE_VEL` | 目标速度 | 直接控制 | 速度跟踪、连续运动 | 中 |
| `DOF_MODE_EFFORT` | 目标力矩/力 | 直接施加 | 力控制、阻抗控制 | 取决于控制算法 |

**相关 API**：
- `gym.get_actor_dof_properties()` : 获取 Actor 的 DOF 属性
- `gym.set_actor_dof_properties()` : 设置 Actor 的 DOF 属性
- `gym.set_dof_position_targets()` : 设置位置目标（用于 `DOF_MODE_POS`）
- `gym.set_dof_velocity_targets()` : 设置速度目标（用于 `DOF_MODE_VEL`）
- `gym.set_dof_actuation_force_tensor()` : 设置力矩/力目标（用于 `DOF_MODE_EFFORT`）


**枚举成员**：

1. **`DOF_MODE_NONE` (值 = 0)** : 无控制模式
   - DOF 可以自由运动，不受任何控制
   - 适用于被动关节、自由摆动的关节
   - 常用于测试或让关节在重力/外力作用下自然运动

2. **`DOF_MODE_POS` (值 = 1)** : 位置控制模式
   - DOF 会响应位置目标命令
   - 使用 **PD 控制器**（比例-微分控制器）跟踪目标位置
   - 需要设置 `stiffness`（刚度，P 增益）和 `damping`（阻尼，D 增益）
   - **应用场景**：精确位置控制，如机械臂末端定位、机器人姿态控制

3. **`DOF_MODE_VEL` (值 = 2)** : 速度控制模式
   - DOF 会响应速度目标命令
   - 直接控制关节的角速度或线速度
   - **应用场景**：速度跟踪、连续运动控制

4. **`DOF_MODE_EFFORT` (值 = 3)** : 力矩/力控制模式
   - DOF 会响应力矩（旋转关节）或力（平移关节）命令
   - 直接施加力或力矩，不经过控制器
   - **应用场景**：力控制、阻抗控制、需要精确力输出的场景

**重要说明**：
- **互斥性**：一个 DOF 只能设置一种驱动模式，设置后会自动忽略其他模式的命令
- **默认模式**：可以通过 `AssetOptions.default_dof_drive_mode` 设置资产的默认驱动模式
- **运行时修改**：可以通过 `set_dof_properties` 在运行时修改每个 Actor 的 DOF 驱动模式

**使用示例**：

```python
from isaacgym import gymapi

# 1. 在 AssetOptions 中设置默认驱动模式
asset_options = gymapi.AssetOptions()
asset_options.default_dof_drive_mode = gymapi.DOF_MODE_POS  # 位置控制
robot_asset = gym.load_asset(sim, asset_root, asset_file, asset_options)

# 2. 创建 Actor 后，获取并修改 DOF 属性
robot_actor = gym.create_actor(env, robot_asset, robot_pose, name="robot")

# 获取 DOF 属性（结构化数组）
dof_props = gym.get_actor_dof_properties(env, robot_actor)

# 修改所有 DOF 为位置控制模式
dof_props['driveMode'][:] = gymapi.DOF_MODE_POS
dof_props['stiffness'][:] = 100.0  # 设置刚度（P 增益）
dof_props['damping'][:] = 10.0     # 设置阻尼（D 增益）

# 应用修改后的属性
gym.set_actor_dof_properties(env, robot_actor, dof_props)

# 2.5. 验证枚举值（可选）
print(f"DOF_MODE_NONE = {gymapi.DOF_MODE_NONE}")      # 输出: 0
print(f"DOF_MODE_POS = {gymapi.DOF_MODE_POS}")        # 输出: 1
print(f"DOF_MODE_VEL = {gymapi.DOF_MODE_VEL}")        # 输出: 2
print(f"DOF_MODE_EFFORT = {gymapi.DOF_MODE_EFFORT}")  # 输出: 3

# 3. 为不同的 DOF 设置不同的驱动模式
num_dofs = gym.get_actor_dof_count(env, robot_actor)
dof_props = gym.get_actor_dof_properties(env, robot_actor)

for i in range(num_dofs):
    dof_name = gym.get_actor_dof_name(env, robot_actor, i)

    if "hip" in dof_name or "shoulder" in dof_name:
        # 大关节使用位置控制
        dof_props['driveMode'][i] = gymapi.DOF_MODE_POS
        dof_props['stiffness'][i] = 200.0
        dof_props['damping'][i] = 20.0
    elif "knee" in dof_name or "elbow" in dof_name:
        # 小关节使用速度控制
        dof_props['driveMode'][i] = gymapi.DOF_MODE_VEL
    else:
        # 其他关节无控制（自由摆动）
        dof_props['driveMode'][i] = gymapi.DOF_MODE_NONE

gym.set_actor_dof_properties(env, robot_actor, dof_props)

# 4. 发送控制命令（根据驱动模式）
# 位置控制：发送目标位置
gym.set_dof_position_targets(env, robot_actor, target_positions)

# 速度控制：发送目标速度
gym.set_dof_velocity_targets(env, robot_actor, target_velocities)

# 力矩控制：发送目标力矩
gym.set_dof_actuation_force_tensor(env, robot_actor, target_efforts)
```



---

## Python Constants and Flags

