class Model:
    def __init__(self):
        self.selected_directory = None
        self.chosen_filters = {}
        self.results_presentation = None

    def update_selected_directory(self, directory):
        self.selected_directory = directory
        print(self.selected_directory)

    def update_filters(self, filter_type, value):
        self.chosen_filters[filter_type] = value
        print(self.chosen_filters)
