from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QCheckBox

from gui.parameter_windows.parameters_window import ParametersWindow


class SelectBodyWindow(ParametersWindow):

    def __init__(self, callback, parent=None):
        self.parts = [
            'hands', 'face'
        ]
        self.check_boxes = []
        super(SelectBodyWindow, self).__init__(callback, parent)
        self.setWindowTitle('Choose body part')

    def add_widgets(self):
        for i, body_part in enumerate(self.parts):
            check_box = QCheckBox(body_part, self)
            check_box.setGeometry(20, 20*i, 100, 20)
            self.check_boxes.append(check_box)
            self.layout.addWidget(check_box)

    def set_values(self):
        self.chosen_values = [cb.text() for cb in self.check_boxes if cb.isChecked()]

    def get_size(self):
        return QSize(100, 80)
