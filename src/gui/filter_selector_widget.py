from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout, QMainWindow


class FilterSelectorWidget(QWidget):
    def __init__(self, label, callback, parent=None):
        super(FilterSelectorWidget, self).__init__(parent)
        self.parameters_window = None
        self.callback = callback
        self.setGeometry(0, 100, 300, 100)
        layout = QHBoxLayout()
        self.label = QLabel(label)
        self.btn = QPushButton("Select parameters")
        self.btn.clicked.connect(self.open_window)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def open_window(self):
        self.parameters_window = ParametersWindow(parent=self, callback=self.callback)
        self.parameters_window.show()


class ParametersWindow(QMainWindow):
    def __init__(self, callback, parent=None):
        super(ParametersWindow, self).__init__(parent)
        self.callback = callback
        self.chosen_values = None
        self.layout = QHBoxLayout()
        self.add_widgets()
        self.btn = QPushButton("Save", self)
        self.btn.clicked.connect(self.save)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)

    # to be used by inheriting classes for adding widgets to current layout
    def add_widgets(self):
        pass

    # to be used by inheriting classes for setting chosen_values attribute
    def set_values(self):
        pass

    def save(self):
        self.callback(self.chosen_values)
        self.close()
