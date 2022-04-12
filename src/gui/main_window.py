from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QWidget

from core.model import Model
from core.results_presentation import ResultsPresentation, get_name
from .filter_selector_widget import FilterSelectorWidget
from .select_directory_widget import SelectDirectoryWidget
from .select_format_widget import SelectFormatWidget


class Window(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setGeometry(300, 300, 600, 400)
        self.model = model
        self.layout = QVBoxLayout()
        
        self.widgets = [
            SelectFormatWidget(parent=self, callback=self.model.update_selected_directory),
            SelectDirectoryWidget(parent=self, callback=self.model.update_selected_directory)
        ]
        for w in self.widgets:
            self.layout.addWidget(w)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.add_filter_selectors()
        self.combo_box = self.add_results_presentation_selector()
        self.setWindowTitle("Welcome")
        self.show()

    def add_filter_selectors(self):
        self.add_selector('File format', lambda x: self.model.update_filters('format', x))

    def add_selector(self, label, callback):
        widget = FilterSelectorWidget(label, callback, self)
        self.layout.addWidget(widget)

    def add_results_presentation_selector(self):
        combo_box = QComboBox(self)
        for pres in [p for p in ResultsPresentation]:
            combo_box.addItem(get_name(pres))
        combo_box.currentIndexChanged.connect(self.selection_change)
        combo_box.setGeometry(0, 200, 100, 25)
        self.layout.addWidget(combo_box)
        return combo_box

    def selection_change(self):
        self.model.update_results_presentation(self.combo_box.currentIndex())
