from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6 import QtCore

from constants.variables import PREDEFINED_EXERCISES
from models.patient import Patient
from ui.dialogs.session_dialog import SessionDialog
from ui.custom_widgets.show_message import CustomMessage
from ui.dialogs.add_patient import CreatePatientDialog
from ui.tabs.tab_uis.Ui_TrainPanel import Ui_TrainPanel


class TrainWidget(QWidget):
    def __init__(self, parent=None):
        super(TrainWidget, self).__init__(parent)
        self.ui = Ui_TrainPanel()
        self.subject = ""
        self.classifyExercises = None
        if parent is not None:
            self.classifyExercises = parent.classifyExercises
            self.infoLabel = parent.infoLabel

        self.patients = []
        self.selectedPatient = Patient("", "", {})
        self.ui.setupUi(self)
        self.connections()

    def connections(self):
        self.ui.addPatient.clicked.connect(self.addPatientDialog)  # to train panel
        self.ui.listFiles.clicked.connect(self.listClicked)
        self.ui.calibrateButton.clicked.connect(self.onCalibrateClicked)
        self.ui.sessionButton.clicked.connect(self.onSessionClicked)

    def addPatientDialog(self):
        dialog = CreatePatientDialog(
            self.classifyExercises,
            self.selectedPatient,
            self.infoLabel)
        ret = dialog.exec()
        # If accept, save patient data and refresh list
        if ret == 1:
            self.classifyExercises.SavePatientData()
            self.ui.loadPatientList()

    def onSessionClicked(self):
        dialog = SessionDialog(self, self.selectedPatient, self.classifyExercises)
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
                CustomMessage.showDialog("Message",
                                         "You must either select or enter a subject name.",
                                         QMessageBox.StandardButtons.Ok)
                print("Subject is none!")

    @QtCore.pyqtSlot(int)
    def on_pathChanged(self, num):
        num = self.classifyExercises.epochs  # append path
        print(num)

    def listClicked(self, index):
        item = self.ui.listFiles.currentItem()
        if self.classifyExercises is not None:
            name, age = item.text().split('-')
            self.classifyExercises.load_patient_data(name, age)
            self.selectedPatient = next(x for x in self.patients if x.name == name and x.age == age)
            print("Selected patient:", self.selectedPatient.name)
            self.infoLabel.setText("Subject name set to " + name + ", age " + age)
