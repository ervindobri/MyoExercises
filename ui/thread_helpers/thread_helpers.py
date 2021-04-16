import time

from PyQt6 import QtCore
from PyQt6.QtCore import QThread

from classify import ClassifyExercises


class trainThread(QThread):
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


class progressThread(QThread):
    progress_update = QtCore.pyqtSignal(int)  # or pyqtSignal(int)

    def __init__(self, classify: ClassifyExercises = None):
        QThread.__init__(self)
        self.classify = classify

    # def __del__(self):
    #     self.wait()

    def run(self):
        # TODO:  can't get progress as global variable
        counter = 0
        while counter < self.classify.epochs + 1:
            # print(counter/self.classify.epochs)
            self.progress_update.emit(int((counter / self.classify.epochs) * 100))
            # Tell the thread to sleep for 1 second and let other things run
            time.sleep(.05)
            counter += 1
