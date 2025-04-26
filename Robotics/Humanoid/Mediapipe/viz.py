import os
import numpy as np

import pybullet
import pybullet_data
import time

import myMediapipe


# ------------------------------------------------------------

CURRENT_FILE_PATH = os.path.abspath(__file__)
PACKAGE_DIR = os.path.dirname(os.path.dirname(CURRENT_FILE_PATH))
ROBOT_MODELS_DIR = os.path.join(PACKAGE_DIR, 'models')
G1_29_DOF_URDF = os.path.join(ROBOT_MODELS_DIR, 'g1_description_rviz', 'g1_29dof_rev_1_0.urdf')
G1_29_DOF_LOCK_WAIST_URDF = os.path.join(ROBOT_MODELS_DIR, 'g1_description_rviz', 'g1_29dof_lock_waist_rev_1_0.urdf')




# ------------------------------------------------------------

JOINT_TYPE_DICT = {
    0 : "REVOLUTE (Hinge)",   # 旋转关节（单轴旋转）
    1 : "PRISMATIC",          # 滑动关节（单轴平移）
    2 : "SPHERICAL",          # 球形关节（可以绕任意轴旋转）
    3 : "PLANAR",             # 平面关节（可以在 2D 平面内移动）
    4 : "FIXED",              # 固定关节（无运动）
    6 : "FLOATING"            # 浮动关节（全 6 自由度，适用于无人机等）
}

# ------------------------------------------------------------

# 关键点 加在 link 上

MEDIAPIPE_KEYPOINTS_ID_LIST = myMediapipe.INTERESTED_POINTS_ID_LIST

MEDIAPIPE_KEYPOINTS_NAME_LIST = myMediapipe.INTERESTED_POINTS_NAME_LIST

G1_KEY_LINKS_ID_LIST = [
    22, 30,
    24, 32,
    28, 36,
    1,  7,
    4, 10,
    5, 11,
]

G1_KEY_LINKS_NAME_LIST = [
    "left_shoulder_roll_link"   , "right_shoulder_roll_link",
    "left_elbow_link"           , "right_elbow_link",
    "left_rubber_hand"          , "right_rubber_hand",
    "left_hip_roll_link"        , "right_hip_roll_link",
    "left_knee_link"            , "right_knee_link",
    "left_ankle_pitch_link"     , "right_ankle_pitch_link",
]

RATIO_MEDIAPIPE_TO_G1 = 0.75


# ------------------------------------------------------------

def overviewJoints(robot):
    print("==========" * 3, "Joints Overview", "==========" * 3)

    dictJointNameToIdx = {}

    notFixedJointsList = []

    lowerLimits = []
    upperLimits = []

    notFixedJointsCnt = 0
    jointsCnt = 0

    numJoints = pybullet.getNumJoints(robot)

    for jointIdx in range(numJoints):
        jointInfo = pybullet.getJointInfo(robot, jointIdx)
        jointName = jointInfo[1].decode("utf-8")
        jointType = JOINT_TYPE_DICT[jointInfo[2]]

        if jointType != "FIXED":
            notFixedJointsCnt += 1
            notFixedJointsList.append(jointIdx)
        jointsCnt += 1

        print(f"Joint {jointIdx:02} | {jointName:30} | {jointType}")

        dictJointNameToIdx[jointName] = jointIdx

    print(f"jointsCnt = {jointsCnt}")  # 38 有 11 个 FIXED
    print(f"notFixedJointCnt = {notFixedJointsCnt}")  # 对于 G1_29_DOF_LOCK_WAIST_URDF : 29 - 2 waist 自由度 = 27

    return dictJointNameToIdx, notFixedJointsList

def overviewLinks(robot):
    print("==========" * 3, "Links Overview", "==========" * 3)

    numJoints = pybullet.getNumJoints(robot)

    basePos, baseOrient = pybullet.getBasePositionAndOrientation(robot)  # base (link -1)
    print(f"Base Link (Root, -1) Position: {basePos}, Orientation: {baseOrient}")

    for jointIdx in range(numJoints):
        jointInfo = pybullet.getJointInfo(robot, jointIdx)
        linkName = jointInfo[12].decode("utf-8")  # joint 的 childlink
        print(f"Joint {jointIdx:02} -> ChildLink : {linkName}")

    # print(pybullet.getJointInfo(robot, 0))  # link 0 (not joint)

def getJointsInfo(robot):
    lowerLimits = []
    upperLimits = []
    jointRanges = []

    numJoints = pybullet.getNumJoints(robot)

    for jointIdx in range(numJoints):
        jointInfo = pybullet.getJointInfo(robot, jointIdx)
        lowerLimit = jointInfo[8]
        upperLimit = jointInfo[9]
        jointRange = upperLimit - lowerLimit

        lowerLimits.append(lowerLimit)
        upperLimits.append(upperLimit)
        jointRanges.append(jointRange)

    return np.array(lowerLimits), np.array(upperLimits), np.array(jointRanges)

def getJointsState(robot):
    jointAngles = []

    numJoints = pybullet.getNumJoints(robot)
    for jointIdx in range(numJoints):
        jointState = pybullet.getJointState(robot, jointIdx)
        jointAngle = jointState[0]
        jointAngles.append(jointAngle)

    return np.array(jointAngles)


