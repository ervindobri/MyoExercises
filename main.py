import sys
from PyQt6 import QtGui
# 1. Import `QApplication` and all the required widgets
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMainWindow
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QWidget

from ui.table_window import MainTabWidget


class HIMOApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'HIMO - Health In Motion'
        self.left = int(self.screen().size().width()/4)
        self.top = int(self.screen().size().height()/4)
        self.width = 640
        self.height = 450
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MainTabWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()




if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = QWidget()
    # window.setWindowTitle()

    app = QApplication(sys.argv)
    ex = HIMOApp()

    # 5. Run your application's event loop (or main loop)
    sys.exit(app.exec())