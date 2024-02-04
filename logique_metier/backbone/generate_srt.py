from logique_metier.backbone import backbone_srt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class generate_file(QThread) :
    error_connexion = pyqtSignal()
    end_generate = pyqtSignal(str)
    def __init__(
        self,
        video_path : str,
        language_src : str,
        language_dest : str,
        type : str,
        horo_name : str,
        path_srt : str
    ) :
        super(generate_file, self).__init__()
        self.videeo_path = video_path
        self.lang_dest = language_dest
        self.lang_src = language_src
        self.type = type
        self.horo_name = horo_name
        self.path_srt = path_srt

    def run(self) :
        try :
            path_srt = backbone_srt.transcribe_audio(
                video_path = self.videeo_path,
                language_dest = self.lang_dest,
                language_src = self.lang_src,
                type = self.type,
                horo_name = self.horo_name,
                path_srt = self.path_srt
            )
            self.end_generate.emit(path_srt)
        except ConnectionError :
            pass