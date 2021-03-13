from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget

from ui.tabs.tab_uis.Ui_KeysPanel import Ui_KeysPanel


class KeysWidget(QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)

    def __init__(self, parent=None):
        super(KeysWidget, self).__init__(parent)
        self.classifyExercises = None
        if parent is not None:
            self.classifyExercises = parent.classifyExercises

        self.ui = Ui_KeysPanel()
        self.ui.setupUi(self)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Up:
            print("Up")
            self.deleteLater()
        elif event.key() == QtCore.Qt.Key.Key_Enter:
            self.proceed()
        event.accept()
