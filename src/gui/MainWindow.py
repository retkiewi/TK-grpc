from PyQt5.QtWidgets import QMainWindow

from src.gui.selectdirectorywidget import SelectDirectoryWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = SelectDirectoryWidget(self)
        self.setCentralWidget(self.form_widget)
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle("Welcome")
        self.show()
