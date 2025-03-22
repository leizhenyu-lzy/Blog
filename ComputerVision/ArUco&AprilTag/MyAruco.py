import cv2
import numpy as np
# 生成aruco标记
# 加载预定义的字典
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# 生成标记
markerImage = np.zeros((200, 200), dtype=np.uint8)
markerImage = cv2.aruco.generateImageMarker(dictionary, 22, 200, markerImage, 1)
# cv2.imwrite("marker22.png", markerImage)


# 显示标记
cv2.imshow("Aruco Marker", markerImage)
cv2.waitKey(0)
cv2.destroyAllWindows()