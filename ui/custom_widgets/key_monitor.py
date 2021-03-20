import sys
from typing import Any

from PyQt6 import QtCore, QtWidgets

from pynput.keyboard import Key, Listener, KeyCode


class KeyMonitor(QtCore.QObject):
    keyPressed = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.currentKey = None
        self.released = False
        print("Monitor init!")

    def on_press(self, key):
        self.released = False
        self.currentKey = key
        self.keyPressed.emit(key)

    def on_release(self, key):
        self.currentKey = None
        self.released = True

    def stop_monitoring(self):
        self.listener.stop()
        self.deleteLater()

    def start_monitoring(self):
        self.listener.start()
