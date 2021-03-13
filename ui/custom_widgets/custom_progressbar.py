from random import randint

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QProgressBar


class ProgressBar(QProgressBar):

    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
        if self.minimum() != self.maximum():
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.onTimeout)
            self.timer.start(100)

    def start(self):
        self.timer.start(100)

    def stop(self):
        self.timer.stop()

    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)