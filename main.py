import sys
from PyQt6 import QtGui
# 1. Import `QApplication` and all the required widgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMainWindow
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QWidget

from classify import ClassifyExercises
from constants.variables import number_of_samples, PREDEFINED_EXERCISES
from ui.table_window import MainTabWidget


class HIMOApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left = int(self.screen().size().width() / 4)
        self.top = int(self.screen().size().height() / 4)
        self.width = 640
        self.height = 450

        self.title = 'HIMO - Health In Motion'

        self.classifyExercises = ClassifyExercises(
            # subject="Ervin",
            nr_of_samples=number_of_samples,
            epochs=300,
            # nr_of_gestures=4,
            exercises=PREDEFINED_EXERCISES,
            # batch_size=50,
            training_batch_size=16
        )
        self.table_widget = MainTabWidget(self)

        bar = self.menuBar()
        about = bar.addMenu("About")
        info = QAction("App Information", self)
        about.triggered[QAction].connect(self.aboutThis)
        about.addAction(info)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setCentralWidget(self.table_widget)

        self.show()

    def aboutThis(self, q):
        print(q.text() + " is triggered")


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = QWidget()
    # window.setWindowTitle()

    app = QApplication(sys.argv)
    ex = HIMOApp()

    # 5. Run your application's event loop (or main loop)
    sys.exit(app.exec())
