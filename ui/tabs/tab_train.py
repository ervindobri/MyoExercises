from PyQt6.QtWidgets import QMessageBox, QWidget, QHBoxLayout
from PyQt6 import QtCore

from constants.variables import PREDEFINED_EXERCISES
from models.patient import Patient
from ui.custom_widgets.session_dialog import SessionDialog
from ui.tabs.tab_uis.Ui_TrainPanel import Ui_TrainPanel
from ui.custom_widgets.dialog import DateDialog
from ui.thread_helpers.thread_helpers import progressThread, trainThread


class TrainWidget(QWidget):
    def __init__(self, parent=None):
        super(TrainWidget, self).__init__(parent)
        self.ui = Ui_TrainPanel()
        self.subject = ""

        self.classifyExercises = None
        self.progress_thread = progressThread()
        self.trainThread = trainThread()
        if parent is not None:
            self.classifyExercises = parent.classifyExercises
            self.infoLabel = parent.infoLabel
            self.progress_thread = progressThread(self.classifyExercises)
            self.trainThread = trainThread(self.classifyExercises)

        self.patients = []
        self.selectedPatient = Patient("","",[])
        self.ui.setupUi(self)
        self.connections()

    def connections(self):
        self.trainThread.taskFinished.connect(self.onFinished)
        self.ui.batchSizeMenu.currentIndexChanged.connect(self.onBatchSizeSelected)
        self.ui.subjectButton.clicked.connect(self.onSubjectSelected)
        self.ui.listFiles.clicked.connect(self.listClicked)
        # self.ui.checkRecording.clicked.connect(self.onRecordChecked)
        self.ui.calibrateButton.clicked.connect(self.onCalibrateClicked)
        self.ui.sessionButton.clicked.connect(self.onSessionClicked)
        self.ui.resultButton.clicked.connect(self.onResultClicked)
        self.ui.trainButton.clicked.connect(self.onTrainClicked)
        self.ui.epochSlider.valueChanged.connect(self.updateEpochValue)

    def onSessionClicked(self):
        dialog = SessionDialog(self, self.selectedPatient)
        dialog.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        dialog.exec()

    def onCalibrateClicked(self):
        if self.classifyExercises is not None:
            if self.classifyExercises.subject is not None:
                # self.ui.createWizard(self)
                self.ui.wizard.setWindowTitle("Calibrating " + self.classifyExercises.subject)
                self.ui.recordReady = []
                self.ui.wizard.listSelection.mInput.clear()
                self.ui.wizard.listSelection.mOuput.clear()
                self.ui.wizard.listSelection.mOuput.addItems([e.name for e in PREDEFINED_EXERCISES])
                self.ui.wizard.restart()
                self.ui.wizard.show()

            else:
                self.ui.showDialog("Message",
                                   "You must either select or enter a subject name.",
                                   QMessageBox.StandardButtons.Ok)
                print("Subject is none!")

    def updateEpochValue(self, num):
        print(num)
        epochs = num * 50
        self.ui.epochValue.setNum(epochs)
        self.classifyExercises.epochs = epochs

    def onBatchSizeSelected(self, ind):
        self.classifyExercises.training_batch_size = int(self.ui.batchSizeMenu.currentText())
        self.infoLabel.setText("Batch size set to " + self.ui.batchSizeMenu.currentText() + ".")

    def onResultClicked(self):
        print("open image")
        self.classifyExercises.DisplayResults()

    def onTrainClicked(self):
        if self.classifyExercises.subject is not None:
            if self.classifyExercises.DataAvailable():
                if self.ui.resultButton.isEnabled:
                    self.ui.resultButton.setEnabled(False)
                self.infoLabel.setText("Training in progress.")

                self.trainThread.start()
                self.progress_thread.start()
                self.progress_thread.progress_update.connect(self.updateProgressBar)
            else:
                self.ui.showDialog("Message",
                                   "Calibrate for patient to obtain data.",
                                   QMessageBox.StandardButtons.Ok)

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
        self.infoLabel.setText("Training model successful.")

    @QtCore.pyqtSlot(int)
    def on_pathChanged(self, num):
        num = self.classifyExercises.epochs  # append path
        print(num)

    def onSubjectSelected(self):
        if self.classifyExercises is not None \
                and "" != self.ui.subjectEdit.text() \
                and "" != self.ui.ageEdit.text():
            self.subject = self.ui.subjectEdit.text()
            self.classifyExercises.subject = self.subject
            self.classifyExercises.age = self.ui.ageEdit.text()
            self.infoLabel.setText("Subject name set to " + self.subject + ", age " + self.classifyExercises.age)

    # TODO: train model
    def listClicked(self, index):
        item = self.ui.listFiles.currentItem()
        if self.classifyExercises is not None:
            name, age = item.text().split('-')
            self.classifyExercises.subject = name
            self.classifyExercises.age = age
            self.selectedPatient = next(x for x in self.patients if x.name == name and x.age == age)
            print("Selected patient:", self.selectedPatient.name)
            self.infoLabel.setText("Subject name set to " + name + ", age " + age)
