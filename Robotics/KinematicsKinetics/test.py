import numpy as np

theta = 5
c = np.cos(theta)
s = np.sin(theta)
d = 10

R = np.array([
    [c,-s, 0, 0],
    [s, c, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
])

T = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, d],
    [0, 0, 0, 1],
])

print(R @ T == T @ R)