# ------------------------------------------------------------

def forwardKinematics(robot, names, angles, dictNameIdx):
    print("==========" * 3, "Forward Kinematics", "==========" * 3)

    for name, angle in zip(names, angles):
        idx = dictNameIdx[name]
        pybullet.resetJointState(robot, idx, angle)  # 重置关节角度

    print("Forward Kinematics Finished")

# ------------------------------------------------------------

def drawBoxMarker(position, size, color):
    halfSize = size/2.0

    vertices = np.array([
        [-halfSize, -halfSize, -halfSize],
        [ halfSize, -halfSize, -halfSize],
        [ halfSize,  halfSize, -halfSize],
        [-halfSize,  halfSize, -halfSize],
        [-halfSize, -halfSize,  halfSize],
        [ halfSize, -halfSize,  halfSize],
        [ halfSize,  halfSize,  halfSize],
        [-halfSize,  halfSize,  halfSize],
    ])

    edges = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7),
    ]  # 立方体 12 条边的索引

    vertices[:, 0] = vertices[:, 0] + position[0]
    vertices[:, 1] = vertices[:, 1] + position[1]
    vertices[:, 2] = vertices[:, 2] + position[2]

    for edge in edges:
        pybullet.addUserDebugLine(vertices[edge[0], :], vertices[edge[1], :], color, lineWidth=2)

def markAimKeypoints(positions, color="red"):
    for linkIdx, linkName in zip(MEDIAPIPE_KEYPOINTS_ID_LIST, MEDIAPIPE_KEYPOINTS_NAME_LIST):
        position = positions[linkIdx, :]
        drawBoxMarker(position, size=0.075, color=[1,0,0])
        pybullet.addUserDebugText(linkName, position, textSize=2, textColorRGB=[1, 1, 1])

def markKeyLinkOrigins(robot):
    for linkIdx, linkName in zip(G1_KEY_LINKS_ID_LIST, G1_KEY_LINKS_NAME_LIST):
        linkState = pybullet.getLinkState(robot, linkIdx)
        linkWorldPosition = linkState[4]  # worldLinkFramePosition

        drawBoxMarker(linkWorldPosition, size=0.075, color=[0,1,0])
        pybullet.addUserDebugText(linkName, linkWorldPosition, textSize=2, textColorRGB=[1, 1, 1])

# ------------------------------------------------------------

def inverseKinematics(robot, linkIdxList, targetPositions, notFixedJointsMask):
    print("==========" * 3, "Inverse Kinematics", "==========" * 3)
    lowerLimits, upperLimits, jointRanges = getJointsInfo(robot)
    refJointAngles = getJointsState(robot)

    jointAngles = pybullet.calculateInverseKinematics2(
        robot,
        linkIdxList,
        targetPositions,
        lowerLimits[notFixedJointsMask],
        upperLimits[notFixedJointsMask],
        jointRanges[notFixedJointsMask],
        refJointAngles[notFixedJointsMask]
    )
    return jointAngles







if __name__ == '__main__':

    URDF_FILE = G1_29_DOF_LOCK_WAIST_URDF
    GRAVITY_CHOICE = "ZERO"  # ZERO, EARTH

    # ------------------------------------------------------------

    pybullet.connect(pybullet.GUI)
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())

    if GRAVITY_CHOICE == "ZERO":
        pybullet.setGravity(0, 0, 0)  # 设置零重力
    else:
        pybullet.setGravity(0, 0, -9.81)  # 设置地球重力

    robotG1 = pybullet.loadURDF(URDF_FILE, [0, 0, +0.07605], useFixedBase=True)  # 机器人不会受重力或其他外力影响 初始位置可以改为[0, 0, 0.75]

    # ------------------------------------------------------------

    dictJointNameToIdx, notFixedJointsList = overviewJoints(robotG1)
    overviewLinks(robotG1)

    # ------------------------------------------------------------

    # aimJointNames = np.load(os.path.join(os.path.dirname(__file__), "Data/names.npy"))
    # # print(aimJointNames)

    # aimJointAngles = np.load(os.path.join(os.path.dirname(__file__), "Data/angles.npy"))
    # # print(aimJointAngles)

    # forwardKinematics(robotG1, aimJointNames, aimJointAngles, dictJointNameToIdx)

    # ------------------------------------------------------------

    imgPath = os.path.join(PACKAGE_DIR, "src", "Pics", "kobe001.png")

    mediapipeResults = myMediapipe.processImage(imgPath, visualize=True)

    aimLinkPositions = myMediapipe.cvtMediapipeResultsToEgoCentric(mediapipeResults) * RATIO_MEDIAPIPE_TO_G1

    markKeyLinkOrigins(robotG1)

    markAimKeypoints(aimLinkPositions)

    # ------------------------------------------------------------

    jointAnglesFromIK = inverseKinematics(robotG1, G1_KEY_LINKS_ID_LIST, aimLinkPositions, notFixedJointsList)


    while True:
        time.sleep(0.1)




