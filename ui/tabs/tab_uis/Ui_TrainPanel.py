import os
from os import listdir
from os.path import join, isfile

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QComboBox, QFormLayout, QLineEdit, QPushButton, \
    QCheckBox, QProgressBar, QListWidget, QGroupBox, QMessageBox, QSizePolicy, QListWidgetItem, QSlider, QWizard, QWizardPage

from ui.custom_slider import Slider
from ui.custom_widgets.two_list_selection import TwoListSelection

FULL_MODEL_PATH = os.getcwd() + '/data/results/training_data'
# FULL_MODEL_PATH = '/data/results/training_data'


class Ui_TrainPanel(object):

    def setupUi(self, TrainPanel):
        self.mainLayout = QHBoxLayout(TrainPanel)
        self.epochValue = QLabel(parent=TrainPanel)
        self.vbox = QVBoxLayout(TrainPanel)
        self.label_maximum = QLabel(parent=TrainPanel)
        self.label_minimum = QLabel(parent=TrainPanel)
        self.slider_hbox = QHBoxLayout(TrainPanel)
        self.slider_vbox = QVBoxLayout(TrainPanel)
        self.nrOfExercises = QSpinBox(TrainPanel)
        self.batchSizeMenu = QComboBox(TrainPanel)
        self.properties = QFormLayout(TrainPanel)
        self.epochSlider = Slider(orientation=QtCore.Qt.Orientations.Horizontal, parent=TrainPanel)

        self.subjectEdit = QLineEdit(TrainPanel)
        self.subjectButton = QPushButton('New', parent=TrainPanel)
        # print(parent)
        self.actionsLayout = QHBoxLayout(TrainPanel)
        self.checkRecording = QCheckBox(TrainPanel)
        self.calibrateButton = QPushButton("Calibrate new model", parent=TrainPanel)
        self.calibrateButton.setMinimumHeight(50)
        self.calibrateButton.setMaximumWidth(120)

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
        self.box2 = QGroupBox(title="Options", parent=TrainPanel)
        self.wizard = QWizard(parent=TrainPanel)

        self.setSubjectPanel(TrainPanel)  # right panel
        self.trainPanel(TrainPanel)  # left panel
        self.createWizard(TrainPanel)

        self.mainLayout.addWidget(self.box1, stretch=1)
        self.mainLayout.addWidget(self.box2, stretch=2)

        # self.retranslateUi(TrainPanel)

    # Display progress bar, checkbox - to record new gestures or not, start train
    def trainPanel(self, TrainPanel):
        self.checkRecording.setToolTip("Checking this will open a new window where you can calibrate the "
                                       "exercises and train a new model.")

        self.nrOfExercises.setRange(2, 6)
        self.nrOfExercises.setToolTip("Select the number of exercises you want to do. Rest exercise included.")
        self.nrOfExercises.setMaximumWidth(100)

        self.form_layout2.addRow('Number of exercises:', self.nrOfExercises)
        self.form_layout2.addRow('Record gestures:', self.checkRecording)
        hLayout = QHBoxLayout()
        hLayout.addLayout(self.form_layout2)
        hLayout.addWidget(self.calibrateButton)

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

        # self.wizard.setPixmap(QWizard.WizardPixmap.WatermarkPixmap,
        #                       QPixmap('Watermark.png'))
        # self.wizard.setPixmap(QWizard.WizardPixmap.LogoPixmap,
        #                       QPixmap('Logo.png'))
        # self.wizard.setPixmap(QWizard.WizardPixmap.BannerPixmap,
        #                       QPixmap('Banner.png'))

        # CREATE PAGE 1, LINE EDIT, TITLES
        page1 = QWizardPage()
        page1.setTitle('Select the exercises you wish to do later')
        page1.setSubTitle('Below are listed all the available and selected exercises by you.')
        self.listSelection = TwoListSelection()
        # listSelection.addAvailableItems(["item-{}".format(i) for i in range(5)])
        hLayout1 = QHBoxLayout(page1)
        hLayout1.addWidget(self.listSelection)

        # CREATE PAGE 2, LABEL, TITLES
        page2 = QWizardPage()
        page2.setFinalPage(True)
        page2.setTitle('Page 2 is better!')
        page2.setSubTitle('Lies!')
        label = QLabel()
        hLayout2 = QHBoxLayout(page2)
        hLayout2.addWidget(label)
        self.listWidget = QListWidget()
        itemsTextList = [str(self.listSelection.mInput.item(i).text()) for i in range(self.listSelection.mInput.count())]
        print(itemsTextList)
        self.listWidget.addItems(itemsTextList)
        hLayout2.addWidget(self.listWidget)

        nxt = self.wizard.button(QWizard.WizardButton.NextButton)

        func = lambda: label.setText(page1.field('myField'))
        nxt.clicked.connect(self.onWizardNextButton)
        self.wizard.addPage(page1)
        self.wizard.addPage(page2)

        print()

    # Send list to next page
    def onWizardNextButton(self):
        itemsTextList = [str(self.listSelection.mInput.item(i).text()) for i in range(self.listSelection.mInput.count())]
        print(itemsTextList)
        self.listWidget.clear()
        self.listWidget.addItems(itemsTextList)

    # Display list of subjects, or new subject
    def setSubjectPanel(self, TrainPanel):
        self.form_layout.addRow('Name:', self.subjectEdit)
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
