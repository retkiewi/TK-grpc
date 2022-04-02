from core.model import Model
from gui.main_window import Window
from PyQt5.QtWidgets import QApplication
import sys

def main():
    # Start all components
    model = Model()
    app = QApplication(sys.argv)
    window = Window(model)
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()

