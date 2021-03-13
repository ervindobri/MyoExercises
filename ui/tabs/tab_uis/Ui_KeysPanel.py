import os
from functools import partial
from os import listdir
from os.path import join, isfile

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QTimer, QObject
from PyQt6.QtGui import QPixmap, QIcon, QCursor
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QFormLayout, QLineEdit, QPushButton, \
    QCheckBox, QProgressBar, QListWidget, QGroupBox, QMessageBox, QSizePolicy, QListWidgetItem, QSlider, QApplication, \
    QWizard, QWizardPage, QStyle, QGridLayout, QLayoutItem, QWidget
from pynput.keyboard import Controller
from pynput.keyboard import Key, Listener

from constants.variables import Exercise
from input import InputController
from ui.custom_slider import Slider
from ui.custom_widgets.custom_progressbar import ProgressBar
from ui.custom_widgets.key_monitor import KeyMonitor
from ui.custom_widgets.two_list_selection import TwoListSelection
from ui.dialog import DateDialog

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
        # if button is QPushButton:
