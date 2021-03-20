import PyQt6.QtWidgets as Widgets


class ConfigDialog(Widgets.QDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        layout = Widgets.QVBoxLayout()
        self.setLayout(layout)
        self.setFixedSize(500, 400)
        print("init config")