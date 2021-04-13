import json
import os
from PyQt6.QtCore import QTimer, QSize, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout
from pynput.keyboard import KeyCode

from constants.variables import KEYS, SUPPORTED_KEYS, MAPPED_KEYS_PATH
from ui.custom_widgets.key_monitor import KeyMonitor


class SessionDialog(QDialog):
    def __init__(self, parent=None):
        super(SessionDialog, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Session")
        self.setLayout(layout)
