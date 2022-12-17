import cv2 as cv
import torch


def cannyWithTrackBar(outerPath, onChangeCannyThreshLow=None, onChangeCannyThreshHigh=None):
    r"""
    FunctionName    : myCannyWithTrackBar
    FunctionDescribe: 使用OpenCV的Canny结合Trackbar，用于选出Canny的两个阈值，按下'q'键退出
    InputParameter  : ①outerPath(str 图片路径)  
                      ②onChangeCannyThreshLow(默认None)  
                      ③onChangeCannyThreshHigh(默认None)
    OutputParameter : ①imgCanny(<class 'numpy.ndarray'>)  
                      ②cannyThresholdLow  
                      ③cannyThresholdHigh
    """
    path = outerPath
    imgGray = cv.imread(path, cv.IMREAD_GRAYSCALE)
    # 对应两个trackbar的onChange函数
    def recallCannyThresholdLow(threshold):
        # print("recallCannyThresholdLow: ", threshold)
        pass
    def recallCannyThresholdHigh(threshold):
        # print("recallCannyThresholdLow: ", threshold)
        pass

    cv.namedWindow("CannyThresholds")
    cv.resizeWindow("CannyThresholds", 500, 150)
    if (onChangeCannyThreshHigh is None) or (onChangeCannyThreshLow is None):
        cv.createTrackbar("CannyThreshLow","CannyThresholds",0,255,recallCannyThresholdLow)
        cv.createTrackbar("CannyThreshHigh","CannyThresholds",0,255,recallCannyThresholdHigh)
    else:
        cv.createTrackbar("CannyThreshLow","CannyThresholds",0,255,onChangeCannyThreshLow)
        cv.createTrackbar("CannyThreshHigh","CannyThresholds",0,255,onChangeCannyThreshHigh)

    while True:
        thresholdLow = cv.getTrackbarPos("CannyThreshLow", "CannyThresholds")
        thresholdHigh = cv.getTrackbarPos("CannyThreshHigh", "CannyThresholds")
        imgCanny = cv.Canny(imgGray,thresholdLow,thresholdHigh)
        cv.imshow("imgCanny", imgCanny)
        
        if cv.waitKey(1)&0xFF == ord('q'):
            cv.destroyAllWindows()
            print("CannyThresholdLow: ",min(thresholdHigh,thresholdLow),
                    "\nCannyThresholdHigh: ",max(thresholdHigh,thresholdLow))
            print(type(imgCanny))
            return imgCanny, min(thresholdHigh,thresholdLow), max(thresholdHigh,thresholdLow)


if __name__ == "__main__":
    cannyWithTrackBar("./PicsForCode/StraightLines/StraightLines01.jpg")