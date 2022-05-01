from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QCheckBox

from gui.parameter_windows.parameters_window import ParametersWindow


class SelectFormatWindow(ParametersWindow):

    def __init__(self, callback, parent=None):
        self.formats = [
            "jpeg", "jpeg2000", "gif", "bmp", "png",
            "webp", "ico", "img", "xcf", "cgm", "svg",
            "blend", "xaml", "pdf"
        ]
        self.check_boxes = []
        super(SelectFormatWindow, self).__init__(callback, parent)
        self.setWindowTitle('Choose format')

    def add_widgets(self):
        for i, format_ext in enumerate(self.formats):
            check_box = QCheckBox(format_ext, self)
            x, y = self.get_position(i)
            check_box.setGeometry(100*x + 10, 20*y, 100, 20)
            self.check_boxes.append(check_box)
            self.layout.addWidget(check_box)

    def get_position(self, i):
        row = int(i / 4)
        col = i % 4
        return col, row

    def set_values(self):
        self.chosen_values = [cb.text() for cb in self.check_boxes if cb.isChecked()]

    def get_size(self):
        return QSize(400, 120)
