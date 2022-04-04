from PyQt5.QtWidgets import QMainWindow, QVBoxLayout

from core.model import Model
from .filter_selector_widget import FilterSelectorWidget
from .select_directory_widget import SelectDirectoryWidget


class Window(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setGeometry(300, 300, 600, 400)
        self.model = model
        self.layout = QVBoxLayout()
        form_widget = SelectDirectoryWidget(parent=self, callback=self.model.update_selected_directory)
        self.layout.addWidget(form_widget)
        self.add_filter_selectors()
        self.setLayout(self.layout)
        self.setWindowTitle("Welcome")
        self.show()

    def add_filter_selectors(self):
        self.add_selector('File format', lambda x: self.model.update_filters('format', x))

    def add_selector(self, label, callback):
        widget = FilterSelectorWidget(label, callback, self)
        self.layout.addWidget(widget)
