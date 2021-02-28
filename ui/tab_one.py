import os
from os import listdir
from os.path import isfile, join

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QCheckBox, QPushButton, QListWidget, QProgressBar, QFormLayout, \
    QGroupBox, QLabel, QLineEdit, QSizePolicy, QToolTip, QListWidgetItem, QMessageBox, QSlider, QComboBox, QSplitter, \
    QSpinBox, QWidget, QWizard, QWizardPage
from PyQt6.uic.uiparser import QtCore
from PyQt6 import QtCore

from ui.Ui_TrainPanel import Ui_TrainPanel
from ui.custom_slider import Slider
from ui.dialog import DateDialog
from ui.thread_helpers.thread_helpers import progressThread, trainThread




class TrainWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_TrainPanel()
        self.ui.setupUi(self)

        self.classifyExercises = parent.classifyExercises
        self.progress_thread = progressThread(self.classifyExercises)
        self.trainThread = trainThread(self.classifyExercises)
        self.trainThread.taskFinished.connect(self.onFinished)

        self.ui.batchSizeMenu.currentIndexChanged.connect(self.onBatchSizeSelected)
        self.ui.subjectButton.clicked.connect(self.onSubjectSelected)
        self.ui.listFiles.clicked.connect(self.listClicked)
        self.ui.checkRecording.clicked.connect(self.onRecordChecked)
        self.ui.calibrateButton.clicked.connect(self.onCalibrateClicked)
        self.ui.resultButton.clicked.connect(self.onResultClicked)
        self.ui.trainButton.clicked.connect(self.onTrainClicked)
        self.ui.epochSlider.valueChanged.connect(self.updateEpochValue)

        # Test default values
        self.test_defaults()

    def onCalibrateClicked(self):
        if self.classifyExercises.subject is not None:
            self.ui.wizard.setWindowTitle("Create new ML Model for " + self.classifyExercises.subject)
            self.ui.listSelection.mOuput.clear()
            self.ui.listSelection.mOuput.addItems([e.name for e in self.classifyExercises.exercises.values()])
            self.ui.wizard.show()

        else:
            self.ui.showDialog("Message",
                            "You must either select or enter a subject name.",
                            QMessageBox.StandardButtons.Ok)
            print("Subject is none!")


    @staticmethod
    def onRecordChecked(value):
        print(value)
        # TODO: if true open RECORD exercises dialog
        if value:
            date, time, ok = DateDialog.getDateTime()

    def updateEpochValue(self, num):
        epochs = num * 50
        self.ui.epochValue.setNum(epochs)
        self.classifyExercises.epochs = epochs

    def onBatchSizeSelected(self, ind):
        self.classifyExercises.training_batch_size = int(self.ui.batchSizeMenu.currentText())

    def onResultClicked(self):
        print("open image")
        self.classifyExercises.DisplayResults()

    def onTrainClicked(self):
        print("clicked")
        if self.ui.resultButton.isEnabled:
            self.ui.resultButton.setEnabled(False)

        print("disabled button")
        if self.classifyExercises.subject is not None:
            self.trainThread.start()
            self.progress_thread.start()
            self.progress_thread.progress_update.connect(self.updateProgressBar)

        else:
            self.ui.showDialog("Message",
                            "You must either select or enter a subject name.",
                            QMessageBox.StandardButtons.Ok)
            print("Subject is none!")

    def updateProgressBar(self, maxVal):
        self.ui.progress.setValue(maxVal)
        if maxVal == 0:
            self.ui.progress.setValue(100)

    def onFinished(self):
        # Stop the progress
        self.progress_thread.disconnect()
        self.progress_thread.exit()
        self.ui.progress.setValue(100)
        self.ui.showDialog("Message",
                        "Training model finished!",
                        QMessageBox.StandardButtons.Ok)
        self.ui.resultButton.setEnabled(True)

    @QtCore.pyqtSlot(int)
    def on_pathChanged(self, num):
        num = self.classifyExercises.epochs  # append path
        print(num)

    def onSubjectSelected(self):
        print(self.ui.subjectEdit.text())
        self.ui.subject = self.ui.subjectEdit.text()
        # TODO: show alert dialog

    # TODO: train model
    def listClicked(self, index):
        item = self.ui.listFiles.currentItem()
        print(item.text())
        self.classifyExercises.subject = item.text()

    def test_defaults(self):
        """Test the GUI in its default state"""
        # self.assertEqual(self.subjectEdit.text(), "")
        # self.assertEqual(self.nrOfExercises.value(), 2)
        # self.assertEqual(self.checkRecording.isChecked(), False)
        # self.assertEqual(self.epochSlider.value(), 5)
        # self.assertEqual(self.subjectButton.text(), "New")

        # Class is in the default state even without pressing OK
        # self.assertEqual(self.form.jiggers, 36.0)
        # self.assertEqual(self.form.speedName, "&Karate Chop")

        # Push OK with the left mouse button
        # okWidget = self.form.ui.buttonBox.button(self.form.ui.buttonBox.Ok)
        # QTest.mouseClick(okWidget, Qt.LeftButton)
        # self.assertEqual(self.form.jiggers, 36.0)
        # self.assertEqual(self.form.speedName, "&Karate Chop")
        pass







