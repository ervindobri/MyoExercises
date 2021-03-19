from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6 import QtCore

from ui.tabs.tab_uis.Ui_TrainPanel import Ui_TrainPanel
from ui.custom_widgets.dialog import DateDialog
from ui.thread_helpers.thread_helpers import progressThread, trainThread


class TrainWidget(QWidget):
    def __init__(self, parent=None):
        super(TrainWidget, self).__init__(parent)
        self.ui = Ui_TrainPanel()
        self.ui.setupUi(self)
        self.subject = ""

        self.classifyExercises = None
        self.progress_thread = progressThread()
        self.trainThread = trainThread()
        if parent is not None:
            self.classifyExercises = parent.classifyExercises
            self.infoLabel = parent.infoLabel
            self.progress_thread = progressThread(self.classifyExercises)
            self.trainThread = trainThread(self.classifyExercises)

        self.connections()

    def connections(self):
        self.trainThread.taskFinished.connect(self.onFinished)
        self.ui.batchSizeMenu.currentIndexChanged.connect(self.onBatchSizeSelected)
        self.ui.subjectButton.clicked.connect(self.onSubjectSelected)
        self.ui.listFiles.clicked.connect(self.listClicked)
        self.ui.checkRecording.clicked.connect(self.onRecordChecked)
        self.ui.calibrateButton.clicked.connect(self.onCalibrateClicked)
        self.ui.resultButton.clicked.connect(self.onResultClicked)
        self.ui.trainButton.clicked.connect(self.onTrainClicked)
        self.ui.epochSlider.valueChanged.connect(self.updateEpochValue)

    def onCalibrateClicked(self):
        if self.classifyExercises is not None:
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
        print(num)
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
        self.infoLabel.setText("Starting training...")
        if self.ui.resultButton.isEnabled:
            self.ui.resultButton.setEnabled(False)

        print("disabled button")
        if self.classifyExercises is not None:
            if self.classifyExercises.subject is not None:
                self.infoLabel.setText("Training in progress.")

                self.trainThread.start()
                self.progress_thread.start()
                self.progress_thread.progress_update.connect(self.updateProgressBar)

            else:
                self.ui.showDialog("Message",
                                   "You must either select or enter a subject name.",
                                   QMessageBox.StandardButtons.Ok)
                print("Subject is none!")

    def updateProgressBar(self, maxVal):
        self.ui.progress.setValue(0) if maxVal % 2 == 0 else self.ui.progress.setValue(100)
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
        self.subject = self.ui.subjectEdit.text()
        self.ui.showDialog("Information",
                           "Subject name set to" + self.subject,
                           QMessageBox.StandardButtons.Ok)

    # TODO: train model
    def listClicked(self, index):
        item = self.ui.listFiles.currentItem()
        print(item.text())
        if self.classifyExercises is not None:
            self.classifyExercises.subject = item.text()
