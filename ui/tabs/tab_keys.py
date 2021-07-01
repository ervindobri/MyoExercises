import json
import os

from PyQt6 import QtCore
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget

from constants.variables import MAPPED_KEYS_PATH
from ui.custom_styles import CustomQStyles
from ui.custom_widgets.key_monitor import KeyMonitor
from ui.tabs.tab_uis.Ui_KeysPanel import Ui_KeysPanel


class KeysWidget(QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self, parent=None):
        super(KeysWidget, self).__init__(parent)
        self.classifyExercises = None
        if parent is not None:
            self.classifyExercises = parent.classifyExercises
            self.infoLabel = parent.infoLabel

        self.ui = Ui_KeysPanel()
        self.ui.setupUi(self)
        self.monitor = KeyMonitor()
        self.monitor.start_monitoring()

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start()

        self.ui.saveProfile.clicked.connect(self.saveBindings)

    def saveBindings(self):
        print(str(len(self.classifyExercises.exercises)) + " exercises")
        self.classifyExercises.SavePatientData()
        if self.classifyExercises.subject is not None:
            key_list = [x.serialize() for x in self.classifyExercises.exercises]
            content = {
                self.classifyExercises.subject: key_list
            }
            print(content)
            with open(MAPPED_KEYS_PATH + self.classifyExercises.subject + '.json', "w") as f:
                json.dump(content, f)

    def onTimeout(self):
        if self.monitor.released:
            for b in self.ui.buttons:
                b.setStyleSheet(CustomQStyles.keyButtonStyle)
        else:
            for ind in range(0, len(self.ui.exercises)):
                if self.monitor.currentKey == self.ui.exercises[ind].assigned_key[1]:
                    self.ui.buttons[ind].setStyleSheet(CustomQStyles.pressedKeyButtonStyle)

