import numpy as np
import pandas as pd

# 模拟 replicate 配置参数
count = 4  # replicate count
euler_per_step = 1.57  # 每次复制旋转 90 度（弧度）
offset_local = np.array([-0.05, 0.0, 0.0])  # 每个副本之间在局部坐标下的平移
site_local = np.array([0.05, 0.0, 0.0])  # site 在当前副本局部坐标中的位置

# 初始化第 0 个副本的原点和旋转（世界坐标）
origin = np.array([0.0, 0.0, 0.0])
rotation = np.eye(3)  # 单位矩阵表示无旋转

positions = []  # 存储每个副本的 site 世界坐标

for i in range(count):
    # 第 i 个副本中 site 的世界坐标 = 当前副本原点 + 当前旋转作用下的 site 相对位置
    site_world = origin + rotation @ site_local
    positions.append({
        "replica": f"rfAAA{i}",
        "site_world_x": site_world[0],
        "site_world_y": site_world[1],
        "site_world_z": site_world[2]
    })

    # 下一副本的原点 = 当前原点 + 当前坐标系中 offset 所表示的世界方向偏移
    offset_world = rotation @ offset_local
    origin = origin + offset_world

    # 更新旋转矩阵：继续在当前坐标系下累积绕 Z 轴旋转
    theta = euler_per_step
    Rz = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0,              0,             1]
    ])
    rotation = rotation @ Rz  # 累积旋转

# 显示结果
df = pd.DataFrame(positions)
print(df)
