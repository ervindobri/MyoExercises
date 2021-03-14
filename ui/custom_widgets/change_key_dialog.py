from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QDateTimeEdit, QDialogButtonBox, QLabel, QWidget

from constants.variables import KEYS
from ui.custom_widgets.key_monitor import KeyMonitor


class ChangeKeyDialog(QDialog):
    def __init__(self, parent=None,
                 buttons=None,
                 exercises=None,
                 index: int = None,
                 ):
        super(ChangeKeyDialog, self).__init__(parent)
        widget = QWidget(self)
        layout = QVBoxLayout(self)
        label = QLabel("Press a key to swap this exercise's key")
        layout.addWidget(label)
        self.buttons = buttons
        self.exercises = exercises
        self.index = index
        widget.setLayout(layout)
        self.window().setMinimumSize(210, 150)

        self.monitor = KeyMonitor()
        self.monitor.start_monitoring()

        self.timer = QTimer()
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start()

    def onTimeout(self):
        if self.monitor.currentKey in list(KEYS.values()):
            for name, key in KEYS.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                if key == self.monitor.currentKey:
                    old_exercise = None
                    old_button = None
                    for exercise, button in zip(self.exercises, self.buttons):
                        if exercise.assigned_key == (name, key) and button.text() == name:
                            old_exercise = exercise
                            old_button = button

                    # Set new keys and labels
                    if old_exercise is not None and old_button is not None:
                        self.exercises[self.index].assigned_key, old_exercise.assigned_key = old_exercise.assigned_key, self.exercises[
                            self.index].assigned_key
                        old_label = old_button.text()
                        old_button.setText(self.buttons[self.index].text())
                        self.buttons[self.index].setText(old_label)
                        print("old key:", old_exercise.assigned_key)
                        print("new key:", self.exercises[self.index].assigned_key)
                        self.close()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getSwapper(parent=None):
        dialog = ChangeKeyDialog(parent)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted
