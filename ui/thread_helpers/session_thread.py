import myo
from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from services.classify import ClassifyExercises
from models.exercise import Exercise


class SessionThread(QThread):
    exerciseResult = QtCore.pyqtSignal(Exercise)

    def __init__(self, classification: ClassifyExercises, parent=None):
        QThread.__init__(self, parent)
        # self.queue = queue
        # self.result_queue = result_queue
        self.classification = classification

    def run(self):
        self.classification.LoadModel()
        if self.classification.hub.running:
            print("Hub is running!")
        while True:
            val = self.classification.Predict()
            self.exerciseResult.emit(self.classification.exercises[val])
            self.classification.PressKey(val)
