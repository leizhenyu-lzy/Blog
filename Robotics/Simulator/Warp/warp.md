# Warp

ray-casting

参考 IsaacLab 的 实现

# 底层 Warp Kernels

`source/isaaclab/isaaclab/utils/warp/kernels.py`

`@wp.kernel`
1. raycast_mesh_kernel           : 单 mesh，所有 ray 展平成 (N,3)
2. raycast_static_meshes_kernel  : 多个 静态 mesh，batch (B,N,3)，用 atomic_min 取最近命中
3. raycast_dynamic_meshes_kernel : 多个 动态 mesh，先把 ray 变换到 mesh 局部坐标再打，支持 mesh_positions + mesh_rotations

# 中间层封装层 (Torch & Warp 桥接)

`source/isaaclab/isaaclab/utils/warp/ops.py`


# 传感器层

`source/isaaclab/isaaclab/sensors/ray_caster/`

RayCaster : Heightmap Raycasting，用 grid_pattern 向下发射 ray，得到地面高度点云

RayCasterCamera

MultiMeshRayCaster

MultiMeshRayCasterCamera



