# IsaacGym

[Isaac Gym - Download Archive](https://developer.nvidia.com/isaac-gym/download)

直接看 里面的 `docs/index.html` 即可，不需要 下载 [Github repository](https://github.com/NVIDIA-Omniverse/IsaacGymEnvs)

---

# Table of Contents

- [IsaacGym](#isaacgym)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Examples](#examples)
  - [`franka_cube_ik_osc.py`](#franka_cube_ik_oscpy)
  - [`kuka_bin.py`](#kuka_binpy)
  - [Simulation Setup](#simulation-setup)
  - [Assets](#assets)
  - [Tensor API](#tensor-api)
    - [Physics State](#physics-state)
    - [Contact Tensors](#contact-tensors)
    - [Force Tensors](#force-tensors)
    - [Control Tensors](#control-tensors)
  - [API Reference](#api-reference)
    - [Python API](#python-api)
  - [Installation](#installation-1)

---

# Installation

推荐 conda，进入 python 文件夹 `pip install -e .` 又可能 python 版本 不匹配

```bash
./create_conda_env_rlgpu.sh
conda activate rlgpu
```

# Examples

## `franka_cube_ik_osc.py`

2种 控制器
1. **IK**  : Inverse Kinematics - 逆运动学
2. **OSC** : Operational Space Control - 操作空间控制
   1. [Operational Space Control of Constrained and Underactuated Systems - 论文](https://roboticsproceedings.org/rss07/p31.pdf)


asset
1. franka: `gym.load_asset`
2. table : `gym.create_box`
3. box   : `gym.create_box`

配置 franka DoF 的 driveMode stiffness damping

franka 的 body & gripper 设置 不同 default_dof_pos，并转为 tensor

配置 多环境布局 grid layout，单个环境的 局部坐标边界

添加 ground plane

for 循环
1. 创建 env
2. `create_actor` : table + box + franka
3. 获取 各个 rigid_body_index & rigid_body_handle，配合 后续 rigid_body_state





## `kuka_bin.py`




---




gymapi : Isaac Gym 的核心接口模块，提供了与底层物理引擎（PhysX）交互的基本功能。它定义了仿真环境、资产（Assets）、角色（Actors）等的创建和管理方法，是构建和控制仿真世界的基础。

gymutil : 辅助模块，提供了一些实用工具函数，用于简化仿真设置、参数解析和调试

gymtorch : gymtorch 是 Isaac Gym 与 PyTorch 的集成模块，用于将仿真中的原始数据（例如张量）转换为 PyTorch 张量，从而便于在深度学习框架中使用



## Simulation Setup

`from isaacgym import gymapi`  core API defined in `gymapi` module

`gym = gymapi.acquire_gym()`


## Assets






## Tensor API

tensor API is currently only supported for the **PhysX backend**




**global tensors** : tensors that hold the values for all actors in the simulation

Gym Tensor API 直接与 GPU 交互，但返回的数据不是标准的 PyTorch Tensor，而是低级别的 GPU 缓冲区，必须使用 `gymtorch.wrap_tensor()` 转换，才能在 PyTorch 中操作

Gym tensor API uses simple tensor desciptor, which specify the **device, memory address, data type, and shape of a tensor**




### Physics State

Actor Root State Tensor - TODO

`actor_root_state = self.gym.acquire_actor_root_state_tensor(self.sim)`

`self.root_states = gymtorch.wrap_tensor(actor_root_state)`



Degrees-of-Freedom


### Contact Tensors

```python
_net_cf = gym.acquire_net_contact_force_tensor(sim)
net_cf = gymtorch.wrap_tensor(_net_cf)
```

### Force Tensors


### Control Tensors

**DOF Control**

set_dof_actuation_force_tensor

**Body Forces**






## API Reference

### Python API

[Python Gym API - Isaac Gym](file:///home/lzy/Projects/isaacgym/docs/api/python/gym_py.html)

`gym = gymapi.acquire_gym()`
`robot_asset = gym.load_asset(sim, asset_root, asset_file, asset_options)`

**class** `isaacgym.gymapi.Gym`
1. `acquire_actor_root_state_tensor` : Retrieves buffer for Actor root states - TODO
   1. shape : (num_actors, 13)
      1. position([0:3]) - 3
      2. rotation([3:7]) - 4
      3. linear velocity([7:10]) - 3
      4. angular velocity([10:13]) - 3
   2. 通常对应于机器人模型的 基座(base link/pelvis)
2. `get_asset_dof_count` : Gets the count of Degrees of Freedom on a given asset
   1. number of degrees of freedom in asset
3. `get_asset_dof_dict`
4. `get_asset_dof_name` : 需要 index of joint
5. `get_asset_dof_names`
6. `get_asset_dof_properties(self: Gym, arg0: Asset)→ numpy.ndarray[carb::gym::GymDofProperties]` : Gets an array of DOFs' properties for the given asset
   1. [DOF Properties and Drive Modes](file:///home/lzy/Projects/isaacgym/docs/programming/physics.html?highlight=physics#dof-properties-and-drive-modes)
   2. 注意 得到的 是 **结构化数组**
        ```python
        dof_props_asset = gym.get_asset_dof_properties(robot_asset)
        print(type(dof_props_asset)) # <class 'numpy.ndarray'>
        print(dof_props_asset.dtype)
        # {
        #    'names':
        #        ['hasLimits', 'lower', 'upper', 'driveMode',
        #        'velocity', 'effort', 'stiffness', 'damping', 'friction', 'armature'],
        #    'formats':
        #        ['?', '<f4', '<f4', '<i4', '<f4', '<f4', '<f4', '<f4', '<f4', '<f4'],
        #    'offsets':
        #        [0, 4, 8, 12, 16, 20, 24, 28, 32, 36],
        #    'itemsize': 40
        # }
        print(dof_props_asset["lower"][0].item())
        print(dof_props_asset["effort"][0].item())
        ```
   3. <img src="Pics/gym005.png" width=600>
   4. stiffness (对应 PD-Control 的 P-gain $K_p$ 比例增益)
   5. damping   (对应 PD-Control 的 D-gain $K_d$ 微分增益)
7. `get_asset_dof_type(self: Gym, arg0: Asset, arg1: int)→ DofType` : Degree of Freedom type
   ```python
    dof_type = gym.get_asset_dof_type(robot_asset, i)
    if dof_type == gymapi.DOF_ROTATION:
        dof_type_str = "Rotation"
    elif dof_type == gymapi.DOF_TRANSLATION:
        dof_type_str = "Translation"
   ```





**class** `isaacgym.gymapi.AssetOptions`
1. Docs Path : Programming -> API Reference -> Python API -> Python Structures
2. **物理属性 (Physics Properties)**：
   - `density` : 默认密度参数，单位 $kg/m^3$。当资产文件中没有提供质量和惯性数据时，用于计算物体的质量和惯性张量
   - `angular_damping` : 刚体的角速度阻尼系数，用于模拟旋转时的能量损失
   - `linear_damping` : 刚体的线速度阻尼系数，用于模拟平移时的能量损失
   - `max_angular_velocity` : 刚体的最大角速度限制，单位 $rad/s$
   - `max_linear_velocity` : 刚体的最大线速度限制，单位 $m/s$
   - `armature` : 添加到所有刚体/连杆的惯性张量对角线元素上的值，可提高仿真稳定性(类似于数值正则化)
   - `thickness` : 碰撞形状的厚度。设置物体与该物体表面的静止距离
3. **关节与驱动 (Joints and Actuation)**：
   - `default_dof_drive_mode` : 用于驱动 asset 关节的默认模式，参见 `isaacgym.gymapi.DriveModeFlags`，常见模式包括 : 位置控制 (POSITION)、速度控制 (VELOCITY)、力矩控制 (EFFORT)
   - `tendon_limit_stiffness` : 默认腱限制刚度。由于限制不是隐式求解的，应选择较小的值。通过设置适当的阻尼值来避免振荡
4. **几何与拓扑 (Geometry and Topology)**：
   - ==`collapse_fixed_joints`== : 合并由固定关节连接的连杆，可以简化模型并提高性能
   - ==`fix_base_link`== : 在导入时将资产的基座固定在指定位置（用于固定基座的机器人）
   - `flip_visual_attachments` : 将网格从 Z-up 左手坐标系转换为 Y-up 右手坐标系
   - `override_com` : 是否从几何形状计算质心并覆盖原始资产中给定的值
   - `override_inertia` : 是否从几何形状计算惯性张量并覆盖原始资产中给定的值
5. **碰撞几何 (Collision Geometry)**：
   - ==`replace_cylinder_with_capsule`== : 用胶囊体替换圆柱体以获得更好的性能(胶囊体碰撞检测更高效)
   - `slices_per_cylinder` : 生成的圆柱体网格的面数（不包括顶部和底部）
   - `vhacd_enabled` : 是否启用凸分解(仅适用于 PhysX)，默认值为 False
   - `vhacd_params` : 凸分解参数(仅适用于 PhysX)，如果未指定，所有三角网格将使用单个凸包进行近似
   - `convex_decomposition_from_submeshes` : 是否将网格中的子网格视为网格的凸分解。默认值为 False
6. **材质与视觉 (Materials and Visuals)**：
   - `mesh_normal_mode` : 如何加载资产中网格的法线。可选值：
     - `FROM_ASSET` : 从资产文件加载（默认）
     - `COMPUTE_PER_VERTEX` : 按顶点计算（如果资产中未完全指定法线，则回退到此模式）
     - `COMPUTE_PER_FACE` : 按面计算
   - `use_mesh_materials` : 是否使用从网格文件加载的材质，而不是资产文件中定义的材质。默认值为 False
7. **物理引擎特定 (Physics Engine Specific)**：
   - `disable_gravity` : 禁用该资产的重力
   - `enable_gyroscopic_forces` : 启用陀螺力（仅限 PhysX）
   - `use_physx_armature` : 使用关节空间 armature，而不是连杆惯性张量修改
8. **软体与粒子 (Soft Bodies and Particles)**：
   - `min_particle_mass` : 软体中粒子的最小质量，单位 Kg

**使用示例**：
```python
asset_options = gymapi.AssetOptions()
asset_options.fix_base_link = True           # 固定基座
asset_options.collapse_fixed_joints = True   # 合并固定关节
asset_options.disable_gravity = False        # 启用重力
asset_options.default_dof_drive_mode = gymapi.DOF_MODE_POS  # 位置控制模式
asset_options.armature = 0.01                # 增加数值稳定性
robot_asset = gym.load_asset(sim, asset_root, asset_file, asset_options)
```































torch_utils
1. `quat_rotate` & `quat_rotate_inverse` - TODO
   1. input
      1. q : 四元数 $(q_x, q_y, q_z, q_w)$
      2. v : 待旋转的向量 $x, y, z$

```python
@torch.jit.script
def quat_rotate(q, v):
    shape = q.shape
    q_w = q[:, -1]
    q_vec = q[:, :3]
    a = v * (2.0 * q_w ** 2 - 1.0).unsqueeze(-1)
    b = torch.cross(q_vec, v, dim=-1) * q_w.unsqueeze(-1) * 2.0
    c = q_vec * \
        torch.bmm(q_vec.view(shape[0], 1, 3), v.view(
            shape[0], 3, 1)).squeeze(-1) * 2.0
    return a + b + c


@torch.jit.script
def quat_rotate_inverse(q, v):
    shape = q.shape
    q_w = q[:, -1]
    q_vec = q[:, :3]
    a = v * (2.0 * q_w ** 2 - 1.0).unsqueeze(-1)
    b = torch.cross(q_vec, v, dim=-1) * q_w.unsqueeze(-1) * 2.0
    c = q_vec * \
        torch.bmm(q_vec.view(shape[0], 1, 3), v.view(
            shape[0], 3, 1)).squeeze(-1) * 2.0
    return a - b + c
```


## Installation


[Isaac Gym - Now Deprecated](https://developer.nvidia.com/isaac-gym)

[Isaac Gym - Download Archive](https://developer.nvidia.com/isaac-gym/download)

Installation instructions can be found in the package in the docs folder - open `docs/index.html` to see more.

[Isaac Gym安装及使用教程 - 知乎](https://zhuanlan.zhihu.com/p/618778210)


```python
# unitree-rl 不要完全一样操作
# 可能需要
# find ~/miniconda3/envs/unitree-rl/ -name "libpython3.8.so.1.0"
# sudo ln -s /home/lzy/miniconda3/envs/unitree-rl/lib/libpython3.8.so.1.0 /usr/lib/libpython3.8.so.1.0 创建软链接




# 绿色的按钮下载压缩文件IsaacGym_Preview_4_Package.tar.gz
# 对上面的文件解压缩，得到isaacgym的文件夹，最外层可以扔掉

# 指令会新建名为rlgpu的conda环境

cd isaacgym/python/
sh ../create_conda_env_rlgpu.sh

# 先试一下安装好的环境能不能用
conda activate rlgpu
cd examples
python joint_monkey.py

# 如果报错没有isaacgym
cd isaacgym/python/
pip install -e .

# 此时再尝试运行demo
cd examples
python joint_monkey.py

# 如果报错ImportError: libpython3.7m.so.1.0
# 找出系统中的libpython3.7m.so.1.0的位置
find / -name "libpython*so*"
sudo cp /path/to/libpython3.7m.so.1.0 /usr/lib/x86_64-linux-gnu

# 再次尝试运行demo
cd examples
python joint_monkey.py

# 从 Github 下载 IsaacGymEnvs https://github.com/isaac-sim/IsaacGymEnvs/tree/main 内容全部复制到 isaacgym 中
cd isaacgym/
pip install -e .


cd isaacgymenvs
python train.py task=Cartpole
# 【ImportError】from torch._C import * # noqa: F403； ImportError: xxx: defined symbol: iJIT_NotifyEvent
pip install mkl==2024.0.0

# RuntimeError: The following operation failed in the TorchScript interpreter.
# Traceback of TorchScript (most recent call last):
# RuntimeError: nvrtc: error: invalid value for --gpu-architecture (-arch)
pip3 install torch torchvision torchaudio  # solve this by upgrading to a higher torch version
```


