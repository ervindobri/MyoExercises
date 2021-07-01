import myo
from PyQt6.QtCore import QTimer, QSize, Qt, QTime
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QWidget, QPushButton, QHBoxLayout, QComboBox, QTimeEdit

from constants.variables import PREDEFINED_REPS, \
    IMAGES_PATH
from services.connection import Connection
from ui.custom_styles import CustomQStyles
from ui.thread_helpers.session_thread import SessionThread


class SessionDialog(QDialog):
    def __init__(self, parent=None,
                 patient=None,
                 classifyExercises=None
                 ):
        super(SessionDialog, self).__init__(parent)
        layout = QHBoxLayout(self)
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Session")
        self.setLayout(layout)
        self.setParent(parent)
        self.patient = patient
        self.classifyExercises = classifyExercises
        optionsContainer = QWidget()
        optionsContainer.setStyleSheet("background-color: #ededed; border-radius: 7px;")
        options = QVBoxLayout()
        optionsContainer.setLayout(options)

        repsLabel = QLabel('Repetitions')
        pauseLabel = QLabel('Pause between exercises (sec)')
        bigFont = repsLabel.font()
        bigFont.setPointSize(13)

        repsLabel.setFont(bigFont)
        pauseLabel.setFont(bigFont)

        self.reps = QComboBox()
        self.reps.addItems(PREDEFINED_REPS)
        self.reps.setStyleSheet(CustomQStyles.comboStyle)
        self.reps.setFixedHeight(35)

        self.reps.currentTextChanged.connect(self.onRepsChanged)

        self.pause = QLabel()
        self.pause.setStyleSheet(CustomQStyles.comboStyle)
        self.pause.setFixedHeight(35)
        self.pause.setText('0')

        options.addWidget(repsLabel)
        options.addWidget(self.reps)
        options.addWidget(pauseLabel)

        options.addWidget(self.pause)

        options.setAlignment(self.reps, Qt.Alignment.AlignTop)

        self.startButton = QPushButton('Start')
        self.startButton.setStyleSheet(CustomQStyles.buttonStyle)
        self.startButton.setFont(bigFont)
        self.startButton.clicked.connect(self.startSession)
        self.startButton.setFixedSize(120, 35)
        options.addWidget(self.startButton)
        options.setAlignment(self.startButton, Qt.Alignment.AlignHCenter)

        # Session panel
        session = QVBoxLayout()
        self.timerLabel = QTimeEdit()
        self.timerLabel.setDisplayFormat('hh:mm:ss')
        biggerFont = bigFont
        biggerFont.setPointSize(20)
        self.timerLabel.setFont(biggerFont)
        self.timerLabel.setStyleSheet(CustomQStyles.timerStyle)
        self.timerLabel.setFixedHeight(50)

        self.exerciseWidget = QVBoxLayout()
        self.exerciseLabel = QLabel('Exercise name')
        self.exerciseLabel.setFont(bigFont)
        self.exerciseImage = QLabel()
        self.exerciseImage.setPixmap(QPixmap(IMAGES_PATH + 'frame.png'))
        self.exerciseWidget.addWidget(self.exerciseLabel)
        self.exerciseWidget.setAlignment(self.exerciseLabel, Qt.Alignment.AlignCenter)
        self.exerciseWidget.addWidget(self.exerciseImage)
        self.exerciseWidget.setAlignment(self.exerciseImage, Qt.Alignment.AlignCenter)

        session.addWidget(self.timerLabel)
        session.addLayout(self.exerciseWidget)
        session.setAlignment(self.timerLabel, Qt.Alignment.AlignHCenter)
        session.setAlignment(self.exerciseWidget, Qt.Alignment.AlignCenter)
        layout.addWidget(optionsContainer, stretch=1)
        layout.addLayout(session, stretch=2)
        self.curr_time = QTime(00, 00, 00)

        self.timer = QTimer()
        self.timer.timeout.connect(self.time)

        self.sessionThread = SessionThread(self.classifyExercises)
        self.sessionThread.exerciseResult.connect(self.onResultExercise)

    def time(self):
        self.curr_time = self.curr_time.addSecs(1)
        self.timerLabel.setTime(self.curr_time)

    def onRepsChanged(self, text):
        # update pauses
        self.pause.setText(str(int(text) * 2))
        if Connection.active_connection():
            self.classifyExercises.SaveSessionData(self.reps.currentText(), self.pause.text())
        else:
            print("Error! Probably no internet")

    def onResultExercise(self, exercise):
        self.exerciseImage.setPixmap(QPixmap(IMAGES_PATH + exercise.code + '.png'))
        self.exerciseLabel.setText(exercise.name)

    def startSession(self):
        if self.startButton.text() == 'Start':
            print("Starting timer and session!")

            self.timer.start(1000)
            self.startButton.setText('Stop')
            self.sessionThread.classification.hub = myo.Hub()
            self.sessionThread.start()
        else:
            self.timer.stop()
            self.curr_time = QTime(00, 00, 00)
            self.timerLabel.setTime(self.curr_time)
            self.startButton.setText('Start')
            self.sessionThread.terminate()

        # self.sessionThread.start()
