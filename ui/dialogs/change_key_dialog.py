import json
import os
from PyQt6.QtCore import QTimer, QSize, Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout
from pynput.keyboard import KeyCode

from constants.variables import KEYS, SUPPORTED_KEYS, MAPPED_KEYS_PATH
from ui.custom_styles import CustomQStyles
from ui.custom_widgets.key_monitor import KeyMonitor


class ChangeKeyDialog(QDialog):
    def __init__(self, parent=None,
                 buttons=None,
                 exercises=None,
                 index: int = None,
                 ):
        super(ChangeKeyDialog, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.setWindowTitle('Swap keys')
        self.setMinimumWidth(250)

        widget = QWidget()
        keyLayout = QVBoxLayout()
        widget.setStyleSheet("""
        QWidget{
            border-radius: 12px;
            border: 1px solid grey;
            background-color: #b5b5b5;
            color: white;
            font-size: 40px;
        }
        """)
        # widget.setFixedSize(100, 100)
        self.currentKeyLabel = QLabel('W')
        keyLayout.addWidget(self.currentKeyLabel)
        keyLayout.setAlignment(self.currentKeyLabel, Qt.Alignment.AlignCenter)
        widget.setLayout(keyLayout)

        label = QLabel("Press a key to swap " + exercises[index].name)
        emptyKey = QPushButton('Use empty slot')
        emptyKey.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        emptyKey.setStyleSheet(CustomQStyles.outlineButtonStyle)
        emptyKey.setFixedHeight(35)
        emptyKey.clicked.connect(self.useEmpty)

        acceptKey = QPushButton('Accept')
        acceptKey.clicked.connect(self.acceptNewKey)
        acceptKey.setStyleSheet(CustomQStyles.buttonStyle)
        acceptKey.setFixedHeight(35)
        acceptKey.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        layout.addWidget(label)
        layout.addWidget(widget)
        actions = QHBoxLayout()
        actions.addWidget(emptyKey)
        actions.addWidget(acceptKey)
        actions.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(actions)
        layout.setAlignment(label, Qt.Alignment.AlignCenter)
        layout.setAlignment(widget, Qt.Alignment.AlignCenter)
        self.buttons = buttons
        self.exercises = exercises
        self.index = index


        self.monitor = KeyMonitor()
        self.monitor.start_monitoring()
        self.currentKey = self.monitor.currentKey

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start()
        print("Dialog init done!")

    def acceptNewKey(self):
        currentKeyScheme = [e.assigned_key for e in self.exercises]
        print(self.exercises[self.index].assigned_key)

        # Check if pressed key is among
        if self.currentKey in currentKeyScheme:
            for name, key in SUPPORTED_KEYS.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                if key == self.currentKey:
                    old_exercise = None
                    old_button = None
                    for exercise, button in zip(self.exercises, self.buttons):
                        if exercise.assigned_key == (name, key) and button.text() == name:
                            old_exercise = exercise
                            old_button = button

                    # Set new keys and labels
                    if old_exercise is not None and old_button is not None:
                        self.exercises[
                            self.index].assigned_key, old_exercise.assigned_key = old_exercise.assigned_key, \
                                                                                  self.exercises[
                                                                                      self.index].assigned_key
                        old_label = old_button.text()
                        old_button.setText(self.buttons[self.index].text())
                        self.buttons[self.index].setText(old_label)
                        print("old key:", old_exercise.assigned_key)
                        print("new key:", self.exercises[self.index].assigned_key)
                        self.timer.stop()
                        self.close()
        else:
            self.exercises[self.index].assigned_key = self.currentKey
            print("pos:", list(SUPPORTED_KEYS.keys())[list(SUPPORTED_KEYS.values()).index(self.currentKey[1])])
            self.buttons[self.index].setText(list(SUPPORTED_KEYS.keys())[list(SUPPORTED_KEYS.values())
                                             .index(self.currentKey[1])])
            self.timer.stop()
            self.accept()

    def useEmpty(self):
        self.currentKey = ("Empty", None)
        self.exercises[self.index].assigned_key = self.currentKey
        self.buttons[self.index].setText(self.currentKey[0])
        self.timer.stop()
        self.close()

    def onTimeout(self):
        if self.monitor is not None:
            if self.monitor.currentKey in list(SUPPORTED_KEYS.values()):
                if type(self.monitor.currentKey) is KeyCode:
                    self.currentKeyLabel.setText(self.monitor.currentKey.char)
                else:
                    self.currentKeyLabel.setText(str(self.monitor.currentKey))
                name = list(SUPPORTED_KEYS.keys())[list(SUPPORTED_KEYS.values()).index(self.monitor.currentKey)]
                self.currentKey = (name, self.monitor.currentKey)


    def writeExerciseKeyMap(self):
        with open(os.getcwd() + MAPPED_KEYS_PATH + self.subject + '.json', 'w') as fp:
            json.dump(self.exercises, fp)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getSwapper(parent=None):
        dialog = ChangeKeyDialog(parent)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
