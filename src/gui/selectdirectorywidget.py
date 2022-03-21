from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog


class QStringList(object):
    pass


class SelectDirectoryWidget(QWidget):
    def __init__(self, parent=None):
        super(SelectDirectoryWidget, self).__init__(parent)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        self.btn = QPushButton("Select directory")
        self.btn.clicked.connect(self.getfile)
        self.label = QLabel('Selected directory: ')
        layout.addWidget(self.btn)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def getfile(self):
        dir_name = QFileDialog.getExistingDirectory(self, 'Select folder')
        self.label.setText('Selected directory: ' + dir_name)

