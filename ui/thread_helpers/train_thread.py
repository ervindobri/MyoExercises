from PyQt6 import QtCore
from PyQt6.QtCore import QThread
from services.classify import ClassifyExercises


class TrainThread(QThread):
    taskFinished = QtCore.pyqtSignal()

    def __init__(self, classify: ClassifyExercises = None):
        QThread.__init__(self)
        self.classify = classify

    # def __del__(self):
    #     self.wait()

    def run(self):
        # your logic here
        self.classify.TrainEMG()
        self.taskFinished.emit()

