from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from services.classify import ClassifyExercises


class RecordThread(QThread):
    taskFinished = QtCore.pyqtSignal()

    def __init__(self,
                 classify: ClassifyExercises = None,
                 exercise: str = None
                 ):
        QThread.__init__(self)
        self.classify = classify
        self.exercise = exercise
        self.result = None

    def run(self):
        # your logic here
        result = self.classify.RecordExercise(self.exercise)
        self.taskFinished.emit()
        self.result = result
