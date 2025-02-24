import cv2
import mediapipe as mp
import argparse
import os
import glob
import re

# 初始化MediaPipe Pose模块
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description="3D Pose Detection using MediaPipe")
    parser.add_argument('--src', type=str, default='webcam', choices=['webcam', 'video', 'image', 'folder'],
                        help="Input source: 'webcam', 'video', 'image', or 'folder'")
    parser.add_argument('--pth', type=str, default='', help="Path to video/image file (if using 'video' as source)")
    return parser.parse_args()

def split_file_path(file_path):
    dir = os.path.dirname(file_path)
    name, ext = os.path.splitext(os.path.basename(file_path))
    return dir, name, ext

# 处理图像
def process_image(image_path, result_dir=None):
    # 检查图像路径是否存在
    if not os.path.exists(image_path):
        print(f"Failed to load image from {image_path}: File does not exist.")
        return

    image_dir, image_name, image_ext = split_file_path(image_path)

    if not result_dir:
        result_path = os.path.join(image_dir, f"{image_name}_result{image_ext}")
    else:
        result_path = os.path.join(result_dir, f"{image_name}_result{image_ext}")
    print(f"result Path = {result_path}")

    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image from {image_path}")
        return

    # 转换为RGB格式
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 进行3D姿态检测
    results = pose.process(rgb_image)

    # 绘制关键点
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # 显示结果
    cv2.imshow('3D Pose Detection - image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite(result_path, image)

def process_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Failed to load folder from {folder_path}: Folder does not exist.")
        return

    result_folder = folder_path + "_result"
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)

    image_path_list = glob.glob(os.path.join(folder_path, '*'))
    pattern = re.compile(r'.*\.(jpg|jpeg|png)$', re.IGNORECASE)
    image_path_list = [pth for pth in image_path_list if pattern.match(pth)]

    for image_path in image_path_list:
        process_image(image_path, result_folder)


def process_video(video_path):
    # 判断是使用摄像头还是视频文件

    if not os.path.exists(video_path):
        print(f"Failed to open video file: {video_path}: File does not exist.")
        return

    cap = cv2.VideoCapture(video_path)  # 使用指定视频文件
    if not cap.isOpened():
        print(f"Failed to open video file: {video_path}")
        return

    video_dir, video_name, video_ext = split_file_path(video_path)
    result_path = os.path.join(video_dir, f"{video_name}_result{video_ext}")
    print(f"result Path = {result_path}")


    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 编码器
    out = cv2.VideoWriter(result_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 转换为RGB格式
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 进行3D姿态检测
        results = pose.process(rgb_frame)

        # 绘制关键点
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 显示结果
        cv2.imshow(f'3D Pose Detection - video', frame)

        out.write(frame)

        # 按键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def process_webcam():
    # 判断是使用摄像头还是视频文件
    cap = cv2.VideoCapture(0)  # 使用默认摄像头
    if not cap.isOpened():
        print("Failed to open webcam.")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 转换为RGB格式
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 进行3D姿态检测
        results = pose.process(rgb_frame)

        # 绘制关键点
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 显示结果
        cv2.imshow(f'3D Pose Detection - webcam', frame)

        # 按键退出
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    args = parse_args()
    print(f"inputSrc = {args.src}")

    if args.pth:
        args.pth = os.path.expanduser(args.pth)  # resolve path with ~
        print(f"src Path = {args.pth}")

    # 根据输入的源类型进行不同的处理
    if args.src == 'image' and args.pth:
        process_image(args.pth)
    elif args.src == 'video' and args.pth:
        process_video(args.pth)
    elif args.src == 'webcam':
        process_webcam()
    elif args.src == 'folder':
        process_folder(args.pth)

if __name__ == '__main__':
    main()


"""
python3 Pose3D.py --src=webcam
python3 Pose3D.py --src=video --pth=~/Videos/taiji.mp4
python3 Pose3D.py --src=video --pth=~/Videos/dance.mp4
python3 Pose3D.py --src=image --pth=~/Videos/skate.jpg
"""


