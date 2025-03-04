import cv2 as cv
import numpy as np
import urllib.request as request

if __name__ == '__main__':

    response = request.urlopen("https://robot.4-xiang.com/htc-image/2025-03-03/small_%E9%84%82AT465K_20250303163306816.jpg")
    imgUrl = cv.imdecode(np.array(bytearray(response.read()), dtype=np.uint8), -1)
    cv.imshow("imgUrl", imgUrl)
    key = cv.waitKey(5000)  # 0 标识无限延迟
    cv.destoryAllWindows()