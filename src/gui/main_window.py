from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox

from core.model import Model
from core.results_presentation import ResultsPresentation, get_name
from .filter_selector_widget import FilterSelectorWidget
from .similar_image_widget import SimilarImageWidget
from .select_directory_widget import SelectDirectoryWidget


class Window(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setGeometry(300, 300, 600, 400)
        self.model = model
        self.layout = QVBoxLayout()
        select_directory_widget = SelectDirectoryWidget(parent=self, callback=self.model.update_selected_directory)
        self.layout.addWidget(select_directory_widget)
        self.add_filter_selectors()
        paste_image_widget = SimilarImageWidget(parent=self, callback=lambda x: self.model.update_filters('similar', x))
        self.layout.addWidget(paste_image_widget)
        self.combo_box = self.add_results_presentation_selector()
        self.setLayout(self.layout)
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
        combo_box.setGeometry(10, 200, 100, 25)
        self.layout.addWidget(combo_box)
        return combo_box

    def selection_change(self):
        self.model.update_results_presentation(self.combo_box.currentIndex())
