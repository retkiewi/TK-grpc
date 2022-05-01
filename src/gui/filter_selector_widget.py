from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QLineEdit, QCheckBox


class FilterSelectorWidget(QWidget):
    def __init__(self, label, parameters_window, ay, with_weight, weight_callback, parent=None):
        super(FilterSelectorWidget, self).__init__(parent)
        self.parameters_window = parameters_window
        self.setGeometry(0, ay, 500, 80)
        layout = QHBoxLayout()
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)
        self.label = QLabel(label)
        self.label.setFixedSize(100, 20)
        layout.addWidget(self.label)
        self.btn = QPushButton("Select parameters")
        self.btn.clicked.connect(self.open_window)
        layout.addWidget(self.btn)
        layout.addStretch()
        if with_weight:
            self.weight_label = QLabel('Minimal weight:')
            layout.addWidget(self.weight_label)
            self.weight_input = QLineEdit()
            reg_ex = QRegExp("^[1-9][0-9]?$|^100$")
            input_validator = QRegExpValidator(reg_ex, self.weight_input)
            self.weight_input.setValidator(input_validator)
            self.weight_input.textChanged.connect(weight_callback)
            self.weight_input.setFixedSize(40, 20)
            layout.addWidget(self.weight_input)
        self.setLayout(layout)

    def open_window(self):
        self.parameters_window.show()
