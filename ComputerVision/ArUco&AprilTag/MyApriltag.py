import cv2
import apriltag
import numpy as np
import matplotlib.pyplot as plt
import sys,os,math,time


testImg1Path=r"./TestPics/april001.png"
testImg2Path=r"./TestPics/april002.png"

filename=testImg1Path

img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# plt.figure(figsize=(10,10))
# plt.imshow(gray, cmap=plt.cm.gray)
# plt.show()


at_detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11 tag25h9'))
tags = at_detector.detect(gray)

print(len(tags))
# print(tags)
print(tags[0].__repr__())
print(type(tags[0]))  # <class 'apriltag.Detection'>

"""
Detection(
    tag_family=b'tag36h11',  # 标签所属的 tag family，b 前缀表示该字符串是以字节 bytes 形式存储的
    tag_id=3,  # 在 tag_family 中该标签的编号
    hamming=0,  # 检测到的标签与 tag_family 中某一标签的实际编码之间的 Hamming 距离
    goodness=0.0,  # 表示图像中该标签的清晰程度或识别可靠性
    decision_margin=83.49791717529297,  # 正确标签和最相似的错误标签之间的解码置信度差距，数值越大，表示识别的置信度越高
    homography=array([  [ 1.46298201e+00,  2.33748738e+00, -4.19032887e+01],
                        [-2.74977265e-01,  5.13138146e-01, -1.24367093e+01],
                        [ 2.47093499e-03,  2.80314209e-03, -7.19309551e-02]]),  # 标签平面与图像平面之间的 单应性矩阵
    center=array([582.54875941, 172.89787484]),  # 标签中心点在图像中的像素坐标
    corners=array([ [591.97900391, 164.17155457],
                    [591.97235107, 183.00921631],
                    [571.6262207 , 183.00509644],
                    [573.03771973, 162.69270325]])  # 标签四个顶点的像素坐标(顺时针顺序排列)
    )
"""

for tag in tags:
    cv2.circle(img, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2)
    cv2.circle(img, tuple(tag.corners[1].astype(int)), 4, (0, 255, 0), 2)
    cv2.circle(img, tuple(tag.corners[2].astype(int)), 4, (0, 0, 255), 2)
    cv2.circle(img, tuple(tag.corners[3].astype(int)), 4, (255, 255, 0), 2)


plt.figure(figsize=(10,10))
plt.imshow(img)
plt.show()