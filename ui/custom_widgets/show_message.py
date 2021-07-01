from PyQt6.QtWidgets import QMessageBox


class CustomMessage:
    @staticmethod
    def showDialog(title, message, buttons: QMessageBox.StandardButtons):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setText(message)
        msgBox.setStandardButtons(buttons)
        msgBox.exec()

    @staticmethod
    def showAlert(title, message, buttons: QMessageBox.StandardButtons):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setText(message)
        msgBox.setStandardButtons(buttons)
        msgBox.exec()
