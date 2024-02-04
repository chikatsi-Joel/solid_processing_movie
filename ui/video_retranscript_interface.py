
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from ui import precision_interface
from functools import singledispatchmethod


class Item(QWidget) :
    @singledispatchmethod
    def __init__(self, args) :
        raise NotImplementedError
    
    @__init__.register(int)
    def _(self, value : int) :
        pass

    @__init__.register(dict)
    def _(self, value : dict) :
        """
        contenu secret et juste pour l'appli premium
        """
        pass

    @__init__.register(str)
    def _(self, text : str, parent : QWidget | None = None) :
        super(Item, self).__init__(parent)
        self.hbox = QHBoxLayout(self)
        ico = ImageLabel("Images/folder.png")
        self.lab = CaptionLabel(text)
        self.frame = QFrame()
        self.hbox.addWidget(SubtitleLabel(">"))
        ico.scaledToWidth(24)
        self.hbox.addWidget(ico), self.hbox.addStretch() ,self.hbox.addWidget(self.lab)
        self.setContentsMargins(50, 1, 1, 1)
        self.frame.setLayout(self.hbox), self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setStyleSheet(open("ui/style/settings.qss", 'r').read())
        vbox = QVBoxLayout(self)
        self.frame.setFixedHeight(50), self.frame.setFixedWidth(300)
        vbox.addWidget(self.frame)
        
 
class Load_file(HeaderCardWidget) :
    def __init__(self) :
        super(Load_file, self).__init__()
        self.setTitle("Selectionner la Video")

        self.tit = SubtitleLabel("File")
        self.tit_path = SubtitleLabel("Choisir l'emplacement du SRT  : ")
        self.butt = PushButton("Select", self, FIF.FOLDER_ADD)
        self.empla = PushButton("Select", self, FIF.FOLDER_ADD)
        self.sep = HorizontalSeparator()
        h = QGridLayout()
        self.vbox = QVBoxLayout()
        self.item, self.path = None, ""
        self.srt_path = ""
        h.addWidget(self.tit, 0, 0),h.addWidget(self.butt, 0, 1)
        h.addWidget(self.tit_path, 1, 0), h.addWidget(self.empla, 1, 1)
        self.vbox.addLayout(h), self.vbox.addWidget(self.sep)
        
        self.viewLayout.addLayout(self.vbox)
        self.butt.clicked.connect(self.slots_con)
        self.empla.clicked.connect(self.slots_path)
        self.setFixedWidth(500)

    def slots_con(self) :
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select le Video ",
            "/home/chikatsi/Bureau/INFL3/COURS/TP_INF321",
            "Video (*.mp4 *.avi *.3gp *.webm)"
        )
        if filename:
            path = Path(filename)
            self.path = str(path)
            self.addFolder(self.path)
        
    def slots_path(self) :
        filename = QFileDialog.getExistingDirectory(
        self,
            "Selectionnez un Dossier",
            "/home/",
        )
        if filename:
            path = Path(filename)
            self.srt_path = str(path)
            print(self.srt_path)
        
    def addFolder(self, path : str) :
        self.item = Item(path, self)
        self.vbox.addWidget(self.item)
        self.vbox.addStretch()

    def add_widget(self, widget : QWidget) :
        self.vbox.addWidget(widget)

    def get_params(self) -> dict[str, str]:
        if self.path.strip() == "" :
            raise AttributeError("Erreur")
        return {
            'file_path' : self.path
        }



class Interface(QWidget) :
    def __init__(self, parent : QWidget | None = None, **kwargs) :
        super(Interface, self).__init__(parent = parent, **kwargs)

        self.central = QVBoxLayout(self)
        self.hbox = QHBoxLayout()

        self.load_file = Load_file()
        self.precision = precision_interface.Interface(parent = self)

        self.hbox.addWidget(self.load_file), self.hbox.addWidget(self.precision)

        self.central.addLayout(self.hbox)

        self.setStyleSheet(open("ui/style/settings.qss", 'r').read())

    def get_srt_path(self) -> str:
        return self.precision.srt_path
    
    def get_video_path(self) : 
        return self.load_file.path


if __name__=="__main__" :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    input = Interface()
    input.show()
    app.exec()