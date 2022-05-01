from PyQt5.QtCore import QRect, QSize
from PyQt5.QtWidgets import QMainWindow, QPushButton, QGridLayout


class ParametersWindow(QMainWindow):
    def __init__(self, callback, parent=None):
        super(ParametersWindow, self).__init__(parent)
        self.setFixedSize(self.get_size())
        self.callback = callback
        self.chosen_values = None
        self.layout = QGridLayout()
        self.add_widgets()
        self.btn = QPushButton("Save", self)
        self.btn.clicked.connect(self.save)
        self.btn.setGeometry(self.get_save_geometry())
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    # to be used by inheriting classes for adding widgets to current layout
    def add_widgets(self):
        pass

    # to be used by inheriting classes for setting chosen_values attribute
    def set_values(self):
        pass

    # to be used by inheriting classes for determining size of the window
    def get_size(self) -> QSize:
        pass

    def get_save_geometry(self):
        return QRect(self.size().width()/2 - 35, self.size().height() - 35, 70, 30)

    def save(self):
        self.set_values()
        self.callback(self.chosen_values)
        self.close()
