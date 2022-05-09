from core.results_presentation import ResultsPresentation


class Model:
    def __init__(self):
        self.selected_directory = None
        self.chosen_filters = {}
        self.chosen_weights = {}
        self.results = []
        self.results_presentation = ResultsPresentation.TOP_PICK
        self.template_path = None

    def update_selected_directory(self, directory):
        self.selected_directory = directory
        print(self.selected_directory)

    def update_filters(self, filter_type, value):
        self.chosen_filters[filter_type] = value
        print(self.chosen_filters)

    def update_weights(self, filter_type, value):
        self.chosen_weights[filter_type] = value
        print(self.chosen_weights)

    def update_results_presentation(self, index: int):
        self.results_presentation = [p for p in ResultsPresentation][index]
        print(self.results_presentation)


    def update_template_path(self, path):
        self.template_path = path
        print(self.template_path)

    def update_results(self, path: str, score):
        self.results.append((path, score))
