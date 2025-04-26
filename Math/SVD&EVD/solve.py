import numpy as np

# 原始 A 和 b
A = np.array([
    [1, 1, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 1]
], dtype=np.float64)

b = np.array([63, 73, 30, 76, 32, 43], dtype=np.float64)

# ✅ 解法1：伪逆法
x_pinv = np.linalg.pinv(A) @ b

# ✅ 解法2：增广矩阵 + 齐次解法
A_aug = np.hstack((A, -b.reshape(-1, 1)))
U, S, Vh = np.linalg.svd(A_aug)
x_aug = Vh[-1, :]
x_svd = x_aug[:-1] / x_aug[-1]  # 归一化

# ✅ 对比结果
print("解法1（伪逆）:\n", x_pinv)
print("解法2（增广+SVD）:\n", x_svd)

# ✅ 验证 Ax ≈ b
print("Ax_pinv:\n", A @ x_pinv)
print("Ax_svd:\n", A @ x_svd)
print("原始 b:\n", b)
