from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QCheckBox

from gui.parameter_windows.parameters_window import ParametersWindow


class SelectAnimalWindow(ParametersWindow):

    def __init__(self, callback, parent=None):
        self.animals = [
            'tiger', 'elephant', 'panda'
        ]
        self.check_boxes = []
        super(SelectAnimalWindow, self).__init__(callback, parent)
        self.setWindowTitle('Choose animal')

    def add_widgets(self):
        for i, format_ext in enumerate(self.animals):
            check_box = QCheckBox(format_ext, self)
            check_box.setGeometry(20, 20*i, 100, 20)
            self.check_boxes.append(check_box)
            self.layout.addWidget(check_box)

    def set_values(self):
        self.chosen_values = [cb.text() for cb in self.check_boxes if cb.isChecked()]

    def get_size(self):
        return QSize(100, 100)
