import cv2
import numpy as np

def nothing(x):
    pass

img_color = cv2.imread(f'./Pics/OpencvCards.png')
img = cv2.imread(f"./Pics/OpencvCards.png", cv2.IMREAD_GRAYSCALE)

print(np.max(img))

# 初始化 SimpleBlobDetector
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 100
detector = cv2.SimpleBlobDetector_create(params)

# 检测关键点
keypoints = detector.detect(img)

# 创建窗口
cv2.namedWindow("Blobs")

# 创建滑动条
cv2.createTrackbar("Min Area", "Blobs", 100, 500, nothing)
cv2.createTrackbar("Max Area", "Blobs", 500, 500, nothing)
cv2.createTrackbar("Min Circularity", "Blobs", 30, 100, nothing)
cv2.createTrackbar("Min Convexity", "Blobs", 30, 100, nothing)
cv2.createTrackbar("Min Inertia Ratio", "Blobs", 15, 100, nothing)
# cv2.createTrackbar("Blob Color", "Blobs", 0, 255, nothing)

while True:
    # 读取 trackbar 的位置
    min_area = max(cv2.getTrackbarPos("Min Area", "Blobs"), 1)
    max_area = max(cv2.getTrackbarPos("Max Area", "Blobs"), min_area+1)
    min_circularity = max(cv2.getTrackbarPos("Min Circularity", "Blobs") / 100.0, 0.01)
    min_convexity = max(cv2.getTrackbarPos("Min Convexity", "Blobs") / 100.0, 0.01)
    min_inertia_ratio = max(cv2.getTrackbarPos("Min Inertia Ratio", "Blobs") / 100.0, 0.01)
    blob_color = cv2.getTrackbarPos("Blob Color", "Blobs")

    # 设置 SimpleBlobDetector 参数
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = min_area
    params.maxArea = max_area

    params.filterByCircularity = True
    params.minCircularity = min_circularity

    params.filterByConvexity = True
    params.minConvexity = min_convexity

    params.filterByInertia = True
    params.minInertiaRatio = min_inertia_ratio

    # params.filterByColor = True
    # params.blobColor = blob_color

    # 创建一个 SimpleBlobDetector 对象
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(img)

    # 绘制关键点
    img_with_keypoints = cv2.drawKeypoints(
        img_color, keypoints, np.array([]), (255, 255, 255),
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )

    # 显示结果
    cv2.imshow("Blobs", img_with_keypoints)

    # 按下 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


