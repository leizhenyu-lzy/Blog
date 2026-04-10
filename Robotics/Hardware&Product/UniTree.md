# UniTree

## G1

Links
1. [UniTree - G1](https://www.unitree.com/cn/g1)
2. [G1 URDF - Github](https://github.com/unitreerobotics/unitree_ros/tree/master/robots)
3. [G1 SDK Development Guide](https://support.unitree.com/home/en/G1_developer/about_G1)

<img src="Pics/g1_001.png" width=900>

**G1**
1. 23 DoF
   1. waist : 1
   2. single arm : 5
   3. single hand : 0

**G1-EDU**
1. **23 ~ 43** (`43 = 23 + 2 + (7 + 2) * 2`) DoF
   1. waist : 1(origin) + **2 (additional)**
   2. single arm : 5
   3. single hand : **(7 + 2) * 2 (additional)**
      1. dexterous hand : 7
         1. thumb : 3
         2. index finger  : 2
         3. middle finger : 2
      2. additional wrist : 2

29 DoF & 23 DoF (区别)
1. waist_roll_joint
2. waist_pitch_joint
3. right_wrist_pitch_joint
4. right_wrist_yaw_joint
5. right_hand_palm_joint
6. left_wrist_pitch_joint
7. left_wrist_yaw_joint
8. left_hand_palm_joint



lock 只需将 `revolute` 改为 `fixed`




头部 & 颈部 无 DoF


**Size** : 1320x450x200mm

**Weight** : ≈ 35 kg


**Joint serial number and joint limit** (0~28 共 29 个)
1. <img src="Pics/g1_003.png" width=800>
2. <img src="Pics/g1_002.png" width=800>

Vocabulary
1. torso : 躯干
2. pelvis : 盆骨 (tf-tree root)
3. elbow : 肘
4. ankle : 脚踝
5. hip : 髋
6. wrist : 手腕
7. waist : 腰





**TF-Tree (29 DoF)**
```
pelvis
├── pelvis_contour_link
├── right_hip_pitch_link
│   └── right_hip_roll_link
│       └── right_hip_yaw_link
│           └── right_knee_link
│               └── right_ankle_pitch_link
│                   └── right_ankle_roll_link
├── waist_yaw_link
│   └── waist_roll_link
│       └── torso_link
│           ├── d435_link
│           ├── head_link
│           ├── imu_in_torso
│           ├── left_shoulder_pitch_link
│           │   └── left_shoulder_roll_link
│           │       └── left_shoulder_yaw_link
│           │           └── left_elbow_link
│           │               └── left_wrist_roll_link
│           │                   └── left_wrist_pitch_link
│           │                       └── left_wrist_yaw_link
│           │                           └── left_rubber_hand
│           ├── logo_link
│           ├── mid360_link
│           ├── right_shoulder_pitch_link
│           │   └── right_shoulder_roll_link
│           │       └── right_shoulder_yaw_link
│           │           └── right_elbow_link
│           │               └── right_wrist_roll_link
│           │                   └── right_wrist_pitch_link
│           │                       └── right_wrist_yaw_link
│           │                           └── right_rubber_hand
│           ├── imu_in_pelvis
├── left_hip_pitch_link
│   └── left_hip_roll_link
│       └── left_hip_yaw_link
│           └── left_knee_link
│               └── left_ankle_pitch_link
│                   └── left_ankle_roll_link
```




39 links (1 root link(pelvis) + 38 joint(child link))

38 joints
1. 29dof_lock_waist = 29 - 2(waist roll & pitch) = 27 DoF (11 fixed + 27 revolute)


