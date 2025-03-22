import cv2
import numpy as np


def featureSIFT(imgGray):
    """
    SIFT : https://docs.opencv.org/3.4/da/df5/tutorial_py_sift_intro.html
    """
    siftObject = cv2.SIFT_create()  # 创建一个 SIFT 对象
    kp, des = siftObject.detectAndCompute(imgGray, None)  # 同时找到关键点并计算描述符
    print(f"SIFT Descriptor Length : {des.shape[-1]}")  # 关键点对应一个 128 维的向量
    print(f"SIFT Detected Feature Points : {des.shape[0]}")

    imgSIFT = cv2.drawKeypoints(imgGray, kp, None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # 显示每个关键点的大小和方向

    # cv2.imshow("SIFT Effect", imgSIFT)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return imgSIFT


def featureSURF(imgGray):
    """
    SURF : https://docs.opencv.org/3.4/df/dd2/tutorial_py_surf_intro.html
    """
    surfObject = cv2.xfeatures2d.SURF_create(400)
    kp, des = surfObject.detectAndCompute(imgGray, None)
    print(f"ORB Descriptor Length : {des.shape[-1]}")
    print(f"ORB Detected Feature Points : {des.shape[0]}")

    imgSURF = cv2.drawKeypoints(imgGray, kp, None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # 显示每个关键点的大小和方向

    # cv2.imshow("SURF Effect", imgSURF)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return imgSURF


def featureORB(imgGray):
    """
    ORB : https://docs.opencv.org/3.4/d1/d89/tutorial_py_orb.html
    """
    orbObject = cv2.ORB_create()
    kp, des = orbObject.detectAndCompute(imgGray, None)
    print(f"ORB Descriptor Length : {des.shape[-1]}")
    print(f"ORB Detected Feature Points : {des.shape[0]}")

    imgORB = cv2.drawKeypoints(imgGray, kp, None,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  # 显示每个关键点的大小和方向

    # cv2.imshow("ORB Effect", imgORB)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return imgORB




if __name__ == "__main__":
    imgPath = r"./Pics/asuka.jpg"
    # imgPath = r"./Pics/lena.jpg"
    imgPath = r"./Pics/lena_high.jpg"
    # imgPath = r"./Pics/lena_unpub.jpg"

    imgBGR = cv2.imread(imgPath, flags=cv2.IMREAD_COLOR)
    imgGray = cv2.cvtColor(imgBGR, code=cv2.COLOR_BGR2GRAY)

    imgSIFT = featureSIFT(imgGray)
    # imgSURF = featureSURF(imgGray)
    imgORB = featureORB(imgGray)

    imgFull = np.concatenate([imgBGR, imgSIFT, imgORB], axis=1)
    print(f"imgFull.shape  =  {imgFull.shape}")
    imgFullHalf = cv2.resize(imgFull, dsize=None, fx=1/2, fy=1/2)
    print(f"imgFullHalf.shape={imgFullHalf.shape}")

    cv2.imshow("Effects", imgFullHalf)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
