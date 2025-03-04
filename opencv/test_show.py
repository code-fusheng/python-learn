import cv2 as cv

if __name__ == '__main__':

    # 读取图像文件 支持 BMP、JPG、PNG、TIFF 等格式

    filePath = "source/images/full_冀R17BZ1.jpg"
    img = cv.imread(filePath, flags=1)      # flags=1 读取彩色图像文件(BGR)
    gray = cv.imread(filePath, flags=0)     # flags=0 读取灰度图像

    cv.imshow("img", img)
    cv.imshow("gray", gray)
    key = cv.waitKey(0)
    cv.destoryAllWindows()