from PyQt5.QtWidgets import QLineEdit, QCheckBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from .filter_selector_widget import ParametersWindow
from format.available_formats import available_formats


class FormatParametersWindow(ParametersWindow):
    def __init__(self, callback, parent=None):
        super(FormatParametersWindow, self).__init__(callback, parent)

    # to be used by inheriting classes for adding widgets to current layout
    def add_widgets(self):
        for available_format in available_formats:
            weight_input = QLineEdit(self)
            weight_input.move(170, self.padding)
            weight_input.resize(40, 40)
            reg_ex = QRegExp("^[1-9][0-9]?$|^100$")
            input_validator = QRegExpValidator(reg_ex, weight_input)
            weight_input.setValidator(input_validator)
            self.layout.addChildWidget(weight_input)

            param_check_box = QCheckBox(available_format, parent=self)
            param_check_box.move(20, self.padding)
            self.layout.addChildWidget(param_check_box)
            self.padding += 40

            self.params.append((param_check_box, weight_input))

