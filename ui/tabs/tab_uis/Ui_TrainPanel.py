import functools
import json
import os
from os import listdir
from os.path import join, isfile

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QFormLayout, QLineEdit, QPushButton, \
    QCheckBox, QProgressBar, QListWidget, QGroupBox, QMessageBox, QSizePolicy, QListWidgetItem, QSlider, QWizard, \
    QWizardPage

from constants.variables import PATIENTS_PATH
from models.patient import Patient
from ui.custom_slider import Slider
from ui.custom_widgets.calibrate_wizard import CalibrateWizard
from ui.custom_widgets.two_list_selection import TwoListSelection
from ui.custom_styles import CustomQStyles
from ui.thread_helpers.thread_helpers import RecordThread

FULL_MODEL_PATH = os.getcwd() + '/data/results/training_data'


# FULL_MODEL_PATH = '/data/results/training_data'


class Ui_TrainPanel(object):

    def setupUi(self, TrainPanel):
        self.parent = TrainPanel

        self.mainLayout = QHBoxLayout(TrainPanel)
        self.epochValue = QLabel(parent=TrainPanel)
        self.vbox = QVBoxLayout(TrainPanel)
        self.label_maximum = QLabel(parent=TrainPanel)
        self.label_minimum = QLabel(parent=TrainPanel)
        self.slider_hbox = QHBoxLayout(TrainPanel)
        self.slider_vbox = QVBoxLayout(TrainPanel)
        # self.nrOfExercises = QSpinBox(TrainPanel)
        self.batchSizeMenu = QComboBox(TrainPanel)
        self.properties = QFormLayout(TrainPanel)
        self.epochSlider = Slider(orientation=QtCore.Qt.Orientations.Horizontal, parent=TrainPanel)

        self.subjectEdit = QLineEdit(TrainPanel)
        self.subjectEdit.setFixedHeight(30)
        self.subjectEdit.setText('Jozsika')
        self.subjectEdit.setStyleSheet(CustomQStyles.lineEditStyle)

        self.ageEdit = QLineEdit(TrainPanel)
        self.ageEdit.setFixedHeight(30)
        self.ageEdit.setValidator(QIntValidator())
        self.ageEdit.setText('5')
        self.ageEdit.setStyleSheet(CustomQStyles.lineEditStyle)

        self.subjectButton = QPushButton('New', parent=TrainPanel)
        self.subjectButton.setFixedHeight(30)
        self.subjectButton.setStyleSheet(CustomQStyles.outlineButtonStyle)

        # print(parent)
        self.actionsLayout = QHBoxLayout(TrainPanel)
        # self.checkRecording = QCheckBox(TrainPanel)
        self.calibrateButton = QPushButton("Calibrate", parent=TrainPanel)
        self.calibrateButton.setStyleSheet(CustomQStyles.buttonStyle)
        self.calibrateButton.setMinimumHeight(50)
        self.calibrateButton.setMaximumWidth(120)

        self.sessionButton = QPushButton("Session", parent=TrainPanel)
        self.sessionButton.setStyleSheet(CustomQStyles.outlineButtonStyle)
        self.sessionButton.setMinimumHeight(50)
        self.sessionButton.setMaximumWidth(120)

        self.trainButton = QPushButton('Train Model', parent=TrainPanel)
        self.resultButton = QPushButton('Show result image', parent=TrainPanel)
        self.progress = QProgressBar(TrainPanel)
        self.listFiles = QListWidget(TrainPanel)
        self.label = QLabel('or select', parent=TrainPanel)
        self.subjectLayout = QVBoxLayout(TrainPanel)
        self.optionsLayout = QVBoxLayout(TrainPanel)
        self.form_layout = QFormLayout(TrainPanel)
        self.form_layout2 = QFormLayout(TrainPanel)
        print("init")

        self.box1 = QGroupBox(title="Patient", parent=TrainPanel)
        self.box2 = QGroupBox(parent=TrainPanel)
        self.wizard = CalibrateWizard(parent=TrainPanel)

        self.setSubjectPanel(TrainPanel)  # right panel
        self.trainPanel(TrainPanel)  # left panel

        self.mainLayout.addWidget(self.box1, stretch=2)
        self.mainLayout.addWidget(self.box2, stretch=3)

        # self.retranslateUi(TrainPanel)

    # Display progress bar, checkbox - to record new gestures or not, start train
    def trainPanel(self, TrainPanel):

        hLayout = QHBoxLayout()
        hLayout.addLayout(self.form_layout2)
        hLayout.addWidget(self.calibrateButton)
        hLayout.addWidget(self.sessionButton)

        self.batchSizeMenu.addItems(['2', '4', '8', '16', '32', '64', '128'])
        self.batchSizeMenu.setCurrentIndex(3)
        self.batchSizeMenu.setMaximumWidth(100)

        self.initSlider()

        self.properties.addRow('Batch Size', self.batchSizeMenu)

        self.resultButton.setEnabled(False)

        self.actionsLayout.addWidget(self.trainButton)
        self.actionsLayout.addWidget(self.resultButton)

        self.optionsLayout.addLayout(hLayout)
        self.optionsLayout.addWidget(QLabel('Model properties'))
        self.optionsLayout.addLayout(self.vbox)
        self.optionsLayout.addLayout(self.properties)
        self.optionsLayout.addLayout(self.actionsLayout)
        self.progress.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.optionsLayout.addWidget(self.progress)
        # self.options_layout.addWidget(self.label)
        # self.options_layout.addWidget(self.list_widget)

        self.box2.setLayout(self.optionsLayout)

    def initSlider(self):
        self.epochValue.setAlignment(QtCore.Qt.Alignment.AlignHCenter)

        self.epochSlider.setMinimum(2)
        self.epochSlider.setMaximum(10)
        self.epochSlider.setTickInterval(1)
        # self.epochSlider.setInterval(1)
        # self.epochSlider.setValue(8)  # no idea why, but 8 is the middle somehow
        self.epochSlider.setSliderPosition(6)
        self.epochSlider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.label_minimum.setNum(self.epochSlider.minimum().real * 50)
        self.label_minimum.setAlignment(QtCore.Qt.Alignment.AlignLeft)
        self.label_maximum.setNum(self.epochSlider.maximum().real * 50)

        self.label_maximum.setAlignment(QtCore.Qt.Alignment.AlignRight)

        self.epochSlider.minimumChanged.connect(self.label_minimum.setNum)
        self.epochSlider.maximumChanged.connect(self.label_maximum.setNum)

        self.slider_hbox.addWidget(self.label_minimum, QtCore.Qt.Alignment.AlignLeft)
        self.slider_hbox.addWidget(self.epochValue)
        self.slider_hbox.addWidget(self.label_maximum, QtCore.Qt.Alignment.AlignRight)

        self.slider_vbox.addWidget(self.epochSlider)
        self.slider_vbox.addLayout(self.slider_hbox)
        # self.slider_vbox.addStretch()

        self.vbox.addLayout(self.slider_vbox)

    @staticmethod
    def showDialog(title, message, buttons: QMessageBox.StandardButtons):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setText(message)
        msgBox.setStandardButtons(buttons)
        # msgBox.buttonClicked.connect(msgButtonClick)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.StandardButtons.Ok:
            print('OK clicked')

    # Display list of subjects, or new subject
    def setSubjectPanel(self, TrainPanel):
        self.form_layout.addRow('Name', self.subjectEdit)
        self.form_layout.addRow('Age', self.ageEdit)
        self.form_layout.addWidget(self.subjectButton)

        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setAlignment(QtCore.Qt.Alignment.AlignCenter)

        self.loadPatientList()

        self.listFiles.setStyleSheet(CustomQStyles.listStyle)
        self.listFiles.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.subjectLayout.addLayout(self.form_layout)
        self.subjectLayout.addWidget(self.label)
        self.subjectLayout.addWidget(self.listFiles)

        self.box1.setLayout(self.subjectLayout)

    def loadPatientList(self):
        self.listFiles.clear()
        self.parent.patients.clear()
        files = [f for f in listdir(PATIENTS_PATH) if isfile(join(PATIENTS_PATH, f))]
        for x, ind in zip(files, range(0, len(files))):
            item = QListWidgetItem(x.split('.')[0])
            item.setTextAlignment(Qt.Alignment.AlignHCenter)
            self.listFiles.addItem(item)
            with open(PATIENTS_PATH + x, 'r') as f:
                person_dict = json.load(f)
                patient = Patient(person_dict['Name'],
                                  person_dict['Age'],
                                  person_dict['Exercises']
                                  )
                self.parent.patients.append(patient)

        print(self.parent.patients)

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
