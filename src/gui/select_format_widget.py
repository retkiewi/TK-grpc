from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QDialogButtonBox, QDialog
from .select_format_window import FormatChooseWindow

class SelectFormatWidget(QWidget):
    def __init__(self, callback, parent=None):
        super(SelectFormatWidget, self).__init__(parent)

        self.formats = []
        layout = QVBoxLayout()
        self.btn = QPushButton("Select formats")
        self.fWindow = FormatChooseWindow(self)
        self.btn.clicked.connect(self.openFormatWindow)
        self.label = QLabel('Selected formats: ')
        layout.addWidget(self.btn)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def openFormatWindow(self):
        self.fWindow.exec()
        if self.fWindow.accepted:
            self.labeltext = 'Selected formats: '
            for item in self.formats:
                self.labeltext += item + " "
            self.label.setText(self.labeltext)