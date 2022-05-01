from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QComboBox

from core.model import Model
from core.results_presentation import ResultsPresentation, get_name
from .filter_selector_widget import FilterSelectorWidget
from gui.parameter_windows.select_animal_window import SelectAnimalWindow
from gui.parameter_windows.select_format_window import SelectFormatWindow
from .parameter_windows.select_body_window import SelectBodyWindow
from .parameter_windows.select_style_window import SelectStyleWindow
from .similar_image_widget import SimilarImageWidget
from .select_directory_widget import SelectDirectoryWidget


class Window(QMainWindow):
    def __init__(self, model: Model):
        super().__init__()
        self.setFixedSize(1000, 800)
        self.model = model
        self.layout = QVBoxLayout()
        form_widget = SelectDirectoryWidget(parent=self, callback=self.model.update_selected_directory)
        self.layout.addWidget(form_widget)
        self.add_filter_selectors()
        paste_image_widget = SimilarImageWidget(parent=self, callback=lambda x: self.model.update_filters('similar', x))
        self.layout.addWidget(paste_image_widget)
        self.combo_box = self.add_results_presentation_selector()
        self.setLayout(self.layout)
        self.setWindowTitle("Image finder")
        self.show()

    def add_filter_selectors(self):
        self.add_selector(
            'File format',
            SelectFormatWindow(lambda x: self.model.update_filters('format', x)),
            100,
            False,
        )
        self.add_selector(
            'Animal',
            SelectAnimalWindow(lambda x: self.model.update_filters('animal', x)),
            150,
            True,
            'animal',
        )
        self.add_selector(
            'Style',
            SelectStyleWindow(lambda x: self.model.update_filters('style', x)),
            200,
            True,
            'style',
        )
        self.add_selector(
            'Body parts',
            SelectBodyWindow(lambda x: self.model.update_filters('body', x)),
            250,
            True,
            'body',
        )

    def add_selector(self, label, window, ay, with_weight, weight_label=None):
        widget = FilterSelectorWidget(label, window, ay, with_weight, lambda x: self.set_weight(weight_label, x), self)
        self.layout.addWidget(widget)

    def add_results_presentation_selector(self):
        combo_box = QComboBox(self)
        for pres in [p for p in ResultsPresentation]:
            combo_box.addItem(get_name(pres))
        combo_box.currentIndexChanged.connect(self.selection_change)
        combo_box.setGeometry(10, 400, 100, 25)
        self.layout.addWidget(combo_box)
        return combo_box

    def selection_change(self):
        self.model.update_results_presentation(self.combo_box.currentIndex())

    def set_weight(self, label, value):
        try:
            weight = int(value)
        except ValueError:
            weight = None
        self.model.update_weights(label, weight)
