from functools import partial

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, \
    QGridLayout
from ui.dialogs.change_key_dialog import ChangeKeyDialog

# FULL_MODEL_PATH = os.getcwd() + '/data/results/training_data'
from ui.dialogs.supported_keys_dialog import AllKeysDialog

FULL_MODEL_PATH = '/data/results/training_data'


class Ui_KeysPanel(object):

    def setupUi(self, KeysWidget):
        self.mainLayout = QGridLayout(KeysWidget)
        self.buttons = []
        self.exercises = []

        if KeysWidget.classifyExercises is not None:
            for ind in range(0, len(KeysWidget.classifyExercises.exercises)):
                self.exercises.append(KeysWidget.classifyExercises.exercises[ind])
                self.createRow(exercise=KeysWidget.classifyExercises.exercises[ind], index=ind)
        self.actions = QHBoxLayout()
        self.supportedKeys = QPushButton('Supported keys')
        self.supportedKeys.setIcon(QIcon.fromTheme("dialog-information"))
        self.supportedKeys.clicked.connect(self.allKeyDialog)

        self.saveProfile = QPushButton('Save keys')

        self.actions.addWidget(self.supportedKeys)
        self.actions.addWidget(self.saveProfile)
        self.mainLayout.addLayout(self.actions, self.mainLayout.rowCount(), 0)

    def createRow(self, exercise, index):
        item = QHBoxLayout()
        label = QLabel(exercise.name)
        item.addWidget(label)
        item.setAlignment(label, Qt.Alignment.AlignCenter)
        button = QPushButton(exercise.assigned_key[0])
        # button.installEventFilter(self)
        button.setStyleSheet(
            """ QPushButton
            {
                border: 1px solid grey;
                background-color: white;
            }
            """)
        button.clicked.connect(partial(self.openDialog, button))
        self.buttons.append(button)
        item.addWidget(button)
        self.mainLayout.addLayout(item, index, 0)
        print(index, exercise.name, exercise.assigned_key)

    def openDialog(self, button):
        print(button)
        index = self.buttons.index(button)
        button.setStyleSheet(
            """ QPushButton
            {
                border: 1px solid #B8B8B8;
                background-color: grey;
            }
            """)
        dialog = ChangeKeyDialog(
            buttons=self.buttons,
            exercises=self.exercises,
            index=index
        )
        dialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        dialog.exec()
        # if button is QPushButton:

    def allKeyDialog(self):
        dialog = AllKeysDialog()
        dialog.exec()
