import cv2 as cv
import numpy as np
import math

def myGaussian1DFunction(sigma,xPos):
    r"""
    FunctionName    :   myGaussian1DFunction
    FunctionDescribe:   
    InputParameter  :   ①sigma(标准差，不是方差)
                        ②xPos(横坐标)
    OutputParameter :   ①
    """
    return (1/(math.sqrt(2*math.pi)*sigma))*math.exp(-xPos**2/(2*sigma**2))

def myGaussian1DKernel(kernelLength,sigma):
    r"""
    FunctionName    :   myGaussian1DKernel
    FunctionDescribe:   求出一维高斯核
    InputParameter  :   ①kernelLength(一维的长度，需要是正奇数，否则return None)
                        ②sigma(标准差，不是方差)
    OutputParameter :   ①kernel(列向量，<class 'numpy.ndarray'>)
    OfficialLink    :   https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gac05a120c1ae92a6060dd0db190a61afa
    Specification   :   和官方的结果略有不同，小数点后第8位存在一定的误差
    """
    if(kernelLength%2 != 1) or (kernelLength<=0):
        print("Kernel Length Should Be Odd and Positive.")
        return None
    
    kernel = np.ndarray((kernelLength,1),dtype=np.float32)
    # print(kernel.shape)
    midPos = int((kernelLength-1)*0.5)
    kernelSum = 0
    for i in range(0,midPos+1):
        tempVal = math.exp(-(i-midPos)**2/(2*sigma**2))
        kernel[i,0] = tempVal
        kernel[kernelLength-i-1,0] = tempVal  # 轴对称
        kernelSum+=tempVal*2
    kernelSum -= kernel[midPos,0]  # 中间位置算了两遍，减掉一遍
    normalizedKernel = kernel/kernelSum  # normalization
    return normalizedKernel

def myGaussian2DFunction(sigma,xyPos):
    r"""
    FunctionName    :   myGaussian2DFunction
    FunctionDescribe:   自己写的二维高斯函数
    InputParameter  :   ①sigma(标准差，不是方差)
                        ②xyPos(待求点处的函数值)
    OutputParameter :   ①result(函数值)
    """
    xPos = xyPos[0]
    yPos = xyPos[1]
    variance = sigma**2
    result = myGaussian1DFunction(sigma,xPos)*myGaussian1DFunction(sigma,yPos)  # 不相关，也独立的二维正态分布
    # resultAnother = (1/(2*math.pi*variance))*math.exp(-(xPos**2+yPos**2)/(2*variance))
    # print("Diff of 2 calculating methods: ", result - resultAnother)
    return result

def myGaussian2DKernel(kernelSize,sigma):
    r"""
    FunctionName    :   
    FunctionDescribe:   
    InputParameter  :   ①
    OutputParameter :   ①
    Specification   :   kernel元素之和不一定为1，可能会有些误差。eg：myGaussian2DKernel(5,5)的和为0.99999994
    """
    gaussian1DKernel = myGaussian1DKernel(kernelSize,sigma)
    return gaussian1DKernel*gaussian1DKernel.T


if __name__ == "__main__":
    r"""
    FunctionName    :   
    FunctionDescribe:   
    InputParameter  :   ①
    OutputParameter :   ①
    Specification   :   
    """

    print(myGaussian1DKernel(5,5))
    print(myGaussian2DKernel(5,5))
    print(myGaussian2DKernel(5,5).sum())

    pass