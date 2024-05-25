from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys, os
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets.multimedia import SimpleMediaPlayBar, StandardMediaPlayBar, VideoWidget
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
from interface.decorator import decorator


class Pathh(QWidget) :
    def __init__(self, text) :
        super(Pathh, self).__init__()
        self.icon = AvatarWidget("ui/Images/folder.png")
        self.icon.setRadius(30)
        self.path = BodyLabel(text)
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.icon), self.hbox.addWidget(self.path)
        self.hbox.setSpacing(1)
        
class Extract_Thread(QThread) :
    finish = pyqtSignal()
    def __init__(self, url_video : str, url_audio : str, name_audio : str, format : str) :
        super(Extract_Thread, self).__init__()
        self.path_video = url_video
        self.path_audio = url_audio
        self.name = name_audio
        self.format = format
        
    def run(self) :
        ffmpeg_extract_audio(self.path_video, self.path_audio + "/" + self.name + "." +self.format)
        self.finish.emit()

class Music(HeaderCardWidget) :
    def __init__(self ) :
        super(Music, self).__init__()
        self.setTitle("Extraire l'audio d'une Video")
        self.format_audio = ComboBox(self)
        self.name = LineEdit()
        self.valider = PushButton("Valider")
        self.grid = QGridLayout()
        self.montant_tarifaire = BodyLabel("")
        self.montant = TitleLabel("")
        self.select_video = TransparentToolButton(FIF.FOLDER_ADD)
        self.select_audio = TransparentToolButton(FIF.FOLDER_ADD)
        b = QHBoxLayout()
        self.selec_video, self.selec_audio = Pathh(""), Pathh("")
        self.path, self.path_audio = "", ""
        
        self.format_audio.addItems(['mp3', 'wav', 'opus', 'flac', 'ogg', 'flac', 'aac'])
        selec_video, selec_audio = QHBoxLayout(), QHBoxLayout()
        selec_audio.addWidget(self.select_audio), selec_audio.addWidget(self.selec_audio)
        selec_video.addWidget(self.select_video), selec_video.addWidget(self.selec_video)
        b.addWidget(self.montant_tarifaire), b.addStretch(), b.addWidget(VerticalSeparator()), b.addStretch(), b.addWidget(self.montant)
        self.grid.addWidget(BodyLabel("Sélectionnez la  Video : "), 1, 0), self.grid.addLayout(selec_video, 1, 1, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(BodyLabel("Sélectionnez le repertoire De l'audio : "), 2, 0), self.grid.addLayout(selec_audio, 2, 1, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(BodyLabel("Format de l'audio : "), 3, 0), self.grid.addWidget(self.format_audio, 3, 1)
        self.grid.addWidget(BodyLabel("Nom du fichier audio : "), 4, 0), self.grid.addWidget(self.name, 4, 1)
        self.grid.addWidget(self.valider, 6, 0, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.setVerticalSpacing(20)
        self.grid.addLayout(b, 5, 1), b.addSpacing(20)
        self.viewLayout.addLayout(self.grid)
        
        self.setFixedSize(600, 500)
        
        self.select_video.clicked.connect(self.slots_video)
        self.select_audio.clicked.connect(self.slots_path)
        self.valider.clicked.connect(self.extract_audio)

   
    def slots_video(self) :
        filename, ok = QFileDialog.getOpenFileName(
        self,
            "Select a File",
            "/",
            "Videos (*.mp4)"
        )
        if filename:
            path = Path(filename)
            self.path = str(path)
            self.path = self.path
            self.selec_video.path.setText(self.path)
            

    def slots_path(self) :
        filename = QFileDialog.getExistingDirectory(
        self,
            "Selectionnez un Dossier",
            "/",
        )
        if filename:
            path = Path(filename)
            self.path_audio = str(path)
            self.path_audio = self.path_audio
            self.selec_audio.path.setText(self.path_audio)
    
    @decorator.audio_extract_verification
    def extract_audio(self) :
        self.thread_ = Extract_Thread(self.path, self.path_audio, self.name.text(), self.format_audio.currentText())
        self.thread_.start()
        self.thread_.finish.connect(self.sukess)
        
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
        
class Interface(QWidget) :
    def __init__(self) :
        super(Interface, self).__init__()
        self.vbox = VBoxLayout(self)
        self.music = Music()
        self.vbox.addWidget(self.music, 0, Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(40, 40, 40, 40)
        


if __name__=="__main__" :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    input = Interface()
    input.show()
    app.exec()