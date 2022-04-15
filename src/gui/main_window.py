from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox

from core.model import Model
from core.results_presentation import ResultsPresentation, get_name
from .filter_selector_widget import FilterSelectorWidget
from .select_directory_widget import SelectDirectoryWidget
from .format_parameters_window import FormatParametersWindow
from .filter_selector_widget import ParametersWindow


class Window(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setGeometry(300, 300, 600, 400)
        self.model = model
        self.layout = QVBoxLayout()
        form_widget = SelectDirectoryWidget(parent=self, callback=self.model.update_selected_directory)
        self.layout.addWidget(form_widget)
        self.add_filter_selectors()
        self.combo_box = self.add_results_presentation_selector()
        self.setLayout(self.layout)
        self.setWindowTitle("Welcome")
        self.show()

    def add_filter_selectors(self):
        self.add_selector('File format', lambda x: self.model.update_filters('format', x))

    def add_selector(self, label, callback):
        widget = FilterSelectorWidget(label, FormatParametersWindow(callback), self)
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
