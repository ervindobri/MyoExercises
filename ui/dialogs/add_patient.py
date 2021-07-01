from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QWidget

from ui.custom_styles import CustomQStyles


class CreatePatientDialog(QDialog):
    def __init__(self,
                 classification,
                 patient,
                 infoLabel,
                 parent=None):
        super(CreatePatientDialog, self).__init__(parent)
        self.setWindowTitle('Create new patient')
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setMinimumWidth(200)

        self.patient = patient
        self.classifyExercises = classification
        self.infoLabel = infoLabel

        self.subjectEdit = QLineEdit()
        self.subjectEdit.setFixedHeight(30)
        self.subjectEdit.setText('Jozsika')
        self.subjectEdit.setStyleSheet(CustomQStyles.lineEditStyle)

        self.ageEdit = QLineEdit()
        self.ageEdit.setFixedHeight(30)
        self.ageEdit.setValidator(QIntValidator())
        self.ageEdit.setText('5')
        self.ageEdit.setStyleSheet(CustomQStyles.lineEditStyle)

        self.subjectButton = QPushButton('Add patient')
        self.subjectButton.setFixedHeight(30)
        self.subjectButton.setStyleSheet(CustomQStyles.outlineButtonStyle)
        self.subjectButton.clicked.connect(self.onSubjectSelected)
        self.subjectButton.setContentsMargins(5, 15, 5, 5)
        formContainer = QWidget()
        self.formLayout = QFormLayout()
        self.formLayout.addRow('Name', self.subjectEdit)
        self.formLayout.addRow('Age', self.ageEdit)
        self.formLayout.addWidget(self.subjectButton)
        self.formLayout.setFormAlignment(Qt.Alignment.AlignCenter)
        formContainer.setLayout(self.formLayout)
        formContainer.setStyleSheet("background-color: white; border-radius: 7px;")
        layout.addWidget(formContainer)

    def onSubjectSelected(self):
        if self.classifyExercises is not None \
                and "" != self.subjectEdit.text() \
                and "" != self.ageEdit.text():
            self.subject = self.subjectEdit.text()
            self.classifyExercises.subject = self.subject
            self.classifyExercises.age = self.ageEdit.text()
            self.classifyExercises.exercises = []
            self.infoLabel.setText("Subject name set to " + self.subject + ", age " + self.classifyExercises.age)
            self.accept()
