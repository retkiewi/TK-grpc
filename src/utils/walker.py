import os


class DirWalker:
    def __init__(self, search_path, handler, step_callback):
        self.search_path = search_path
        self.handler = handler
        self.step_callback = step_callback

    def walk(self):
        for root, _, files in os.walk(self.search_path):
            for i, filename in enumerate(files):
                filepath = "/".join([root, filename])
                self.handler(filepath)
                self.step_callback(int((i+1) * 100 / len(files)))
