import cv2

if __name__ == "__main__":
    img = cv2.imread("/home/lzy/Pictures/uniqueID.png", cv2.IMREAD_COLOR)
    print(img.shape)

    imgResize = cv2.resize(img, (500,500))

    cv2.imshow("img", img)
    cv2.imshow("imgResize", imgResize)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
