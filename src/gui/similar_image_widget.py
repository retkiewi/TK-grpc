from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication, QHBoxLayout


class SimilarImageWidget(QWidget):
    def __init__(self, callback, parent=None):
        super(SimilarImageWidget, self).__init__(parent)
        self.callback = callback
        self.paste_image_label = None
        self.setGeometry(0, 300, 600, 80)
        self.layout = QVBoxLayout()
        self.add_paste_image_section()
        self.setLayout(self.layout)

    def add_paste_image_section(self):
        layout = QHBoxLayout()
        button = QPushButton("Paste template image from clipboard")
        button.clicked.connect(self.paste_image)
        self.paste_image_label = QLabel('No image selected')
        layout.addWidget(button)
        layout.addWidget(self.paste_image_label)
        self.layout.addLayout(layout)

    def paste_image(self):
        clipboard = QApplication.clipboard()
        if clipboard.mimeData().hasImage():
            self.callback(clipboard.image())
            size = clipboard.image().size()
            self.paste_image_label.setText(f'Image selected. Size: {size.width()} x {size.height()}')
            self.show()
