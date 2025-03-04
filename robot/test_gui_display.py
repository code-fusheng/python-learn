from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import sys
import cv2

# pip install --upgrade PyQt5 sip

class TestGuiDisplay(QMainWindow):
    def __init__(self, screen, image_path):
        super().__init__()
        self.setGeometry(screen.geometry())  # 设置窗口为屏幕大小

        # 创建 QLabel 来显示图像
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # 尝试打开文件作为视频流
        self.cap = cv2.VideoCapture(image_path)
        self.is_mjpeg = self.cap.isOpened()  # 判断是否为 MJPEG 流

        if self.is_mjpeg:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)
        else:
            pixmap = QPixmap(image_path)
            self.label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatio))

    def update_frame(self):
        # 动态更新帧
        if self.is_mjpeg:
            ret, frame = self.cap.read()
            if ret:
                # 转换为 QImage 格式并显示
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = channel * width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.label.setPixmap(QPixmap.fromImage(q_image))
            else:
                # 到文件末尾则循环播放
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def keyPressEvent(self, event):
        # 按下 Esc 键退出全屏
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        # 关闭时释放视频资源
        if self.is_mjpeg:
            self.cap.release()

def main():
    app = QApplication(sys.argv)
    screens = app.screens()  # 获取所有屏幕
    print(len(screens))

    for i, screen in enumerate(screens):
        print(f"屏幕 {i+1} 的信息:")
        print(f" - 屏幕名称: {screen.name()}")
        print(f" - 逻辑尺寸: {screen.size()}")         # 逻辑尺寸 (像素大小)
        print(f" - 几何信息: {screen.geometry()}")      # 屏幕几何信息
        print(f" - 物理尺寸: {screen.physicalSize()}")  # 物理尺寸 (毫米)
        print(f" - 分辨率: {screen.size().width()}x{screen.size().height()}")
        print(f" - 刷新率: {screen.refreshRate()} Hz") # 刷新率
        print(f" - DPI: {screen.logicalDotsPerInch()}")# DPI
        print("-" * 30)

    faces = []

    face1 = "image/test1.jpeg"  # 表情1
    face2 = "image/test2.jpeg"   # 表情2
    face3 = "image/test3.jpeg"   # 表情3

    window1 = TestGuiDisplay(screens[1], face2)
    # window1.show()
    # 设置全屏显示
    window1.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()