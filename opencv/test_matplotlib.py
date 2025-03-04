# pip3 install packaging
# pip3 install --upgrade packaging

import cv2 as cv
from matplotlib import pyplot as plt

if __name__ == '__main__':

    filePath = "source/fusheng.jpg"
    img = cv.imread(filePath, flags=1)  # 读取彩色图像(BGR)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    plt.figure(figsize=(8, 7))  # 创建自定义图像
    plt.subplot(221), plt.title("1. RGB (Matplotlib)"), plt.axis('off')
    plt.imshow(imgRGB)

    plt.subplot(222), plt.title("2. BGR (OpenCV)"), plt.axis('off')
    plt.imshow(img)

    plt.subplot(223), plt.title("3. cmap='gray'"), plt.axis('off')
    plt.imshow(gray, cmap='gray')

    plt.subplot(224), plt.title("4. without cmap"), plt.axis('off')
    plt.imshow(gray)

    plt.tight_layout()  # 自动调整子图间隔
    plt.show()