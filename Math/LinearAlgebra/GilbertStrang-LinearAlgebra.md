![](Pics/linear000.gif)

![](Pics/linear001.png)

## Table of Contents

- [MIT 18.06 Linear Algebra - Gilbert Strang](#mit-1806-linear-algebra---gilbert-strang)
- [01: Introduction to Linear Algebra](#01-introduction-to-linear-algebra)
- [02: Elimination with Matrices](#02-elimination-with-matrices)
  - [03:](#03)
- [Latex Template](#latex-template)



---

# MIT 18.06 Linear Algebra - Gilbert Strang




[Linear Algebra - MIT OpenCourseWare](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)

[18.06 Linear Algebra](https://web.mit.edu/18.06)

[Github](https://github.com/mitmath/1806)



# 01: Introduction to Linear Algebra

**Row Picture**
1. 每一**行**是一个**方程**
2. 解方程组 = 几何上找向量交点


**Col Picture**
1. 系数矩阵(Coefficient Matrix) 每一**列**当做**向量**
2. 解方程组 = 用未知数 线性组合(linear combination) 系数矩阵的列 得到 目标向量
3. 如果有列向量是多余的(没有贡献)，则会导致 All Linear Combination 无法充满整个空间

矩阵&向量相乘
1. **矩阵 × 列向量 = 列向量**
   1. 矩阵各 **列** 按照向量 线性组合
2. **行向量 × 矩阵 = 行向量**
   1. 矩阵各 **行** 按照向量 线性组合

# 02: Elimination with Matrices

主元 pivot - 不能为0

elimination 是消除其他行中的上方有主元的元素





## 03:




# Latex Template

**3x3 matrix**
$$
\begin{bmatrix}
1 & 2 & 3\\
4 & 5 & 6\\
7 & 8 & 9
\end{bmatrix}
$$


**1x3 matrix**
$$
\begin{bmatrix}
1 & 2 & 3
\end{bmatrix}
$$

**3x1 matrix**
$$
\begin{bmatrix}
1 \\
2 \\
3
\end{bmatrix}
$$

**3x3 determinant**
$$
\begin{vmatrix}
1 & 2 & 3\\
4 & 5 & 6\\
7 & 8 & 9
\end{vmatrix}
$$



