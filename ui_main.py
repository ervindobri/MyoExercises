import sys
from PyQt6.QtWidgets import QApplication
from services.myo_helpers import MyoService
from services.ui_widget import HIMOApp

if __name__ == '__main__':
    if not MyoService.check_if_process_running():
        MyoService.start_process()

    app = QApplication(sys.argv)
    ex = HIMOApp()
    currentExitCode = app.exec()
