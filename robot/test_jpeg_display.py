import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage


class MJPEGDisplay(QMainWindow):
    def __init__(self, screen, mjpeg_path):
        super().__init__()
        self.setWindowTitle("MJPEG 动态显示")

        # 设置全屏在指定屏幕上显示
        geometry = screen.geometry()
        self.setGeometry(geometry)

        # 设置 QLabel 来显示图像
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        # 打开 MJPEG 文件（假设路径是 MJPEG 文件路径）
        self.cap = cv2.VideoCapture(mjpeg_path)
        if not self.cap.isOpened():
            print("无法打开 MJPEG 文件")
            sys.exit()

        # 设置定时器定期刷新图像
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 约 30 毫秒刷新一次帧

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # 转换为 QImage 格式并显示
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(q_image))
        else:
            # 若读到文件末尾，可选择重新播放
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 重头开始

    def keyPressEvent(self, event):
        # 按下 Esc 键退出全屏
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        # 关闭时释放 MJPEG 文件
        self.cap.release()

def main():
    app = QApplication(sys.argv)

    # 获取所有屏幕
    screens = app.screens()

    # 设置 MJPEG 文件路径
    mjpeg_path = "image/test1.jpeg"  # 替换为您的 MJPEG 文件路径

    # 在第二个屏幕上显示动态表情
    window1 = MJPEGDisplay(screens[1], mjpeg_path)
    window1.showFullScreen()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
