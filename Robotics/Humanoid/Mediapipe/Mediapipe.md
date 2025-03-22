# 姿势特征点模型

跟踪 33个 身体位置

输出 **归一化 2D 坐标** & **3D 世界坐标**

<img src="Pics/mp001.png" width=400>

00 - nose
01 - left eye (inner)
02 - left eye
03 - left eye (outer)
04 - right eye (inner)
05 - right eye
06 - right eye (outer)
07 - left ear
08 - right ear
09 - mouth (left)
10 - mouth (right)
11 - **left shoulder**
12 - **right shoulder**
13 - **left elbow**
14 - **right elbow**
15 - **left wrist**
16 - **right wrist**
17 - left pinky
18 - right pinky
19 - left index
20 - right index
21 - left thumb
22 - right thumb
23 - **left hip**
24 - **right hip**
25 - **left knee**
26 - **right knee**
27 - **left ankle**
28 - **right ankle**
29 - left heel
30 - right heel
31 - left foot index
32 - right foot index


在 MediaPipe Pose 中，世界坐标系（World Coordinates） 的 原点（0,0,0） 位于骨盆中心（pelvis center），即左右髋关节的中点

ego-centric (origin at pelvis)
x : 左正右负
y : 上负下正
z : 前负后正

