from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QRadioButton

from gui.parameter_windows.parameters_window import ParametersWindow


class SelectStyleWindow(ParametersWindow):

    def __init__(self, callback, parent=None):
        self.types = [
            'photo', 'clip art', 'line drawing', 'GIF'
        ]
        self.radio_buttons = []
        super(SelectStyleWindow, self).__init__(callback, parent)
        self.setWindowTitle('Choose style')

    def add_widgets(self):
        for i, format_ext in enumerate(self.types):
            radio_button = QRadioButton(format_ext, self)
            radio_button.setGeometry(20, 20*i, 100, 20)
            self.radio_buttons.append(radio_button)
            self.layout.addWidget(radio_button)

    def set_values(self):
        self.chosen_values = [cb.text() for cb in self.radio_buttons if cb.isChecked()]

    def get_size(self):
        return QSize(120, 120)
