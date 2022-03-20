import os


class DirWalker:
    def __init__(self, search_path, handler):
        self.search_path = search_path
        self.handler = handler

    def walk(self):
        for root, _, files in os.walk(self.search_path):
            for filename in files:
                filepath = os.path.join(root, filename)
                self.handler(filepath)

