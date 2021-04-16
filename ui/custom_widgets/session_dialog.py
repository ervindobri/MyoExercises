import json
import os
from PyQt6.QtCore import QTimer, QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout, QComboBox
from pynput.keyboard import KeyCode

from constants.variables import KEYS, SUPPORTED_KEYS, MAPPED_KEYS_PATH, PREDEFINED_EXERCISES
from ui.custom_styles import CustomQStyles
from ui.custom_widgets.key_monitor import KeyMonitor


class SessionDialog(QDialog):
    def __init__(self, parent=None,
                 patient=None
                 ):
        super(SessionDialog, self).__init__(parent)
        layout = QHBoxLayout(self)
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Session")
        self.setLayout(layout)
        self.setParent(parent)
        self.patient = patient
        options = QVBoxLayout()
        for ex in self.patient.exercises:
            exercise = next(x for x in PREDEFINED_EXERCISES if x.code == ex)
            options.addWidget(QLabel(exercise.name))
            box = QComboBox()
            box.addItems(['5', '10', '15'])
            options.addWidget(box)
            options.setAlignment(box, Qt.Alignment.AlignTop)

        startButton = QPushButton('Start Session')
        startButton.setStyleSheet(CustomQStyles.buttonStyle)
        startButton.clicked.connect(self.startSession)
        startButton.setFixedSize(120, 35)
        options.addWidget(startButton)
        options.setAlignment(startButton, Qt.Alignment.AlignCenter)

        # Session panel
        session = QVBoxLayout()
        self.exerciseWidget = QVBoxLayout()
        self.exerciseLabel = QLabel('Exercise name')
        self.exerciseImage = QLabel()
        self.exerciseImage.setPixmap(QPixmap(os.getcwd() + "/resources/images/frame.png"))
        self.exerciseWidget.addWidget(self.exerciseLabel)
        self.exerciseWidget.setAlignment(self.exerciseLabel, Qt.Alignment.AlignCenter)
        self.exerciseWidget.addWidget(self.exerciseImage)

        session.addLayout(self.exerciseWidget)
        session.setAlignment(self.exerciseWidget, Qt.Alignment.AlignCenter)
        layout.addLayout(options, stretch=1)
        layout.addLayout(session, stretch=2)
        # TODO: display timer
        # TODO: session thread, start session

    def startSession(self):
        print("Starting timer and session!")
