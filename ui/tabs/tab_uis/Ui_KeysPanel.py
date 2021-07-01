from functools import partial

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QLabel,QCheckBox, QHBoxLayout, QPushButton, \
    QGridLayout

from ui.custom_styles import CustomQStyles
from ui.dialogs.change_key_dialog import ChangeKeyDialog

# FULL_MODEL_PATH = os.getcwd() + '/data/results/training_data'
from ui.dialogs.supported_keys_dialog import AllKeysDialog

FULL_MODEL_PATH = '/data/results/training_data'


class Ui_KeysPanel(object):

    def setupUi(self, KeysWidget):
        self.mainLayout = QGridLayout(KeysWidget)
        self.buttons = []
        self.exercises = []
        self.checks = []
        print("init keyspanel!")
        self.loadExerciseKeys(KeysWidget)
        self.classification = KeysWidget.classifyExercises

        self.actions = QHBoxLayout()
        self.supportedKeys = QPushButton('Supported keys')
        self.supportedKeys.setStyleSheet(CustomQStyles.outlineButtonStyle)
        self.supportedKeys.setFixedHeight(35)
        self.supportedKeys.setIcon(QIcon.fromTheme("dialog-information"))
        self.supportedKeys.clicked.connect(self.allKeyDialog)

        self.saveProfile = QPushButton('Save keys')
        self.saveProfile.setStyleSheet(CustomQStyles.buttonStyle)
        self.saveProfile.setFixedHeight(35)

        self.actions.addWidget(self.supportedKeys)
        self.actions.addWidget(self.saveProfile)
        self.mainLayout.addLayout(self.actions, self.mainLayout.rowCount(), 0)

    def loadExerciseKeys(self, KeysWidget):
        self.deleteItemsOfLayout(self.mainLayout)
        self.exercises.clear()
        self.buttons.clear()
        self.checks.clear()
        if KeysWidget.classifyExercises is not None:
            for ind in range(0, len(KeysWidget.classifyExercises.exercises)):
                self.exercises.append(KeysWidget.classifyExercises.exercises[ind])
                self.createRow(exercise=KeysWidget.classifyExercises.exercises[ind], index=ind)

    def createRow(self, exercise, index):
        item = QHBoxLayout()
        label = QLabel(exercise.name)
        item.addWidget(label)
        item.setAlignment(label, Qt.Alignment.AlignCenter)
        button = QPushButton(exercise.assigned_key[0])
        # button.installEventFilter(self)
        button.setStyleSheet(CustomQStyles.keyButtonStyle)
        button.clicked.connect(partial(self.openDialog, button))
        self.buttons.append(button)
        item.addWidget(button)
        check = QCheckBox("Hold")
        check.setChecked(exercise.assigned_key[2])
        check.stateChanged.connect(partial(self.checkChanged, check))
        self.checks.append(check)
        item.addWidget(check)
        self.mainLayout.addLayout(item, index, 0)
        print(index, exercise.name, exercise.assigned_key)


    def deleteItemsOfLayout(self, layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.setParent(None)
                    else:
                        self.deleteItemsOfLayout(item.layout())

    def checkChanged(self, check):
        index = self.checks.index(check)
        exercise = self.exercises[index]
        exercise.assigned_key = (exercise.assigned_key[0], exercise.assigned_key[1], not exercise.assigned_key[2])
        print("Holding:", exercise.assigned_key[2])

    def openDialog(self, button):
        index = self.buttons.index(button)
        button.setStyleSheet(CustomQStyles.keyButtonStyle)
        dialog = ChangeKeyDialog(
            buttons=self.buttons,
            exercises=self.exercises,
            index=index
        )
        dialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        result = dialog.exec()
        if result == 1:
            # Swap keys in classification
            self.classification.change_key(self.exercises[index])
        # if button is QPushButton:

    def allKeyDialog(self):
        dialog = AllKeysDialog()
        dialog.exec()
