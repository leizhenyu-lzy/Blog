# https://www.bilibili.com/video/BV16K411W7x9/

import cv2 as cv
import numpy as np

## 读图片
# img = cv.imread(r"./Pics/OpencvIcon.png",flags = cv.IMREAD_GRAYSCALE)
# cv.imshow("img", img)
# cv.waitKey(0)

## 读视频
# cap = cv.VideoCapture(r"./Pics/1.mp4")
# while True:
#     success, img = cap.read()
#     cv.imshow("Video", img)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break

## 读摄像头
# cap = cv.VideoCapture(0)
# while True:
#     success, img = cap.read()
#     cv.imshow("Video", img)
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break


## 原图、灰度图、高斯模糊、canny边缘检测、膨胀、侵蚀
# img = cv.imread(r"./Pics/OpencvIcon.png")
# imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# imgBlur = cv.GaussianBlur(imgGray,(7,7),sigmaX=0)
# imgCanny = cv.Canny(img,100,100)
# kernel = np.ones((5,5), np.uint8)
# imgDilation = cv.dilate(imgCanny, kernel, iterations=2)
# imgErosion = cv.erode(imgDilation, kernel, iterations=2)
# cv.imshow("img", img)
# cv.imshow("imgGray", imgGray)
# cv.imshow("imgBlur", imgBlur)
# cv.imshow("imgCanny", imgCanny)
# cv.imshow("imgDilation", imgDilation)
# cv.imshow("imgErosion", imgErosion)
# cv.waitKey(0)


## resize
# img = cv.imread(r"./Pics/OpencvIcon.png")
# print(img.shape)  # 行*列
# imgResize = cv.resize(img,(200,500))  # 宽*高
# print(imgResize.shape)
# cv.imshow("imgResize", imgResize)
# cv.waitKey(0)

## crop
# img = cv.imread(r"./Pics/OpencvIcon.png")
# print(img.shape)
# imgCrop = img[200:400,100:500,:]  # 行*列
# print(imgCrop.shape)  # 行*列
# cv.imshow("img", img)
# cv.imshow("imgCrop", imgCrop)
# cv.waitKey(0)


## draw 
# img = np.zeros((512,1024,3),np.uint8)
# print(img.shape)  # (512, 1024, 3)
# print(img[0,0].shape)  # (3,)
# print(img[0,0].dtype)  # uint8
# print(type(img[0,0]))  # <class 'numpy.ndarray'>
# img[:] = (255,0,0)
# img[100:200,300:400] = (0,255,0)
# # pt要以坐标形式，x-y不是row-col
# cv.line(img,pt1=(100,0),pt2=(img.shape[1],img.shape[0]),color=(0,0,255),thickness=3)
# cv.rectangle(img,pt1=(300,400),pt2=(200,300),color=(0,0,255), thickness=3)
# cv.rectangle(img,pt1=(800,300),pt2=(1000,500),color=(123,123,123), thickness=cv.FILLED)
# cv.circle(img,center=(512,256),radius=40,color=(255,255,0),thickness=10)
# cv.putText(img,"Fuck Nvidia", org=(100,300),fontFace=cv.FONT_HERSHEY_PLAIN,fontScale=3,color=(100,255,100),thickness=3)
# cv.imshow("img", img)
# cv.waitKey(0)


## warp perspective 透视变形
# img = cv.imread(r"./Pics/OpencvCards.png")
# imgCopy = cv.imread(r"./Pics/OpencvCards.png")
# print(img.shape)
# pts1 = np.float32([[100,180],[205,160],[135,345],[245,320]])
# x,y=100,200
# pts2 = np.float32([[0,0],[x,0],[0,y],[x,y]])
# matrix = cv.getPerspectiveTransform(pts1,pts2)
# for pt in pts1:
#     print(pt)
#     cv.circle(imgCopy,pt.astype(np.uint16),3,(0,0,255),2)
# cv.imshow("imgCopy",imgCopy)
# imgTransform = cv.warpPerspective(img,matrix,(x,y))
# cv.imshow("imgTransform",imgTransform)
# cv.waitKey(0)


## joining
# img = cv.imread(r"./Pics/OpencvCards.png")
# imgJoinHorizontal = np.hstack((img.reshape(),img.reshape()))  # 水平
# imgJoinVertical = np.vstack((img,img))  # 竖直
# cv.imshow("img",img)
# cv.imshow("imgJoinHorizontal",imgJoinHorizontal)
# cv.imshow("imgJoinVertical",imgJoinVertical)
# cv.waitKey(0)

## color detect & track bar  chap7
# def trackBarFunc(value):
#     pass
# cv.namedWindow(("trackBars"))
# cv.resizeWindow("trackBars",640,350)  # 稍微大一点，否则bar会显示不全
# # 注意: 在opencv中,H、S、V值范围分别是[0,180]，[0,255]，[0,255]，而非[0,360]，[0,1]，[0,1]；
# cv.createTrackbar("Hue Min","trackBars",  0,179,trackBarFunc)
# cv.createTrackbar("Hue Max","trackBars",179,179,trackBarFunc)
# cv.createTrackbar("Sat Min","trackBars",  0,255,trackBarFunc)
# cv.createTrackbar("Sat Max","trackBars",249,255,trackBarFunc)
# cv.createTrackbar("Val Min","trackBars",  0,255,trackBarFunc)
# cv.createTrackbar("Val Max","trackBars",240,255,trackBarFunc)

# img = cv.imread(r"./Pics/OpencvIcon.png")
# imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
# while True:
#     h_min = cv.getTrackbarPos("Hue Min","trackBars")    
#     h_max = cv.getTrackbarPos("Hue Max","trackBars")
#     s_min = cv.getTrackbarPos("Sat Min","trackBars")
#     s_max = cv.getTrackbarPos("Sat Max","trackBars")
#     v_min = cv.getTrackbarPos("Val Min","trackBars")
#     v_max = cv.getTrackbarPos("Val Max","trackBars")
#     # print(h_min,h_max,s_min,s_max,v_min,v_max)
#     lowerBound = np.array([h_min, s_min, v_min])
#     upperBound = np.array([h_max, s_max, v_max])
#     imgMask = cv.inRange(imgHSV, lowerBound,upperBound)
#     imgDilate = cv.dilate(imgMask, np.ones((3,3)),iterations=2)
#     imgErosion = cv.erode(imgDilate, np.ones((3,3)),iterations=1)
#     imgResult = cv.bitwise_and(img, img, mask=imgDilate)

#     # cv.imshow("img",img)
#     # cv.imshow("imgHSV",imgHSV)
#     cv.imshow("imgResult", imgResult)
#     if cv.waitKey(5) & 0xFF == ord('q'):
#         print("Final: ",h_min,h_max,s_min,s_max,v_min,v_max)  # Final:  0 179 0 235 13 245
#         break

## contours & shape detection chap8



