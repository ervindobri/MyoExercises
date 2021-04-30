import myo
from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from services.classify import ClassifyExercises


class SessionThread(QThread):
    exerciseResult = QtCore.pyqtSignal(str)

    def __init__(self, classification : ClassifyExercises, parent=None):
        QThread.__init__(self, parent)
        # self.queue = queue
        # self.result_queue = result_queue
        self.classification = classification

    def run(self):
        self.classification.LoadModel()
        if self.classification.hub.running:
            print("Hub is running!")
        while True:
            val, res = self.classification.Predict()
            self.exerciseResult.emit(res)
            self.classification.PressKey(val)

