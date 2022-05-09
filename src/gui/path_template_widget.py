from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QInputDialog
from PyQt5.QtCore import Qt


class PathWindow(QInputDialog):
    def __init__(self, callback, text_init):
        super(PathWindow, self).__init__()
        self.callback = callback
        self.setGeometry(1, 300, 300, 300)
        self.move(400, 400)
        self.setLabelText("Enter path of the template image:")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Template path')
        self.text_init = text_init
        self.setTextValue(text_init)

    def save(self):
        self.callback(self.textValue())

    def get_results(self):
        if self.exec() == QInputDialog.Accepted:
            self.save()
            self.deleteLater()
            return self.textValue()
        else:
            self.deleteLater()
            return self.text_init


class PathTemplateWidget(QWidget):
    def __init__(self, callback, parent=None):
        super(PathTemplateWidget, self).__init__(parent)
        self.text_init = ""
        self.callback = callback
        self.setGeometry(1, 350, 308, 80)
        layout = QHBoxLayout()

        self.btn = QPushButton("Select template image")
        self.btn.clicked.connect(self.open_window)

        layout.addWidget(self.btn)
        self.setLayout(layout)

    def open_window(self):
        self.text_init = PathWindow(self.callback, self.text_init).get_results()



