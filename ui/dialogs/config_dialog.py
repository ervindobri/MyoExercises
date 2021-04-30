from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QFormLayout, QDialog, QSlider, QPushButton, \
    QProgressBar, QMessageBox

from ui.custom_slider import Slider
from ui.custom_widgets.show_message import CustomMessage
from ui.thread_helpers.train_thread import TrainThread


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.classifyExercises = parent.classifyExercises
        self.setFixedSize(500, 400)
        self.setWindowTitle("Model Configurations")

        self.epochValue = QLabel()
        self.vbox = QVBoxLayout()
        self.label_maximum = QLabel()
        self.label_minimum = QLabel()
        self.slider_hbox = QHBoxLayout()
        self.slider_vbox = QVBoxLayout()
        self.batchSizeMenu = QComboBox()
        self.properties = QFormLayout()
        self.epochSlider = Slider(orientation=Qt.Orientations.Horizontal)

        self.trainButton = QPushButton('Train Model')
        self.resultButton = QPushButton('Show result image')
        self.progress = QProgressBar()

        self.batchSizeMenu.addItems(['2', '4', '8', '16', '32', '64', '128'])
        self.batchSizeMenu.setCurrentIndex(3)
        self.batchSizeMenu.setMaximumWidth(100)

        self.initSlider()

        self.properties.addRow('Batch Size', self.batchSizeMenu)

        self.resultButton.setEnabled(False)
        self.actionsLayout = QHBoxLayout()

        self.actionsLayout.addWidget(self.trainButton)
        self.actionsLayout.addWidget(self.resultButton)

        self.optionsLayout = QVBoxLayout()
        self.optionsLayout.addWidget(QLabel('Model properties'))
        self.optionsLayout.addLayout(self.vbox)
        self.optionsLayout.addLayout(self.properties)
        self.optionsLayout.addLayout(self.actionsLayout)
        self.progress.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.optionsLayout.addWidget(self.progress)
        # self.options_layout.addWidget(self.label)
        # self.options_layout.addWidget(self.list_widget)

        self.setLayout(self.optionsLayout)

        self.trainThread = TrainThread(self.classifyExercises)
        self.connections()
        print("init config")

    def initSlider(self):
        self.epochValue.setAlignment(QtCore.Qt.Alignment.AlignHCenter)

        self.epochSlider.setMinimum(2)
        self.epochSlider.setMaximum(10)
        self.epochSlider.setTickInterval(1)
        # self.epochSlider.setInterval(1)
        # self.epochSlider.setValue(8)  # no idea why, but 8 is the middle somehow
        self.epochSlider.setSliderPosition(6)
        self.epochSlider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.label_minimum.setNum(self.epochSlider.minimum().real * 50)
        self.label_minimum.setAlignment(QtCore.Qt.Alignment.AlignLeft)
        self.label_maximum.setNum(self.epochSlider.maximum().real * 50)

        self.label_maximum.setAlignment(QtCore.Qt.Alignment.AlignRight)

        self.epochSlider.minimumChanged.connect(self.label_minimum.setNum)
        self.epochSlider.maximumChanged.connect(self.label_maximum.setNum)

        self.slider_hbox.addWidget(self.label_minimum, QtCore.Qt.Alignment.AlignLeft)
        self.slider_hbox.addWidget(self.epochValue)
        self.slider_hbox.addWidget(self.label_maximum, QtCore.Qt.Alignment.AlignRight)

        self.slider_vbox.addWidget(self.epochSlider)
        self.slider_vbox.addLayout(self.slider_hbox)
        # self.slider_vbox.addStretch()

        self.vbox.addLayout(self.slider_vbox)

    def connections(self):
        self.batchSizeMenu.currentIndexChanged.connect(self.onBatchSizeSelected)
        self.resultButton.clicked.connect(self.onResultClicked)
        self.trainButton.clicked.connect(self.onTrainClicked)
        self.epochSlider.valueChanged.connect(self.updateEpochValue)
        self.trainThread.taskFinished.connect(self.onFinished)


    def updateEpochValue(self, num):
        print(num)
        epochs = num * 50
        self.epochValue.setNum(epochs)
        self.classifyExercises.epochs = epochs

    def onBatchSizeSelected(self, ind):
        self.classifyExercises.training_batch_size = int(self.batchSizeMenu.currentText())

    def onResultClicked(self):
        print("open image")
        self.classifyExercises.DisplayResults()

    def onTrainClicked(self):
        if self.classifyExercises.subject is not None:
            if self.classifyExercises.DataAvailable():
                if self.resultButton.isEnabled:
                    self.resultButton.setEnabled(False)

                self.trainThread.start()
                self.progress.setRange(0, 0)
            else:
                CustomMessage.showDialog("Message",
                                         "Calibrate for patient to obtain data.",
                                         QMessageBox.StandardButtons.Ok)

        else:
            CustomMessage.showDialog("Message",
                                     "You must either select or enter a subject name.",
                                     QMessageBox.StandardButtons.Ok)
            print("Subject is none!")

    def onFinished(self):
        # Stop the progress
        self.progress.setRange(0, 1)
        self.progress.setValue(1)
        CustomMessage.showDialog("Message",
                                 "Training model finished!",
                                 QMessageBox.StandardButtons.Ok)
        self.resultButton.setEnabled(True)
