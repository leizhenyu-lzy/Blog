import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import autograd.numpy as np
import cv2
import rospy
from geometry_msgs.msg import Pose, PoseArray
from scipy.spatial.transform import Rotation as R


def normal_to_quaternion(normal):
    normal = np.asarray(normal)
    normal = normal / np.linalg.norm(normal)

    z0 = np.array([0, 0, 1])
    if np.allclose(normal, z0):
        return [0, 0, 0, 1]  # identity rotation

    axis = np.cross(z0, normal)
    angle = np.arccos(np.clip(np.dot(z0, normal), -1.0, 1.0))

    axis = axis / np.linalg.norm(axis)
    quat = R.from_rotvec(angle * axis).as_quat()  # [x, y, z, w]
    return quat


def camera_to_robot_frame(pose):
    pose = np.asarray(pose)

    thetax = np.pi / 2
    thetay = 0
    thetaz = - np.pi / 2

    Rx = np.array([[1, 0,               0],
                   [0, np.cos(thetax), -np.sin(thetax)],
                   [0, np.sin(thetax), np.cos(thetax)]])

    Ry = np.array([[np.cos(thetay),  0, np.sin(thetay)],
                   [0,               1, 0              ],
                   [-np.sin(thetay), 0, np.cos(thetay) ]])

    Rz = np.array([[np.cos(thetaz), -np.sin(thetaz), 0],
                   [np.sin(thetaz), np.cos(thetaz), 0],
                   [0, 0, 1]])

    R = np.array([[0, 0, -1],
                  [1, 0, 0],
                  [0, -1, 0]])

    return R @ pose


def get_hand_pose(wrist, pinky, index, side='left'):
    wrist = np.array([wrist.x, wrist.y, wrist.z])
    pinky = np.array([pinky.x, pinky.y, pinky.z])
    index = np.array([index.x, index.y, index.z])
    center = (wrist + pinky + index)/3

    if side == 'left':
        v1 = pinky - wrist
        v2 = index - wrist
    else:   # side == 'right'
        v1 = index - wrist
        v2 = pinky - wrist
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)
    quat = normal_to_quaternion(normal)

    p = Pose()
    p.position.x = center[0]
    p.position.y = center[1]
    p.position.z = center[2]
    p.orientation.x = quat[0]
    p.orientation.y = quat[1]
    p.orientation.z = quat[2]
    p.orientation.w = quat[3]
    return p


def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

    # Draw the pose landmarks.
    pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    pose_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
    solutions.drawing_utils.draw_landmarks(
        annotated_image,
        pose_landmarks_proto,
        solutions.pose.POSE_CONNECTIONS,
        solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image


class MediapipePoseEstimator:
    def __init__(self):
        rospy.init_node("mediapipe_pose_estimator", anonymous=True)
        self.left_hand_pose_pub = rospy.Publisher("/left_hand", Pose, queue_size=1)
        self.right_hand_pose_pub = rospy.Publisher("/right_hand", Pose, queue_size=1)
        self.landmarks_pub = rospy.Publisher('/landmarks', PoseArray, queue_size=1)

        model_path = "pose_landmarker_full.task"
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=True)

        self.mp_pose = mp.solutions.pose
        self.pose_detector = vision.PoseLandmarker.create_from_options(options)
        self.landmark_names = [lm.name.lower() for lm in self.mp_pose.PoseLandmark]

        self.video_source = rospy.get_param("~video_source", "sleep.mp4")
        self.cap = cv2.VideoCapture(self.video_source)
        self.rate = rospy.Rate(5)

        # self.previous = None

    def run(self):
        while not rospy.is_shutdown() and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                rospy.logwarn("Cannot read video frame.")
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            results = self.pose_detector.detect(mp_img)

            if len(results.pose_landmarks) != 0:
                landmark_msg = PoseArray()
                landmark_msg.header.stamp = rospy.Time.now()
                landmarks = results.pose_world_landmarks[0]     # Use the first pose
                """
                Pose landmarker model:
                    0 - nose
                    1 - left eye (inner)
                    2 - left eye
                    3 - left eye (outer)
                    4 - right eye (inner)
                    5 - right eye
                    6 - right eye (outer)
                    7 - left ear
                    8 - right ear
                    9 - mouth (left)
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

                for idx, lmk in enumerate(landmarks):
                    lmk_robot = camera_to_robot_frame(np.array([lmk.x, lmk.y, lmk.z]))
                    landmarks[idx].x = lmk_robot[0]
                    landmarks[idx].y = lmk_robot[1]
                    landmarks[idx].z = lmk_robot[2]

                for lmk in landmarks:
                    p = Pose()
                    p.position.x = lmk.x
                    p.position.y = lmk.y
                    p.position.z = lmk.z
                    p.orientation.w = 1.0
                    landmark_msg.poses.append(p)

                self.landmarks_pub.publish(landmark_msg)

                # print(landmarks[15].x, landmarks[15].y, landmarks[15].z, '\n')

                left_hand_pose = get_hand_pose(landmarks[15], landmarks[17], landmarks[19], 'left')
                right_hand_pose = get_hand_pose(landmarks[16], landmarks[18], landmarks[20], 'right')

                print("left hand pose: \n", left_hand_pose.position)
                print("right hand pose: \n",right_hand_pose.position)

                self.left_hand_pose_pub.publish(left_hand_pose)
                self.right_hand_pose_pub.publish(right_hand_pose)

                # if self.previous is None:
                #     self.previous = left_hand_pose
                    # self.previous = camera_to_robot_frame([left_hand_pose.position.x, left_hand_pose.position.y, left_hand_pose.position.z])

                # print(left_hand_pose.position.x - self.previous.position.x,
                #       left_hand_pose.position.y - self.previous.position.y,
                #       left_hand_pose.position.z - self.previous.position.z,
                #       '\n')


                # Visualize pose detection
                annotated_image = draw_landmarks_on_image(mp_img.numpy_view(), results)
                cv2.imshow('pose', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            else:
                cv2.imshow('pose', cv2.cvtColor(mp_img.numpy_view(), cv2.COLOR_RGB2BGR))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            self.rate.sleep()

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        node = MediapipePoseEstimator()
        node.run()
    except rospy.ROSInterruptException:
        pass