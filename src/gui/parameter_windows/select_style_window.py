from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QCheckBox

from gui.parameter_windows.parameters_window import ParametersWindow


class SelectStyleWindow(ParametersWindow):

    def __init__(self, callback, parent=None):
        self.types = [
            'photo', 'clip art', 'line drawing'
        ]
        self.check_boxes = []
        super(SelectStyleWindow, self).__init__(callback, parent)
        self.setWindowTitle('Choose style')

    def add_widgets(self):
        for i, image_type in enumerate(self.types):
            check_box = QCheckBox(image_type, self)
            check_box.setGeometry(20, 20*i, 100, 20)
            self.check_boxes.append(check_box)
            self.layout.addWidget(check_box)

    def set_values(self):
        self.chosen_values = [cb.text() for cb in self.check_boxes if cb.isChecked()]

    def get_size(self):
        return QSize(120, 120)
