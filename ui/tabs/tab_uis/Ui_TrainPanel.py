import json
from os import listdir
from os.path import join, isfile

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton,\
    QListWidget, QGroupBox, QSizePolicy, QListWidgetItem

from constants.variables import PATIENTS_PATH
from models.patient import Patient
from ui.custom_widgets.calibrate_wizard import CalibrateWizard
from ui.custom_styles import CustomQStyles


class Ui_TrainPanel(object):
    def setupUi(self, TrainPanel):
        self.parent = TrainPanel
        self.mainLayout = QHBoxLayout(TrainPanel)

        self.bigFont = QLabel().font()
        self.bigFont.setPointSize(13)

        self.actionsLayout = QHBoxLayout(TrainPanel)
        # self.checkRecording = QCheckBox(TrainPanel)
        self.calibrateButton = QPushButton("Calibrate", parent=TrainPanel)
        self.calibrateButton.setFont(self.bigFont)
        self.calibrateButton.setStyleSheet(CustomQStyles.buttonStyle)
        self.calibrateButton.setMinimumHeight(50)
        self.calibrateButton.setMaximumWidth(170)
        self.calibrateButton.setMinimumWidth(120)

        self.sessionButton = QPushButton("Session", parent=TrainPanel)
        self.sessionButton.setFont(self.bigFont)
        self.sessionButton.setStyleSheet(CustomQStyles.outlineButtonStyle)
        self.sessionButton.setMinimumHeight(50)
        self.sessionButton.setMaximumWidth(170)
        self.sessionButton.setMinimumWidth(120)

        self.listFiles = QListWidget(TrainPanel)
        self.listFiles.setFont(self.bigFont)
        self.label = QLabel('or select', parent=TrainPanel)
        self.subjectLayout = QVBoxLayout(TrainPanel)
        print("init")

        self.box1 = QGroupBox(parent=TrainPanel)
        self.box2 = QGroupBox(parent=TrainPanel)
        self.wizard = CalibrateWizard(parent=TrainPanel)

        self.setPatientsBox(TrainPanel)  # right panel
        self.setActionsBox(TrainPanel)  # left panel

        self.mainLayout.addWidget(self.box1, stretch=2)
        self.mainLayout.addWidget(self.box2, stretch=3)
        # self.mainLayout.setAlignment(self.box2, Qt.Alignment.AlignCenter)

    # Display progress bar, checkbox - to record new gestures or not, start train
    def setActionsBox(self, TrainPanel):
        hLayout = QVBoxLayout()
        hLayout.addWidget(self.calibrateButton)
        hLayout.addWidget(self.sessionButton)
        hLayout.setAlignment(self.calibrateButton, Qt.Alignment.AlignCenter)
        hLayout.setAlignment(self.sessionButton, Qt.Alignment.AlignCenter)
        self.box2.setLayout(hLayout)

    # Display list of subjects, or new subject
    def setPatientsBox(self, TrainPanel):

        # Button to create new patient
        self.addPatient = QPushButton('Create Patient')
        self.addPatient.setFixedSize(120, 35)
        self.addPatient.setStyleSheet(CustomQStyles.outlineButtonStyle)

        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setAlignment(QtCore.Qt.Alignment.AlignCenter)

        self.loadPatientList()

        self.listFiles.setStyleSheet(CustomQStyles.listStyle)
        self.listFiles.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.subjectLayout.addWidget(self.addPatient)
        self.subjectLayout.setAlignment(self.addPatient, Qt.Alignment.AlignCenter)
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
