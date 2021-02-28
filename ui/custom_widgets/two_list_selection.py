from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QListWidget, QLabel


class TwoListSelection(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TwoListSelection, self).__init__(parent)
        self.setup_layout()

    def setup_layout(self):
        lay = QtWidgets.QHBoxLayout(self)

        selectedLayout = QVBoxLayout()
        self.mInput = QListWidget()
        selectedLayout.addWidget(QLabel("Selected:"))
        selectedLayout.addWidget(self.mInput)

        availableLayout = QVBoxLayout()
        self.mOuput = QListWidget()
        availableLayout.addWidget(QLabel("Available"))
        availableLayout.addWidget(self.mOuput)

        self.mButtonToSelected = QtWidgets.QPushButton(">>")
        self.mBtnMoveToAvailable = QtWidgets.QPushButton(">")
        self.mBtnMoveToSelected = QtWidgets.QPushButton("<")
        self.mButtonToAvailable = QtWidgets.QPushButton("<<")

        vlay = QtWidgets.QVBoxLayout()
        vlay.addStretch()
        vlay.addWidget(self.mButtonToSelected)
        vlay.addWidget(self.mBtnMoveToAvailable)
        vlay.addWidget(self.mBtnMoveToSelected)
        vlay.addWidget(self.mButtonToAvailable)
        vlay.addStretch()

        self.mBtnUp = QtWidgets.QPushButton("Up")
        self.mBtnDown = QtWidgets.QPushButton("Down")

        vlay2 = QtWidgets.QVBoxLayout()
        vlay2.addStretch()
        vlay2.addWidget(self.mBtnUp)
        vlay2.addWidget(self.mBtnDown)
        vlay2.addStretch()

        lay.addLayout(selectedLayout)
        lay.addLayout(vlay)
        lay.addLayout(availableLayout)
        lay.addLayout(vlay2)

        self.update_buttons_status()
        self.connections()

    @QtCore.pyqtSlot()
    def update_buttons_status(self):
        self.mBtnUp.setDisabled(not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == 0)
        self.mBtnDown.setDisabled(
            not bool(self.mOuput.selectedItems()) or self.mOuput.currentRow() == (self.mOuput.count() - 1))
        self.mBtnMoveToAvailable.setDisabled(not bool(self.mInput.selectedItems()) or self.mOuput.currentRow() == 0)
        self.mBtnMoveToSelected.setDisabled(not bool(self.mOuput.selectedItems()))

    def connections(self):
        self.mInput.itemSelectionChanged.connect(self.update_buttons_status)
        self.mOuput.itemSelectionChanged.connect(self.update_buttons_status)
        self.mBtnMoveToAvailable.clicked.connect(self.on_mBtnMoveToAvailable_clicked)
        self.mBtnMoveToSelected.clicked.connect(self.on_mBtnMoveToSelected_clicked)
        self.mButtonToAvailable.clicked.connect(self.on_mButtonToAvailable_clicked)
        self.mButtonToSelected.clicked.connect(self.on_mButtonToSelected_clicked)
        self.mBtnUp.clicked.connect(self.on_mBtnUp_clicked)
        self.mBtnDown.clicked.connect(self.on_mBtnDown_clicked)

    @QtCore.pyqtSlot()
    def on_mBtnMoveToAvailable_clicked(self):
        self.mOuput.addItem(self.mInput.takeItem(self.mInput.currentRow()))

    @QtCore.pyqtSlot()
    def on_mBtnMoveToSelected_clicked(self):
        self.mInput.addItem(self.mOuput.takeItem(self.mOuput.currentRow()))

    @QtCore.pyqtSlot()
    def on_mButtonToAvailable_clicked(self):
        while self.mOuput.count() > 0:
            self.mInput.addItem(self.mOuput.takeItem(0))

    @QtCore.pyqtSlot()
    def on_mButtonToSelected_clicked(self):
        while self.mInput.count() > 0:
            self.mOuput.addItem(self.mInput.takeItem(0))

    @QtCore.pyqtSlot()
    def on_mBtnUp_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row - 1, currentItem)
        self.mOuput.setCurrentRow(row - 1)

    @QtCore.pyqtSlot()
    def on_mBtnDown_clicked(self):
        row = self.mOuput.currentRow()
        currentItem = self.mOuput.takeItem(row)
        self.mOuput.insertItem(row + 1, currentItem)
        self.mOuput.setCurrentRow(row + 1)

    def addAvailableItems(self, items):
        self.mInput.addItems(items)

    def get_left_elements(self):
        r = []
        for i in range(self.mInput.count()):
            it = self.mInput.item(i)
            r.append(it.text())
        return r

    def get_right_elements(self):
        r = []
        for i in range(self.mOuput.count()):
            it = self.mOuput.item(i)
            r.append(it.text())
        return r
