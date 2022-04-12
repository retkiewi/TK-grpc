from cProfile import label
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QCheckBox, QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt

class FormatChooseWindow(QDialog):
    def __init__(self, parent=None):
        self.accepted = False
        self.rejected = False
        super(FormatChooseWindow, self).__init__(parent)
        lay = QVBoxLayout()
        layout = QHBoxLayout()
        layout0 = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout.addLayout(layout0)
        layout.addLayout(layout1)
        lay.addLayout(layout)
        self.setWindowTitle("Format choose Window")
        self.setGeometry(300, 300, 450, 300)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accepting)
        self.buttonBox.rejected.connect(self.rejecting)
        
        lay.addWidget(self.buttonBox)

        self.fStrings = [
            "jpeg", "jpeg2000", "gif", "bmp", "png",
            "webp", "ico", "img", "xcf", "cgm", "svg",
            "blend", "xaml", "pdf"
        ]
        self.formats = {}

        for s in self.fStrings:
            fExtension = "." + s
            selfB = "self." + s
            exec("%s = False" % (selfB))
            self.formats[s] = [QCheckBox(fExtension), False]

        self.formats["jpeg"][0].stateChanged.connect(lambda: self.setState(self.formats["jpeg"][0]))
        self.formats["jpeg2000"][0].stateChanged.connect(lambda: self.setState(self.formats["jpeg2000"][0]))
        self.formats["gif"][0].stateChanged.connect(lambda: self.setState(self.formats["gif"][0]))
        self.formats["bmp"][0].stateChanged.connect(lambda: self.setState(self.formats["bmp"][0]))
        self.formats["png"][0].stateChanged.connect(lambda: self.setState(self.formats["png"][0]))
        self.formats["webp"][0].stateChanged.connect(lambda: self.setState(self.formats["webp"][0]))
        self.formats["ico"][0].stateChanged.connect(lambda: self.setState(self.formats["ico"][0]))
        layout0.addWidget(self.formats["jpeg"][0])
        layout0.addWidget(self.formats["jpeg2000"][0])
        layout0.addWidget(self.formats["gif"][0])
        layout0.addWidget(self.formats["bmp"][0])
        layout0.addWidget(self.formats["png"][0])
        layout0.addWidget(self.formats["webp"][0])
        layout0.addWidget(self.formats["ico"][0])


        self.formats["img"][0].stateChanged.connect(lambda: self.setState(self.formats["img"][0]))
        self.formats["xcf"][0].stateChanged.connect(lambda: self.setState(self.formats["xcf"][0]))
        self.formats["cgm"][0].stateChanged.connect(lambda: self.setState(self.formats["cgm"][0]))
        self.formats["svg"][0].stateChanged.connect(lambda: self.setState(self.formats["svg"][0]))
        self.formats["blend"][0].stateChanged.connect(lambda: self.setState(self.formats["blend"][0]))
        self.formats["xaml"][0].stateChanged.connect(lambda: self.setState(self.formats["xaml"][0]))
        self.formats["pdf"][0].stateChanged.connect(lambda: self.setState(self.formats["pdf"][0]))
        layout1.addWidget(self.formats["img"][0])
        layout1.addWidget(self.formats["xcf"][0])
        layout1.addWidget(self.formats["cgm"][0])
        layout1.addWidget(self.formats["svg"][0])
        layout1.addWidget(self.formats["blend"][0])
        layout1.addWidget(self.formats["xaml"][0])
        layout1.addWidget(self.formats["pdf"][0])

        self.setLayout(lay)

    def setState(self, cB):
        k = cB.text()[1:]
        if(self.formats[k][0].checkState() == Qt.Checked):
            self.formats[k][1] = True
        else:
            self.formats[k][1] = False
        print(k, self.formats[k][0].checkState(), self.formats[k][1])

    def accepting(self):
        self.setFormat()
        self.accepted = True
        self.rejected = False
        self.accept()

    def rejecting(self):
        self.accepted = False
        self.rejected = True
        self.reject()

    def setFormat(self):
        formatsToMain = []
        for k,cB in self.formats.items():
            if cB[1] == True:
                formatsToMain.append(k)
        self.parent().formats = formatsToMain
        print(formatsToMain)