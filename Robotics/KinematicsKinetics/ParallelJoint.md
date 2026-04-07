# Parallel Joint - 并联关节


参考文献 On the comprehensive kinematics analysis of a humanoid parallel ankle mechanism


电机角度 $\theta$ : $\{\theta_1, \theta_2\}$
关节角度 $x$ : $\{\text{roll}, \text{pitch}\}$

正运动学 : $x = f_{fk}(\theta)$
逆运动学 : $\theta = f_{ik}(x)$

雅可比 : $\dot{\theta} = J_c(\dot{x})$


**仿真 / 训练阶段** : 通常采用 **等效 串联 运动学链** 进行建模，忽略并联闭链结构，policy 直接在 等效的 关节空间(如 roll/pitch)中 进行学习

**实机 / 部署阶段** : policy 输出目标关节角度(或 PD 控制指令)，计算出等效串联关节所需的力矩 $\tau_x$，随后基于虚功原理，利用 **雅可比矩阵** 的 **逆转置** $J_c^{-T}$，将关节力矩映射为实际电机的驱动力矩 $\tau_\theta$





# Mujoco

MuJoCo 不允许直接定义环

添加约束(Equality Constraints)
1. 在 XML 文件中使用 `<equality>` 标签




