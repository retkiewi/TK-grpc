from PyQt5.QtWidgets import QMainWindow

from src.gui.selectdirectorywidget import SelectDirectoryWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setCentralWidget(SelectDirectoryWidget(self))
        self.setWindowTitle("Welcome")
        self.show()
