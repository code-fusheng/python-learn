import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
)


class BasicWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口属性
        self.setWindowTitle("Basic PyQt Window")
        self.setGeometry(100, 100, 600, 400)

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 布局管理器
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 添加控件
        self.label = QLabel("Welcome to PyQt!", self)
        self.layout.addWidget(self.label)

        self.button = QPushButton("Click Me", self)
        self.layout.addWidget(self.button)

        # 连接信号槽
        self.button.clicked.connect(self.on_button_click)

        # 设置菜单栏
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")
        about_action = file_menu.addAction("About")
        exit_action = file_menu.addAction("Exit")

        # 连接菜单信号
        about_action.triggered.connect(self.show_about_message)
        exit_action.triggered.connect(self.close)

        # 设置状态栏
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")

    def on_button_click(self):
        """按钮点击事件"""
        QMessageBox.information(self, "Message", "Button clicked!")

    def show_about_message(self):
        """显示关于信息"""
        QMessageBox.about(self, "About", "This is a basic PyQt window example.")


if __name__ == "__main__":
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 创建主窗口
    window = BasicWindow()
    window.show()

    # 运行应用程序
    sys.exit(app.exec_())
