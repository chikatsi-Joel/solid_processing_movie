from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import sys
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from ui import Setup
from qfluentwidgets.multimedia import *
import os 
from pysrt import SubRipFile
from functools import singledispatchmethod

os.environ["QT_GSTREAMER_PLAYBIN_FLAGS"] = str(0x00000017)

class Video_Select(HeaderCardWidget) :
    def __init__(self) :
        super(Video_Select, self).__init__()
        self.setTitle("Choose Video")
        self.lab = CaptionLabel("Selectionner la Video : ")
        self.select = TransparentToolButton(FIF.FOLDER_ADD)
        self.v = QHBoxLayout(self)
        self.v.addWidget(self.lab), self.v.addSpacing(20), self.v.addWidget(self.select)
        self.viewLayout.addLayout(self.v)
        
class SRT_Select(HeaderCardWidget) :
    def __init__(self) :
        super(SRT_Select, self).__init__()
        self.setTitle("Choose SRT")
        self.lab = CaptionLabel("Selectionner le SRT : ")
        self.select = TransparentToolButton(FIF.FOLDER_ADD)
        self.v = QHBoxLayout(self)
        self.v.addWidget(self.lab), self.v.addSpacing(20), self.v.addWidget(self.select)
        
        self.viewLayout.addLayout(self.v)
        
class Barre(QWidget) :
    
    def __init__(self, parent : QWidget | None = ...) :
        super(Barre, self).__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.vid = Video_Select()
        self.srt = SRT_Select()

        self.chat = TransparentPushButton(FIF.CHAT, "Chat AI", self)

        self.vbox.addStretch(), self.vbox.addWidget(self.chat)
        self.vbox.addStretch(), self.vbox.addWidget(self.vid)
        self.vbox.addStretch(), self.vbox.addWidget(self.srt)
        self.setFixedWidth(150)

        setTheme(Theme.DARK)
        
        
class Video_Stream(QWidget) :

    def __init__(self, parent : QWidget) :
        super(Video_Stream, self).__init__(parent)
        self.vbox = QHBoxLayout(self)
        self.media = QVideoWidget()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.positi = SimpleMediaPlayBar()
        self.barr = Barre(self)
        h, h_2, h_subtit = QHBoxLayout(), QVBoxLayout(), QHBoxLayout()
        fr_sub = QFrame()
        self.subtitle_label = StrongBodyLabel("")
        h_subtit.addWidget(self.subtitle_label, 0, Qt.AlignmentFlag.AlignCenter)
        fr, fr_2 = QFrame(), QFrame()
        fr_sub.setLayout(h_subtit)
        h.addWidget(self.barr), h_2.addWidget(self.media)
        h_2.addWidget(self.positi), h_2.addWidget(fr_sub)
        fr_sub.setFrameShape(QFrame.Shape.Panel)
        fr_sub.setObjectName("fme"), 
        fr.setLayout(h), fr.setFrameShape(QFrame.Shape.Panel)
        fr_2.setLayout(h_2), fr_2.setFrameShape(QFrame.Shape.Panel)
        self.vbox.addWidget(fr_2), self.vbox.addWidget(fr)
        fr.setObjectName("fra"), fr_2.setObjectName("fra")
        self.setStyleSheet(open("ui/style/settings.qss", 'r').read())
        self.subtitle_label.setFont(font :=QFont('KacstTitleL'))
        font.setBold(True)

        self.media.setFixedHeight(500)
        self.subtitle_label.setFixedHeight(40)
        self.path_video, self.path_srt = "", ""
        self.barr.srt.select.clicked.connect(self.select_slots_srt)
        self.barr.vid.select.clicked.connect(self.select_slots)
        self.positi.progressSlider.sliderMoved.connect(self.setPosition)
        self.mediaPlayer.setVideoOutput(self.media)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.positi.playButton.clicked.connect(self.play)
        
        self.positi.volumeButton.volumeChanged.connect(self.setVolume)
    
        self.subtitles = []
        self.current_subtitle_index = None
        
    def select_slots(self) :
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select le Video ",
            "/home/chikatsi/Bureau/INFL3/COURS/TP_INF321",
            "Video (*.mp4 *.avi *.3gp *.webm)"
        )
        if filename:
            path = Path(filename)
            self.path_video = str(path)
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(filename)))
            self.mediaPlayer.play()
            InfoBar.success(
                "Chargement réussi",
                "Votre Video a été chargé avec succès",
                Qt.Horizontal,
                isClosable= True,
                duration = 3000,
                position = InfoBarPosition.TOP,
                parent = self
            )
            
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.positi.playButton.setIcon(FIF.PLAY)
        else:
            self.positi.playButton.setIcon(FIF.PAUSE)
            
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            
    def positionChanged(self, position):
        self.positi.progressSlider.setValue(position)
        
        if self.subtitles:
            current_subtitle = self.get_current_subtitle(position)

            if current_subtitle is not None:
                self.subtitle_label.setText(current_subtitle.text)
            else:
                self.subtitle_label.setText("")
                
    def durationChanged(self, duration):
        self.positi.progressSlider.setRange(0, duration)
        
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def setVolume(self) :
        self.mediaPlayer.setVolume(self.positi.volumeButton.volumeView.volumeSlider.value())
        
    def setMute(self) :
        if self.positi.volumeButton.isMuted :
            self.mediaPlayer.setMuted(True)
        
    def get_current_subtitle(self, position):
        if self.current_subtitle_index is not None:
            subtitle = self.subtitles[self.current_subtitle_index]

            if subtitle.start.ordinal <= position <= subtitle.end.ordinal:
                return subtitle

        for index, subtitle in enumerate(self.subtitles):
            if subtitle.start.ordinal <= position <= subtitle.end.ordinal:
                self.current_subtitle_index = index
                return subtitle

        self.current_subtitle_index = None
        return None
      
    def select_slots_srt(self) :
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select le SRT ",
            "/home/chikatsi/Bureau/INFL3/COURS/TP_INF321",
            "SRT (*.srt)"
        )
        if filename:
            path = Path(filename)
            self.path_srt = str(path)
            InfoBar.success(
                "Chargement réussi",
                "Votre SRT a été chargé avec succès",
                Qt.Horizontal,
                isClosable= True,
                duration = 3000,
                position = InfoBarPosition.TOP,
                parent = self
            )
            self.subtitles = SubRipFile.open(self.path_srt)
            self.current_subtitle_index = None

    def play_video_slots(self) :
        self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.path_video)))
        self.mediaPlayer.play()
        self.subtitles = SubRipFile.open(self.path_srt)
        
        
if __name__=='__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    video_str = Video_Stream()
    video_str.show()
    app.exec()