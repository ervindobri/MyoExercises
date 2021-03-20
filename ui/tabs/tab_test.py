from random import random, randint

from PyQt6 import QtCore
from PyQt6.QtWidgets import QVBoxLayout, QBoxLayout, QHBoxLayout, QLabel, QSpinBox, QPushButton, QLayout, QProgressBar
from scipy import rand


class TestWidget(QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.classifyExercises = parent.classifyExercises
        self.columns = ['Set', 'Exercise', 'Assigned Key', 'Accuracy', 'Latency', 'Avg.lat']
        self.exerciseLayouts = []
        self.setButtons = []
        self.initUi()
        print("init tab2")

    def initUi(self):
        # top labels
        self.mainLayout = QVBoxLayout()
        self.labels = QHBoxLayout()
        for x in self.columns:
            label = QLabel(x)
            self.labels.addWidget(label)
            self.labels.setAlignment(label, QtCore.Qt.Alignment.AlignHCenter)

        self.mainLayout.addLayout(self.labels)
        self.mainLayout.setAlignment(self.labels, QtCore.Qt.Alignment.AlignTop)
        if self.classifyExercises is not None:
            for e in range(0, self.classifyExercises.number_of_gestures):
                alignment = self.exerciseLayout(e)
                self.mainLayout.addLayout(alignment)
                self.mainLayout.setAlignment(alignment, QtCore.Qt.Alignment.AlignTop)
        self.addLayout(self.mainLayout)
        self.setAlignment(self.mainLayout, QtCore.Qt.Alignment.AlignTop)

    def exerciseLayout(self, index):
        hLayout = QHBoxLayout()
        setSpinBox = QSpinBox()
        setSpinBox.setRange(1, 100)
        setSpinBox.setValue(5)
        setSpinBox.setMaximumWidth(80)

        startButton = QPushButton(list(self.classifyExercises.exercises.values())[index].name)
        startButton.setMaximumWidth(120)

        assignedKey = QPushButton(list(self.classifyExercises.exercises.values())[index].assigned_key[0])
        assignedKey.setStyleSheet('background-color: grey; color: white;')
        assignedKey.setMaximumWidth(50)
        assignedKey.setEnabled(False)

        progress = QProgressBar()
        progress.setMaximumWidth(150)
        progress.setValue(randint(1, 100))
        progress.setAlignment(QtCore.Qt.Alignment.AlignCenter)

        latency = QLabel(str(randint(50, 250)) + 'ms')

        avgLatency = QLabel(str(randint(50, 250)) + 'ms')

        hLayout.addWidget(setSpinBox)
        hLayout.setAlignment(setSpinBox, QtCore.Qt.Alignment.AlignHCenter)
        hLayout.addWidget(startButton)
        hLayout.setAlignment(startButton, QtCore.Qt.Alignment.AlignHCenter)
        hLayout.addWidget(assignedKey)
        hLayout.setAlignment(assignedKey, QtCore.Qt.Alignment.AlignHCenter)
        hLayout.addWidget(progress)
        hLayout.setAlignment(progress, QtCore.Qt.Alignment.AlignHCenter)
        hLayout.addWidget(latency)
        hLayout.setAlignment(latency, QtCore.Qt.Alignment.AlignHCenter)
        hLayout.addWidget(avgLatency)
        hLayout.setAlignment(avgLatency, QtCore.Qt.Alignment.AlignHCenter)

        hLayout.setContentsMargins(0, 10, 0, 10)
        self.exerciseLayouts.append(hLayout)
        return hLayout
