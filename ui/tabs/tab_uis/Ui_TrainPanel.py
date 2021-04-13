import functools
import os
from os import listdir
from os.path import join, isfile

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QFormLayout, QLineEdit, QPushButton, \
    QCheckBox, QProgressBar, QListWidget, QGroupBox, QMessageBox, QSizePolicy, QListWidgetItem, QSlider, QWizard, \
    QWizardPage

from ui.custom_slider import Slider
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
        self.subjectEdit.setPlaceholderText("Jozsika")
        self.subjectEdit.setStyleSheet(CustomQStyles.lineEditStyle)

        self.ageEdit = QLineEdit(TrainPanel)
        self.ageEdit.setFixedHeight(30)
        self.ageEdit.setPlaceholderText("5")
        self.ageEdit.setValidator(QIntValidator())
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

        self.box1 = QGroupBox(title="Subject", parent=TrainPanel)
        self.box2 = QGroupBox(parent=TrainPanel)
        self.wizard = QWizard(parent=TrainPanel)

        self.setSubjectPanel(TrainPanel)  # right panel
        self.trainPanel(TrainPanel)  # left panel
        self.createWizard(TrainPanel)
        self.buttons = []
        self.images = []
        self.labels = []
        self.exerciseLayouts = []
        self.recordReady = []

        self.mainLayout.addWidget(self.box1, stretch=1)
        self.mainLayout.addWidget(self.box2, stretch=2)

        self.recordThread = RecordThread(self.parent.classifyExercises)
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

    def createWizard(self, TrainPanel):
        self.wizard.setWizardStyle(QWizard.WizardStyle.ModernStyle)
        # CREATE PAGE 1, LINE EDIT, TITLES
        buttons_layout = [QWizard.WizardButton.NextButton, QWizard.WizardButton.FinishButton]
        page1 = QWizardPage()
        page1.setTitle('Select the exercises you wish to do later')
        page1.setSubTitle('Below are listed all the available and selected exercises by you.')
        self.listSelection = TwoListSelection()
        # listSelection.addAvailableItems(["item-{}".format(i) for i in range(5)])
        hLayout1 = QHBoxLayout(page1)
        hLayout1.addWidget(self.listSelection)

        # CREATE PAGE 2, LABEL, TITLES
        self.page2 = QWizardPage()
        self.page2.setFinalPage(True)
        self.wizard.setButtonLayout(buttons_layout)
        self.page2.setTitle('Calibrate every exercise')
        self.page2.setSubTitle('Do every exercise once, record after pressing button.')
        self.hLayout2 = QHBoxLayout(self.page2)
        itemsTextList = [str(self.listSelection.mInput.item(i).text()) for i in
                         range(self.listSelection.mInput.count())]
        print("items:", itemsTextList)

        nxt = self.wizard.button(QWizard.WizardButton.NextButton)
        nxt.clicked.connect(self.onWizardNextButton)
        self.wizard.button(QWizard.WizardButton.FinishButton).clicked.connect(self.onWizardFinishButton)
        self.wizard.addPage(page1)
        self.wizard.addPage(self.page2)

    def onWizardFinishButton(self):
        if all(x == True for x in self.recordReady):
            print("All recorded!")
            if self.parent.classifyExercises is not None:
                self.parent.classifyExercises.SaveProcessedData()
        else:
            print("Not all recorded!")

    # Send list to next page
    def onWizardNextButton(self):

        itemsTextList = [str(self.listSelection.mInput.item(i).text())
                         for i in range(self.listSelection.mInput.count())]
        # Update list
        if self.parent.classifyExercises is not None:
            self.parent.classifyExercises.UpdateExerciseList(itemsTextList)

        # Set elements on UI
        self.wizard.setMinimumWidth(len(itemsTextList) * 200)
        self.deleteItemsOfLayout(self.hLayout2)
        self.images.clear()
        self.labels.clear()
        self.buttons.clear()
        for x, i in zip(itemsTextList, range(len(itemsTextList))):
            self.exerciseLayouts.append(QVBoxLayout())
            self.buttons.append(QPushButton('Record'))
            self.recordReady.append(False)
            image = QLabel()
            image.setPixmap(QPixmap(os.getcwd() + "/resources/images/" + itemsTextList[i] + ".png"))
            self.labels.append(QLabel(itemsTextList[i]))
            self.images.append(image)
            self.buttons[i].setFixedSize(100, 35)
            self.buttons[i].clicked.connect(functools.partial(self.onRecordExerciseButtonClicked, x, i))
            self.buttons[i].setStyleSheet(CustomQStyles.buttonStyle)
            self.exerciseLayouts[i].addWidget(self.labels[i])
            self.exerciseLayouts[i].addWidget(self.images[i])
            self.exerciseLayouts[i].addWidget(self.buttons[i])
            self.exerciseLayouts[i].setAlignment(self.labels[i], Qt.Alignment.AlignCenter)
            self.exerciseLayouts[i].setAlignment(self.images[i], Qt.Alignment.AlignCenter)
            self.exerciseLayouts[i].setAlignment(self.buttons[i], Qt.Alignment.AlignCenter)
            self.hLayout2.addLayout(self.exerciseLayouts[i])

    def onRecordExerciseButtonClicked(self, exercise, ind):
        print("Recording - ", exercise)
        if self.parent.classifyExercises is not None:
            self.recordThread.exercise = exercise
            self.recordThread.taskFinished.connect(functools.partial(self.recordFinished, exercise, ind),
                                                   Qt.ConnectionType.SingleShotConnection)
            self.recordThread.start()
            self.recordReady[ind] = False
            self.buttons[ind].setStyleSheet(CustomQStyles.recordButtonStyle)
            self.images[ind].setPixmap(QPixmap(os.getcwd() + "/resources/images/" + exercise + ".png"))

    def recordFinished(self, exercise, index):
        print(index)
        self.images[index].setPixmap(QPixmap(os.getcwd() + "/resources/images/" + exercise + "-success.png"))
        self.buttons[index].setStyleSheet(CustomQStyles.buttonStyle)
        self.recordReady[index] = True

    # Display list of subjects, or new subject
    def setSubjectPanel(self, TrainPanel):
        self.form_layout.addRow('Name', self.subjectEdit)
        self.form_layout.addRow('Age', self.ageEdit)
        self.form_layout.addWidget(self.subjectButton)

        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setAlignment(QtCore.Qt.Alignment.AlignCenter)

        files = [f for f in listdir(FULL_MODEL_PATH) if isfile(join(FULL_MODEL_PATH, f))]
        for x, ind in zip(files, range(0, len(files))):
            item = QListWidgetItem(x.split('.')[0])
            item.setTextAlignment(Qt.Alignment.AlignHCenter)
            self.listFiles.addItem(item)

        self.subjectLayout.addLayout(self.form_layout)
        self.subjectLayout.addWidget(self.label)
        self.subjectLayout.addWidget(self.listFiles)

        self.box1.setLayout(self.subjectLayout)

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
