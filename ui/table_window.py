# 1. Import `QApplication` and all the required widgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QTabWidget
from PyQt6.QtWidgets import QWidget

from ui.custom_styles import CustomQStyles
from ui.tabs.tab_train import TrainWidget
from ui.tabs.tab_keys import KeysWidget


class MainTabWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.classifyExercises = parent.classifyExercises
        self.infoLabel = parent.informationLabel

        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(10, 10, 10, 10)
        self.tabs.setStyleSheet(CustomQStyles.tabStyle)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)
        self.tabs.addTab(self.tab1, "Train")
        # self.tabs.addTab(self.tab2, "Test")
        self.tabs.addTab(self.tab3, "Keys")
        self.tabs.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setTabWidgets()

    def setTabWidgets(self):
        # Tab1 widgets:
        layout = QHBoxLayout()
        layout.addWidget(TrainWidget(self))
        self.tab1.layout = layout
        self.tab1.setLayout(self.tab1.layout)

        # self.tab2.layout = TestWidget(self)
        # self.tab2.setLayout(self.tab2.layout)

        layout2 = QHBoxLayout()
        layout2.addWidget(KeysWidget(self))

        self.tab3.layout = layout2
        self.tab3.setLayout(self.tab3.layout)

    def on_click_select_tab2(self):
        self.tabs.setCurrentIndex(1)
