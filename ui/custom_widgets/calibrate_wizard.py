import functools
import os
from os import listdir
from os.path import isfile, join

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWizard, QHBoxLayout, QWizardPage, QLabel, QPushButton, QVBoxLayout, QListWidgetItem, \
    QProgressBar, QMessageBox

from ui.custom_styles import CustomQStyles
from ui.custom_widgets.show_message import CustomMessage
from ui.custom_widgets.two_list_selection import TwoListSelection
from ui.tabs.tab_uis.Ui_KeysPanel import FULL_MODEL_PATH
from ui.thread_helpers.record_thread import RecordThread
from ui.thread_helpers.train_thread import TrainThread


class CalibrateWizard(QWizard):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWizardStyle(QWizard.WizardStyle.ModernStyle)

        # CREATE PAGE 1, LINE EDIT, TITLES
        buttons_layout = [QWizard.WizardButton.NextButton]
        self.page1 = QWizardPage()
        self.page1.setTitle('Select the exercises you wish to do later')
        self.page1.setSubTitle('Below are listed all the available and selected exercises by you.')
        self.listSelection = TwoListSelection()
        # listSelection.addAvailableItems(["item-{}".format(i) for i in range(5)])
        hLayout1 = QHBoxLayout(self.page1)
        hLayout1.addWidget(self.listSelection)

        # CREATE PAGE 2, LABEL, TITLES
        self.page2 = QWizardPage()
        self.page2.setFinalPage(True)
        self.setButtonLayout(buttons_layout)
        self.page2.setTitle('Calibrate every exercise')
        self.page2.setSubTitle('Do every exercise once, record after pressing button.')
        self.contentLayout = QVBoxLayout(self.page2)
        self.hLayout2 = QHBoxLayout()

        # Create progress bar, buttons
        self.actionsLayout = QHBoxLayout()
        self.finishButton = QPushButton('Ready')
        self.finishButton.setStyleSheet(CustomQStyles.buttonStyle)
        self.finishButton.setFixedSize(120, 35)

        self.progress = QProgressBar()
        self.progress.setRange(0, 1)
        self.actionsLayout.addWidget(self.progress)
        self.actionsLayout.setAlignment(self.progress, Qt.Alignment.AlignBottom)
        self.actionsLayout.addWidget(self.finishButton)
        self.actionsLayout.setAlignment(self.finishButton, Qt.Alignment.AlignBottom)

        self.contentLayout.addLayout(self.hLayout2)
        self.contentLayout.addLayout(self.actionsLayout)
        self.actionsLayout.setContentsMargins(15, 35, 15, 0)
        itemsTextList = [str(self.listSelection.mInput.item(i).text()) for i in
                         range(self.listSelection.mInput.count())]
        print("items:", itemsTextList)

        self.button(QWizard.WizardButton.NextButton).clicked.connect(self.onWizardNextButton)
        self.finishButton.clicked.connect(self.onWizardFinishButton)

        self.addPage(self.page1)
        self.addPage(self.page2)

        # Recording data
        self.buttons = []
        self.images = []
        self.labels = []
        self.exerciseLayouts = []
        self.recordReady = []
        self.recordThread = RecordThread(self.parent.classifyExercises)

        # Training recorded data
        self.trained = False
        self.trainThread = TrainThread(self.parent.classifyExercises)
        self.trainThread.taskFinished.connect(self.onTrainFinished)

    # Send list to next page
    def onWizardNextButton(self):
        self.setPage(1, self.page1)
        self.trained = False
        itemsTextList = [str(self.listSelection.mInput.item(i).text())
                         for i in range(self.listSelection.mInput.count())]
        # Update list
        if self.parent.classifyExercises is not None:
            self.parent.classifyExercises.UpdateExerciseList(itemsTextList)

        # Set elements on UI
        self.setMinimumWidth(len(itemsTextList) * 200)
        self.deleteItemsOfLayout(self.hLayout2)
        self.images.clear()
        self.labels.clear()
        self.buttons.clear()
        self.recordReady.clear()
        for x, i in zip(itemsTextList, range(len(itemsTextList))):
            self.exerciseLayouts.append(QVBoxLayout())
            self.buttons.append(QPushButton('Record'))
            self.recordReady.append(False)
            image = QLabel()
            image.setPixmap(QPixmap(os.getcwd() + "/resources/images/" + itemsTextList[i] + ".png"))
            self.labels.append(QLabel(itemsTextList[i]))
            self.images.append(image)
            self.buttons[i].setFixedSize(100, 35)
            self.buttons[i].clicked.connect(functools.partial(self.onRecordExerciseButtonClicked, x, i))
            self.buttons[i].setStyleSheet(CustomQStyles.outlineButtonStyle)
            self.exerciseLayouts[i].addWidget(self.labels[i])
            self.exerciseLayouts[i].addWidget(self.images[i])
            self.exerciseLayouts[i].addWidget(self.buttons[i])
            self.exerciseLayouts[i].setAlignment(self.labels[i], Qt.Alignment.AlignCenter)
            self.exerciseLayouts[i].setAlignment(self.images[i], Qt.Alignment.AlignCenter)
            self.exerciseLayouts[i].setAlignment(self.buttons[i], Qt.Alignment.AlignCenter)
            self.hLayout2.addLayout(self.exerciseLayouts[i])

    def onRecordExerciseButtonClicked(self, exercise, ind):
        print("Recording - ", exercise)
        if self.parent.classifyExercises is not None:
            self.recordThread.exercise = exercise
            self.recordThread.taskFinished.connect(functools.partial(self.recordFinished,
                                                                     exercise,
                                                                     ind),
                                                   Qt.ConnectionType.SingleShotConnection)
            self.recordThread.start()
            self.recordReady[ind] = False
            self.buttons[ind].setStyleSheet(CustomQStyles.recordButtonStyle)
            self.images[ind].setPixmap(QPixmap(os.getcwd() + "/resources/images/" + exercise + ".png"))

    def recordFinished(self, exercise, index):
        imagePath = os.getcwd() + "/resources/images/" + exercise + ".png"
        if self.recordThread.result == 0:
            imagePath = os.getcwd() + "/resources/images/" + exercise + "-fail.png"
        elif self.recordThread.result == 1:
            imagePath = os.getcwd() + "/resources/images/" + exercise + "-success.png"
            self.recordReady[index] = True
        else:
            print("None.")
        self.images[index].setPixmap(QPixmap(imagePath))
        self.buttons[index].setStyleSheet(CustomQStyles.outlineButtonStyle)
        print(self.recordReady)

    def onWizardFinishButton(self):
        if all(x == True for x in self.recordReady):
            print("All recorded!")
            if not self.trained:
                if self.parent.classifyExercises is not None:
                    self.progress.setRange(0, 0)  # indefinite progress bar
                    self.parent.classifyExercises.SaveProcessedData()
                    self.parent.classifyExercises.SavePatientData()
                    self.parent.ui.loadPatientList()
                    self.trainThread.start()

            else:
                self.close()

        else:
            print("Not all recorded!")

    def onTrainFinished(self):
        self.progress.setRange(0, 1)
        self.progress.setValue(1)
        self.trained = True
        CustomMessage.showDialog("Message",
                                 "Training model finished!",
                                 QMessageBox.StandardButtons.Ok)
        self.finishButton.setText('Finish')

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
