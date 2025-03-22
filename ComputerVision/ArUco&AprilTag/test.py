import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter([1, 2, 3], [4, 5, 6], [7, 8, 9])
plt.show()

# 测试 OpenCV 的 GUI 功能
import cv2
image = cv2.imread("test_image.jpg")
cv2.imshow("Test Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()