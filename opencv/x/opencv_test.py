import cv2

# cv2.imread 用于从指定文件加载图像并返回图像的矩阵(多维的Numpy数组)
def test_open_image():
    img = cv2.imread("source/fusheng.jpg")
    cv2.imshow("T1", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    test_open_image()
    pass