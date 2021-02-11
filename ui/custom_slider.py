from PyQt6 import QtCore
from PyQt6.QtWidgets import QSlider


class Slider(QSlider):
    minimumChanged = QtCore.pyqtSignal(int)
    maximumChanged = QtCore.pyqtSignal(int)
    epochValue = QtCore.pyqtSignal(int)

    def __init__(self, orientation: QtCore.Qt.Orientations):
        super().__init__(orientation=orientation)
        self._min = 0
        self._max = 99
        self.interval = 1

    def setValue(self, value):
        index = round((value - self._min) / self.interval)
        return super(Slider, self).setValue(index)

    def value(self):
        return self.index * self.interval + self._min

    @property
    def index(self):
        return super(Slider, self).value()

    def setIndex(self, index):
        return super(Slider, self).setValue(index)

    def setMinimum(self, minimum):
        self._min = minimum
        self.minimumChanged.emit(minimum)
        self._range_adjusted()
        super(Slider, self).setMinimum(minimum)

    def setMaximum(self, maximum):
        self._max = maximum
        self.maximumChanged.emit(maximum)
        self._range_adjusted()
        super(Slider, self).setMaximum(maximum)

    def setInterval(self, value):
        # To avoid division by zero
        if not value:
            raise ValueError('Interval of zero specified')
        self.interval = value
        self._range_adjusted()

    def _range_adjusted(self):
        number_of_steps = int((self._max - self._min) / self.interval)
        super(Slider, self).setMaximum(number_of_steps)


