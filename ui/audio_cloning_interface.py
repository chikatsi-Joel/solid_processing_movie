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
        self.setTitle("Extraire l'audio d'une Video")
        self.langugage = ComboBox(self)
        self.name = LineEdit()
        self.valider = PushButton("Valider")
        self.grid = QGridLayout()
        self.montant_tarifaire = BodyLabel("")
        self.montant = TitleLabel("")
        self.text = TextEdit()
        self.select_repertoire = TransparentToolButton(FIF.FOLDER_ADD)
        self.select_audio = TransparentToolButton(FIF.FOLDER_ADD)
        b = QHBoxLayout()
        self.repertoire, self.selec_audio = Pathh(""), Pathh("")
        self.path, self.path_audio = "", ""
        
        self.langugage.addItems(['en', 'fr'])
        repertoire, selec_audio = QHBoxLayout(), QHBoxLayout()
        selec_audio.addWidget(self.select_audio), selec_audio.addWidget(self.selec_audio)
        repertoire.addWidget(self.select_repertoire), repertoire.addWidget(self.repertoire)
        b.addWidget(self.montant_tarifaire), b.addStretch(), b.addWidget(VerticalSeparator()), b.addStretch(), b.addWidget(self.montant)
        self.grid.addWidget(BodyLabel("Sélectionnez le repertoire de destination : "), 1, 0), self.grid.addLayout(repertoire, 1, 1)
        self.grid.addWidget(BodyLabel("Sélectionnez l'audio échantillon : "), 2, 0), self.grid.addLayout(selec_audio, 2, 1, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(BodyLabel("Text de tuning : "), 3, 0), self.grid.addWidget(self.text, 3, 1, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(BodyLabel("langugage de  l'audio : "), 4, 0), self.grid.addWidget(self.langugage, 4, 1)
        self.grid.addWidget(BodyLabel("Nom du fichier audio : "), 5, 0), self.grid.addWidget(self.name, 5, 1)
        self.grid.addWidget(self.valider, 6, 0, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.setVerticalSpacing(20)
        self.viewLayout.addLayout(self.grid)
        
        self.setFixedSize(600, 500)
        
        self.select_repertoire.clicked.connect(self.slots_audio)
        self.select_audio.clicked.connect(self.slots_path)

   
    def slots_audio(self) :
        filename, ok = QFileDialog.getOpenFileName(
        self,
            "Select a File",
            "/",
            "Audio (*.wav)"
        )
        if filename:
            path = Path(filename)
            self.path_audio = str(path)
            

    def slots_path(self) :
        filename = QFileDialog.getExistingDirectory(
        self,
            "Selectionnez un Dossier",
            "/",
        )
        if filename:
            path = Path(filename)
            self.path = str(path)
   
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

    def apply(self) :
        tts_apply(
            self.cloning.text.toPlainText(),
            self.cloning.path_audio,
            self.cloning.langugage.currentText(),
            self.cloning.path + '/' + self.cloning.name.text()
        )
        
        
