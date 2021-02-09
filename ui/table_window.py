import sys
from PyQt6 import QtGui, QtWidgets
# 1. Import `QApplication` and all the required widgets
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QVBoxLayout, QMainWindow, \
    QTabWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QWidget

from ui.tab_one import TrainWidget


class MainTabWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)
        self.tabs.addTab(self.tab1, "Train")
        self.tabs.addTab(self.tab2, "Test")
        self.tabs.addTab(self.tab3, "Map")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.setTabWidgets()

    def setTabWidgets(self):
        # Tab1 widgets:
        self.tab1.layout = TrainWidget(self)
        self.tab1.setLayout(self.tab1.layout)

    def on_click_select_tab2(self):
        self.tabs.setCurrentIndex(1)
