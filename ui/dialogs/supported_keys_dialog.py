import json
import os
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QListWidget, QListWidgetItem
from constants.variables import SUPPORTED_KEYS


class AllKeysDialog(QDialog):
    def __init__(self, parent=None,):
        super(AllKeysDialog, self).__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel("Below you can see a list with all the supported keys.")
        self.list = QListWidget()
        self.listAllKeys()

        layout.addWidget(label)
        layout.setAlignment(label, Qt.Alignment.AlignTop)
        layout.addWidget(self.list)
        self.setLayout(layout)
        self.setWindowTitle('Supported Keys')

    def listAllKeys(self):
        self.list.addItems([x for x in SUPPORTED_KEYS])
    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getDialog(parent=None):
        dialog = AllKeysDialog(parent)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
