# DUSt3R: Geometric 3D Vision Made Easy (Dense Unconstrained Stereo 3D Reconstruction)

[Paper Website](https://europe.naverlabs.com/research/publications/dust3r-geometric-3d-vision-made-easy/)

[Github](https://github.com/naver/dust3r)




## Table of Contents



#

[理解DUSt3R三维重建新思路 - 知乎](https://zhuanlan.zhihu.com/p/686078541)

三维重建是计算机视觉中的一个高层任务
1. 关键点提取
2. 本质矩阵计算
3. 三角化
4. 相机位姿估计
5. 稀疏重建
6. 稠密重建

传统的三维重建将任务拆解为了多个子问题，作者认为这样的设定，存在几个问题
1. 子问题的解决并非完美的，而且会给下一个子问题带来误差
2. 子问题的数量也会增加任务的复杂度，并加大工程难度
3. 子问题之间的互相协助是有障碍的，后一个子问题的优化不能反馈给前一个子问题，例如相机位姿估计能够帮助进行稠密重建，但是稠密重建的结果无法反馈给相机位姿估计
4. pipeline中有些关键步骤没有较强的鲁棒性，例如估计相机姿态可能会受到图像数量、相机运动等的影响

DUSt3R(Dense Unconstrained Stereo 3D Reconstruction)，在非标定、不含位姿信息的图像上进行稠密三维重建

DUSt3R从非约束的图像集合中**直接恢复出对应的相机坐标系下面的三维点位置信息**(**直接从2D图像中恢复出了对应的3D点云信息**)，然后在三维点信息基础上进行相机标定、深度估计、相机位姿估计、稠密三维重建等




