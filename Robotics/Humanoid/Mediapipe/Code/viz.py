import os
import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
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
11 - left shoulder
12 - right shoulder
13 - left elbow
14 - right elbow
15 - left wrist
16 - right wrist
    17 - left pinky
    18 - right pinky
    19 - left index
    20 - right index
    21 - left thumb
    22 - right thumb
23 - left hip
24 - right hip
25 - left knee
26 - right knee
27 - left ankle
28 - right ankle
    29 - left heel
    30 - right heel
    31 - left foot index
    32 - right foot index
"""


# initial mediapipe pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False)


dictKeyPoint = {
    11 : "left shoulder",
    12 : "right shoulder",
    13 : "left elbow",
    14 : "right elbow",
    15 : "left wrist",
    16 : "right wrist",


    23 : "left hip",
    24 : "right hip",
    25 : "left knee",
    26 : "right knee",
    27 : "left ankle",
    28 : "right ankle",
}


POSE_CONNECTIONS = [
    (11, 13), (13, 15),        # Left Arm
    (12, 14), (14, 16),        # Right Arm
    (23, 25), (25, 27),        # Left Leg
    (24, 26), (26, 28),        # Right Leg
    (11, 12),                  # Shoulders
    (23, 24),                  # Hips
    (11, 23), (12, 24)         # Spine
]





def getPose3D(frame_rgb):
    results = pose.process(frame_rgb)
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        points3d = np.array([[lm.x, lm.y, lm.z] for lm in landmarks])  # (33, 3)
        return points3d
    else:
        return None


def init3Dplot():
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-0.5,0.5)
    ax.set_ylim(-0.5,0.5)
    ax.set_zlim(-0.5,0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Pose')
    return fig, ax


def update3Dplot(ax, points3d, connections=None):
    ax.cla()  # 清空
    xs, ys, zs = points3d[:,0], points3d[:,1], points3d[:,2]
    ax.scatter(xs, ys, zs, c='r', s=20)

    if connections:
        for (start, end) in connections:
            xline = [points3d[start,0], points3d[end,0]]
            yline = [points3d[start,1], points3d[end,1]]
            zline = [points3d[start,2], points3d[end,2]]
            ax.plot(xline, yline, zline, c='b')

    # draw axis
    shrink_rate = 0.1
    ax.quiver(0, 0, 0, 1*shrink_rate, 0, 0, color='r', length=1, normalize=True)  # red
    ax.quiver(0, 0, 0, 0, 1*shrink_rate, 0, color='g', length=1, normalize=True)  # green
    ax.quiver(0, 0, 0, 0, 0, 1*shrink_rate, color='b', length=1, normalize=True)  # blue


    ax.set_xlim(-0.5,0.5)
    ax.set_ylim(-0.5,0.5)
    ax.set_zlim(-0.5,0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Pose')



def center2Pelvis(points3d):
    """
    pelvis (middle point of left & right hip)
    """
    pelvis_center = (points3d[23] + points3d[24]) / 2
    points3d_centered = points3d - pelvis_center
    return points3d_centered


def rotate2EgoCentric(points3d):
    """
    ego-centric
    1. x : front
    2. y : left
    3. z : up

    know position in the world frame, need to cvt back to ego-centric frame

    need the world axis represent in the ego-centric frame


    world:
    z  y
    | /
    |/
    o----x

    ego-centric:
       o----y
      /|
     / |
    z  x
    """
    R = np.array([
        [0, 0, -1],
        [1, 0, 0],
        [0, -1, 0]
    ])
    points3d_rotated = points3d @ R.T  # (R @ point3d.T ).T
    return points3d_rotated




if __name__ == "__main__":
    # videoPath = os.path.join(os.path.dirname(__file__), r"../Pics/cxk_body.webm")
    videoPath = os.path.join(os.path.dirname(__file__), r"../Pics/ball.mp4")

    cap = cv2.VideoCapture(videoPath)
    if not cap.isOpened():
        print(f"Cannot open video: {videoPath}")
        exit()

    # 初始化3D绘图
    plt.ion()  # 打开交互模式
    fig, ax = init3Dplot()
    fig.show()
    fig.canvas.draw()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        points3d = getPose3D(frame_rgb)

        if points3d is not None:
            h, w, _ = frame.shape
            # update 2d image
            for (x, y, z) in points3d:
                cx, cy = int(x * w), int(y * h)
                cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

            # udpate 3d image
            points3d = center2Pelvis(points3d)
            points3d = rotate2EgoCentric(points3d)
            update3Dplot(ax, points3d, POSE_CONNECTIONS)
            fig.canvas.draw()
            fig.canvas.flush_events()

        cv2.imshow("2D Pose", frame)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.close('all')







