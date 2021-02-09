import os
from os import listdir
from os.path import isfile, join

import PyQt6.QtWidgets as qt
from PyQt6.QtCore import QSize, Qt
from PyQt6.uic.properties import QtGui
from PyQt6.uic.uiparser import QtCore
from PyQt6 import QtCore, QtTest

from ui.dialog import DateDialog

MODEL_PATH = os.getcwd() + '/data/results/trained_model'


class TrainWidget(qt.QHBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.actions_layout = qt.QVBoxLayout()
        self.check_record = qt.QCheckBox()
        self.train_button = qt.QPushButton('Start Training')
        self.progress = qt.QProgressBar()
        self.list_widget = qt.QListWidget()
        self.label = qt.QLabel('or select')
        self.subject_layout = qt.QVBoxLayout()
        self.options_layout = qt.QVBoxLayout()
        self.form_layout = qt.QFormLayout()
        self.form_layout2 = qt.QFormLayout()
        print("init")
        self.box1 = qt.QGroupBox(title="Subject")
        self.box2 = qt.QGroupBox(title="Options")

        self.set_subject_panel()  # right panel
        self.train_panel()  # left panel

        self.addWidget(self.box2, stretch=2)
        self.addWidget(self.box1, stretch=1)

    # Display progress bar, checkbox - to record new gestures or not, start train
    def train_panel(self):
        # TODO: if record is checked, dialog appears with the instructions
        self.check_record.clicked.connect(self.on_record_checked)
        self.form_layout2.addRow('Record gestures:', self.check_record)
        self.train_button.clicked.connect(self.on_train_clicked)
        self.actions_layout.addWidget(self.train_button)

        self.options_layout.addLayout(self.form_layout2)
        self.options_layout.addLayout(self.actions_layout)
        self.progress.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.options_layout.addWidget(self.progress)
        # self.options_layout.addWidget(self.label)
        # self.options_layout.addWidget(self.list_widget)

        self.box2.setLayout(self.options_layout)

    def on_record_checked(self, value):
        print(value)
        # TODO: if true open RECORD exercises dialog
        if value:
            date, time, ok = DateDialog.getDateTime()

    def on_train_clicked(self):
        for i in range(0, 101):
            self.progress.setValue(i)
            QtTest.QTest.qWait(10)

    # Display list of subjects, or new subject
    def set_subject_panel(self):
        self.form_layout.addRow('Name:', qt.QLineEdit())
        self.form_layout.addWidget(qt.QPushButton('New'))

        self.label.setSizePolicy(qt.QSizePolicy.Policy.Expanding, qt.QSizePolicy.Policy.Expanding)
        self.label.setAlignment(QtCore.Qt.Alignment.AlignCenter)

        files = [f for f in listdir(MODEL_PATH) if isfile(join(MODEL_PATH, f))]
        for x, ind in zip(files, range(0, len(files))):
            self.list_widget.insertItem(ind, x)

        self.list_widget.clicked.connect(self.list_clicked)

        self.subject_layout.addLayout(self.form_layout)
        self.subject_layout.addWidget(self.label)
        self.subject_layout.addWidget(self.list_widget)

        self.box1.setLayout(self.subject_layout)

    # TODO: train model
    def list_clicked(self, index):
        item = self.list_widget.currentItem()
        print(item.text())
