from PyQt5.QtWidgets import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF

class Main(QWidget) :
    def __init__(self) :
        super(Main, self).__init__()
        self.head = HyperlinkCard("/home/chikatsi/Bureau/Application/ui/Images", "boutton", FIF.ACCEPT, "joel", "putain de programmeur")
        self.vb = QVBoxLayout(self)
        self.vb.addWidget(self.head)


import sys

app = QApplication(sys.argv)

mai = Main()
mai.show()

app.exec()
    
