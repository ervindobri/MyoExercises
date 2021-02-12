import os
from os import listdir
from os.path import isfile, join

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QListWidget, QProgressBar, QFormLayout, \
    QGroupBox, QLabel, QLineEdit, QSizePolicy, QToolTip, QListWidgetItem, QMessageBox, QSlider, QComboBox, QSplitter, \
    QSpinBox
from PyQt6.uic.uiparser import QtCore
from PyQt6 import QtCore

from ui.custom_slider import Slider
from ui.dialog import DateDialog
from ui.thread_helpers.thread_helpers import progressThread, trainThread

FULL_MODEL_PATH = os.getcwd() + '/data/results/training_data'


class TrainWidget(QHBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.epochValue = QLabel()
        self.vbox = QVBoxLayout()
        self.label_maximum = QLabel()
        self.label_minimum = QLabel()
        self.slider_hbox = QHBoxLayout()
        self.slider_vbox = QVBoxLayout()
        self.nrOfExercises = QSpinBox()
        self.batchSizeMenu = QComboBox()
        self.properties = QFormLayout()
        self.epochSlider = Slider(orientation=QtCore.Qt.Orientations.Horizontal)
        self.classifyExercises = parent.classifyExercises
        self.progress_thread = progressThread(self.classifyExercises)
        self.trainThread = trainThread(self.classifyExercises)
        self.trainThread.taskFinished.connect(self.onFinished)

        self.subjectEdit = QLineEdit()
        self.subjectButton = QPushButton('New')
        print(parent)
        self.actionsLayout = QHBoxLayout()
        self.checkRecording = QCheckBox()
        self.trainButton = QPushButton('Train Model')
        self.resultButton = QPushButton('Show result image')
        self.progress = QProgressBar()
        self.listFiles = QListWidget()
        self.label = QLabel('or select')
        self.subjectLayout = QVBoxLayout()
        self.optionsLayout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.form_layout2 = QFormLayout()
        print("init")
        self.box1 = QGroupBox(title="Subject")
        self.box2 = QGroupBox(title="Options")

        self.setSubjectPanel()  # right panel
        self.trainPanel()  # left panel

        self.addWidget(self.box1, stretch=1)
        self.addWidget(self.box2, stretch=2)

    # Display progress bar, checkbox - to record new gestures or not, start train
    def trainPanel(self):
        self.checkRecording.clicked.connect(self.onRecordChecked)
        self.checkRecording.setToolTip("Checking this will open a new window where you can calibrate the "
                                       "exercises and train a new model.")

        self.nrOfExercises.setRange(2, 6)
        self.nrOfExercises.setToolTip("Select the number of exercises you want to do. Rest exercise included.")
        self.nrOfExercises.setMaximumWidth(100)
        self.form_layout2.addRow('Number of exercises:', self.nrOfExercises)
        self.form_layout2.addRow('Record gestures:', self.checkRecording)

        self.batchSizeMenu.addItems(['2', '4', '8', '16', '32', '64', '128'])
        self.batchSizeMenu.setCurrentIndex(3)
        self.batchSizeMenu.currentIndexChanged.connect(self.onBatchSizeSelected)
        self.batchSizeMenu.setMaximumWidth(100)

        self.initSlider()

        self.properties.addRow('Batch Size', self.batchSizeMenu)

        self.resultButton.clicked.connect(self.onResultClicked)
        self.resultButton.setEnabled(False)

        self.trainButton.clicked.connect(self.onTrainClicked)
        self.actionsLayout.addWidget(self.trainButton)
        self.actionsLayout.addWidget(self.resultButton)

        self.optionsLayout.addLayout(self.form_layout2)
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
        self.epochSlider.setMaximum(12)
        self.epochSlider.setInterval(1)
        self.epochSlider.setValue(8)  # no idea why, but 8 is the middle somehow

        self.epochSlider.setTickInterval(1)
        self.epochSlider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.label_minimum.setNum(self.epochSlider.minimum().real*50)
        self.label_minimum.setAlignment(QtCore.Qt.Alignment.AlignLeft)
        self.epochSlider.minimumChanged.connect(self.label_minimum.setNum)
        self.label_maximum.setNum(self.epochSlider.maximum().real*50)

        self.label_maximum.setAlignment(QtCore.Qt.Alignment.AlignRight)

        self.epochSlider.maximumChanged.connect(self.label_maximum.setNum)
        self.slider_hbox.addWidget(self.label_minimum, QtCore.Qt.Alignment.AlignLeft)
        self.slider_hbox.addWidget(self.epochValue)
        self.slider_hbox.addWidget(self.label_maximum, QtCore.Qt.Alignment.AlignRight)

        self.slider_vbox.addWidget(self.epochSlider)
        self.slider_vbox.addLayout(self.slider_hbox)
        # self.slider_vbox.addStretch()

        self.vbox.addLayout(self.slider_vbox)
        self.epochSlider.valueChanged.connect(self.updateEpochValue)

    def updateEpochValue(self, num):
        epochs = num * 50
        self.epochValue.setNum(epochs)
        self.classifyExercises.epochs = epochs

    def onBatchSizeSelected(self, ind):
        self.classifyExercises.training_batch_size = int(self.batchSizeMenu.currentText())

    @staticmethod
    def onRecordChecked(value):
        print(value)
        # TODO: if true open RECORD exercises dialog
        if value:
            date, time, ok = DateDialog.getDateTime()

    def onResultClicked(self):
        print("open image")
        self.classifyExercises.DisplayResults()

    def onTrainClicked(self):
        if self.resultButton.isEnabled:
            self.resultButton.setEnabled(False)

        if self.classifyExercises.subject is not None:
            self.trainThread.start()
            self.progress_thread.start()
            self.progress_thread.progress_update.connect(self.updateProgressBar)

        else:
            self.showDialog("Message",
                            "You must either select or enter a subject name.",
                            QMessageBox.StandardButtons.Ok)
            print("Subject is none!")

    def onFinished(self):
        # Stop the progress
        self.progress_thread.disconnect()
        self.progress_thread.exit()
        self.progress.setValue(100)
        self.showDialog("Message",
                        "Training model finished!",
                        QMessageBox.StandardButtons.Ok)
        self.resultButton.setEnabled(True)

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

    def updateProgressBar(self, maxVal):
        self.progress.setValue(maxVal)
        if maxVal == 0:
            self.progress.setValue(100)

    @QtCore.pyqtSlot(int)
    def on_pathChanged(self, num):
        num = self.classifyExercises.epochs  # append path
        print(num)

    # Display list of subjects, or new subject
    def setSubjectPanel(self):
        self.form_layout.addRow('Name:', self.subjectEdit)
        self.subjectButton.clicked.connect(self.onSubjectSelected)
        self.form_layout.addWidget(self.subjectButton)

        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setAlignment(QtCore.Qt.Alignment.AlignCenter)

        files = [f for f in listdir(FULL_MODEL_PATH) if isfile(join(FULL_MODEL_PATH, f))]
        for x, ind in zip(files, range(0, len(files))):
            item = QListWidgetItem(x.split('.')[0])
            item.setTextAlignment(Qt.Alignment.AlignHCenter)
            self.listFiles.addItem(item)

        self.listFiles.clicked.connect(self.listClicked)

        self.subjectLayout.addLayout(self.form_layout)
        self.subjectLayout.addWidget(self.label)
        self.subjectLayout.addWidget(self.listFiles)

        self.box1.setLayout(self.subjectLayout)

    def onSubjectSelected(self):
        print(self.subjectEdit.text())
        self.classifyExercises.subject = self.subjectEdit.text()
        # TODO: show alert dialog

    # TODO: train model
    def listClicked(self, index):
        item = self.listFiles.currentItem()
        print(item.text())
        self.classifyExercises.subject = item.text()

