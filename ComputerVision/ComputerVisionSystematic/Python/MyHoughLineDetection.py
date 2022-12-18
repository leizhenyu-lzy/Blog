import cv2 as cv
import numpy as np
import os
import MyTrackBarToolFunctions as tbtf

def myHoughLineDetection(imagePath):
    r"""
    FunctionName    :   
    FunctionDescribe:   
    InputParameter  :   ①
    OutputParameter :   ①
    Specification   :   
    """
    pass





if __name__ == "__main__":
    # 查看目录&获取文件
    print("Current File Path:\t", os.getcwd())

    print("Check Pics")
    picPathPrefix = r"./PicsForCode/StraightLines";
    for roots, dirs, fileNames in os.walk(picPathPrefix):
        print(roots,dirs,fileNames)
    
    for idx,fileName in enumerate(fileNames):
        fileNames[idx] = os.path.join(picPathPrefix,fileName)
    print("Pics for Tests:\n\t",fileNames,"\n")

    # 霍夫变换
    imgCanny, CannyLow, CannyHigh = tbtf.myCannyWithTrackBar(fileNames[2])




    pass
