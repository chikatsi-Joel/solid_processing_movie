from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, os
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from interface.decorator import decorator

from logique_metier.tts.audio_cloning_backbone import tts_apply

class Pathh(QWidget) :
    def __init__(self, text) :
        super(Pathh, self).__init__()
        self.icon = AvatarWidget("ui/Images/folder.png")
        self.icon.setRadius(30)
        self.path = BodyLabel(text)
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.icon), self.hbox.addWidget(self.path)
        self.hbox.setSpacing(1)
        


class cloning(HeaderCardWidget) :
    def __init__(self ) :
        super(cloning, self).__init__()
        self.setTitle("Cloning Audio VOice")
        self.name = LineEdit()
        self.valider = PushButton("Valider")
        
        self.grid = QGridLayout()
        self.montant_tarifaire = BodyLabel("")
        self.montant = TitleLabel("")
        self.output_audio = LineEdit()
        self.select_video = TextEdit()
        self.langugage = ComboBox()
        self.select_audio = TransparentToolButton(FIF.FOLDER_ADD)
        b = QHBoxLayout()
        self.selec_video, self.selec_audio = Pathh(""), Pathh("")
        self.langugage.addItems(['en', 'fr'])
        self.path, self.path_audio = "", ""
        
        selec_video, selec_audio = QHBoxLayout(), QHBoxLayout()

        selec_audio.addWidget(self.select_audio), selec_audio.addWidget(self.selec_audio)
        selec_video.addWidget(self.select_video), selec_video.addWidget(self.selec_video)
        b.addWidget(self.montant_tarifaire), b.addStretch(), b.addWidget(VerticalSeparator()), b.addStretch(), b.addWidget(self.montant)
        self.grid.addWidget(BodyLabel("Entrer le texte : "), 1, 0), self.grid.addLayout(selec_video, 1, 1, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(BodyLabel("Sélectionnez l'audio de synthèse : "), 2, 0), self.grid.addLayout(selec_audio, 2, 1, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(BodyLabel("NOm de l'audio de Sortie: "), 3, 0), self.grid.addWidget(self.output_audio, 3, 1)
        self.grid.addWidget(BodyLabel("Nom du fichier audio : "), 4, 0), self.grid.addWidget(self.name, 4, 1)
        self.grid.addWidget(BodyLabel("Language : "), 5, 0), self.grid.addWidget(self.langugage, 5, 1)
        self.grid.addWidget(self.valider, 7, 0, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.setVerticalSpacing(20)
        self.viewLayout.addLayout(self.grid)
        
        self.setFixedSize(600, 500)
        
        self.select_audio.clicked.connect(self.slots_path)

   

    def slots_path(self) :
        filename = QFileDialog.getOpenFileName(
        self,
            "Selectionnez un Dossier",
            "/home/chikatsi/Bureau",
            "Audio (*.wav)"
        )
        if filename:
            path = Path(filename)
            self.path_audio = str(path)
            self.path_audio = self.path_audio
            InfoBar.success(
            "Chargement Réussie",
            "L'audio a été chargé avec succcès..\n",
            duration = 3000,
            parent = self.parent()
        )
   
    def sukess(self) :
        InfoBar.success(
            "Opération Réussie",
            "L'extraction a été\néffectué avec succès\n",
            duration = 3000,
            parent = self
        )

    def warning(self, title : str, content : str) :
        InfoBar.warning(
            title,
            content,
            duration = 3500,
            parent = self
        )
        
class audio_cloning(QWidget) :
    def __init__(self) :
        super(audio_cloning, self).__init__()
        self.vbox = VBoxLayout(self)
        self.cloning = cloning()
        self.vbox.addWidget(self.cloning, 0, Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(40, 40, 40, 40)
        


if __name__=="__main__" :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    input = audio_cloning()
    input.show()
    app.exec()