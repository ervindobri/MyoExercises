from functools import partial

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QPushButton, \
    QGridLayout
from pynput.keyboard import Key

from ui.custom_widgets.change_key_dialog import ChangeKeyDialog
from ui.custom_widgets.key_monitor import KeyMonitor

# FULL_MODEL_PATH = os.getcwd() + '/data/results/training_data'
FULL_MODEL_PATH = '/data/results/training_data'


def on_press(key):
    print('{0} pressed'.format(
        key))


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False


class Ui_KeysPanel(object):


    def setupUi(self, KeysWidget):
        self.mainLayout = QGridLayout(KeysWidget)
        self.buttons = []
        self.exercises = []

        if KeysWidget.classifyExercises is not None:
            for x, ind in zip(KeysWidget.classifyExercises.exercises,
                              range(0, len(KeysWidget.classifyExercises.exercises))):
                self.exercises.append(KeysWidget.classifyExercises.exercises[x])
                self.createRow(exercise=KeysWidget.classifyExercises.exercises[x], index=ind)

        self.monitor = KeyMonitor()
        # self.monitor.keyPressed.connect(self.onKeyPress)
        self.monitor.start_monitoring()

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start()

    def onTimeout(self):
        if self.monitor.released:
            for b in self.buttons:
                b.setStyleSheet(
                    """ QPushButton
                    {
                        border: 1px solid grey;
                        background-color: white;
                    }
                    """)
        else:
            for ind in range(0, len(self.exercises)):
                if self.monitor.currentKey == self.exercises[ind].assigned_key[1]:
                    self.buttons[ind].setStyleSheet(
                    """ QPushButton
                    {
                        border: 1px solid green;
                        background-color: #7FFFD4;
                    }
                    """)

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

    # def eventFilter(self, source, event):
    #     print(event)

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
        dialog.exec()
        # if button is QPushButton:
