from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QMainWindow, QStatusBar, QPushButton, QHBoxLayout, QStyle
from PyQt6.QtWidgets import QWidget
from services.classify import ClassifyExercises
from constants.variables import PREDEFINED_EXERCISES
from services.myo_helpers import MyoService
from ui.dialogs.config_dialog import ConfigDialog
from ui.table_window import MainTabWidget


class HIMOApp(QMainWindow):
    EXIT_CODE_REBOOT = -12345678  # or whatever number not already taken

    def __init__(self):
        super().__init__()
        self.statusBar = QStatusBar()
        self.restartProcessButton = QPushButton('START Myo Connect')
        self.iconLabel = QLabel()
        self.informationLabel = QLabel('App current information is displayed here...')
        self.left = int(self.screen().size().width() / 4)
        self.top = int(self.screen().size().height() / 4)
        self.width = 640
        self.height = 450

        self.title = 'Myo Exercises'

        if MyoService.check_if_process_running():
            print("Myo Connect is running!")
            self.classifyExercises = ClassifyExercises(
                # subject="Ervin",
                # nr_of_samples=number_of_samples,
                epochs=300,
                # nr_of_gestures=4,
                exercises=PREDEFINED_EXERCISES,
                # batch_size=50,
                training_batch_size=16
            )
        else:
            self.classifyExercises = None
            # self.informationLabel.setText('Myo Connect is not running! Please start process.')
        self.table_widget = MainTabWidget(self)

        self.initUI()
        # self.setStyleSheet("background-color: white;")

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumHeight(self.height)
        self.setMinimumWidth(self.width)
        bar = self.menuBar()
        about = bar.addMenu("About")
        config = bar.addMenu("Configuration")

        info = QAction("App Information", self)
        about.triggered[QAction].connect(self.aboutThis)
        about.addAction(info)

        configAction = QAction("System configuration", self)
        config.triggered[QAction].connect(self.configWindow)
        config.addAction(configAction)

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setCentralWidget(self.table_widget)

        widget = QWidget()
        container = QHBoxLayout()
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
        self.iconLabel.setPixmap(icon.pixmap(QSize(16, 16)))
        self.restartProcessButton.clicked.connect(self.restartProcess)

        container.setSpacing(5)
        container.addWidget(self.iconLabel)
        container.addWidget(self.informationLabel)

        if self.classifyExercises is None:
            self.informationLabel.setText('Myo Connect is not running!Please start process.')
            container.addWidget(self.restartProcessButton)

        widget.setLayout(container)
        self.statusBar.addWidget(widget)
        self.setStatusBar(self.statusBar)
        self.show()

    def restartProcess(self):
        MyoService.start_process()

    def aboutThis(self, q):
        # TODO: open dialog with app informations
        print(q.text() + " is triggered")

    def configWindow(self):
        print("config..")
        widget = ConfigDialog(self)
        res = widget.exec()
