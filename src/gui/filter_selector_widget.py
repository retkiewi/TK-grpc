from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QMessageBox, QLabel, QHBoxLayout


class FilterSelectorWidget(QWidget):
    def __init__(self, label, parameters_window, parent=None):
        super(FilterSelectorWidget, self).__init__(parent)
        self.parameters_window = parameters_window
        self.setGeometry(0, 100, 300, 100)
        layout = QHBoxLayout()
        self.label = QLabel(label)
        self.btn = QPushButton("Select parameters")
        self.btn.clicked.connect(self.open_window)
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def open_window(self):
        self.parameters_window.update_params()
        self.parameters_window.show()


class ParametersWindow(QMainWindow):
    def __init__(self, callback, parent=None):
        super(ParametersWindow, self).__init__(parent)
        self.callback = callback
        self.chosen_values = {}
        self.padding = 0
        self.params = []
        self.setGeometry(100, 100, 500, 500)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.add_widgets()

        self.btn = QPushButton("Save", self)
        self.btn.clicked.connect(self.save)
        self.btn.move(20, self.padding)
        self.layout.addChildWidget(self.btn)

    # to be used by inheriting classes for adding widgets to current layout
    def add_widgets(self):
        pass

    def save(self):
        self.chosen_values = {}
        for param_check_box, weight_input in self.params:
            if param_check_box.isChecked():
                if weight_input.text() == "":
                    msg = QMessageBox()
                    msg.setText(f"Input cannot be empty for {param_check_box.text()}")
                    msg.setWindowTitle("Error")
                    msg.exec_()
                    weight_input.setFocus()
                    return
                self.chosen_values[param_check_box.text()] = int(weight_input.text())
        self.callback(self.chosen_values)
        self.close()

    def update_params(self):
        for param_check_box, weight_input in self.params:
            if param_check_box.text() in self.chosen_values:
                param_check_box.setChecked(True)
                weight_input.setText(str(self.chosen_values[param_check_box.text()]))
            else:
                param_check_box.setChecked(False)
                weight_input.clear()
