from ..backbone import backbone_srt, audio
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class generate_file(QThread) :
    error_connexion = pyqtSignal(str, str)
    end_generate = pyqtSignal(str, str)
    path_srt_emit = pyqtSignal(str)
    def __init__(
        self,
        file_path : str,
        language_src : str,
        language_dep : str,
        type : str,
        pdf_or_srt : str,
        horo_name : str,
        path_srt : str,
        type_movie_or_audio : str
    ) :
        super(generate_file, self).__init__()
        self.videeo_path = file_path
        self.lang_dest = language_dep
        self.lang_src = language_src
        self.type = type
        self.horo_name = horo_name
        self.path_srt = path_srt
        self._pdf_or_srt = pdf_or_srt
        self.type_movie_or_audio = type_movie_or_audio
        
    def run(self) :
        audio_path = self.videeo_path
        if self.type_movie_or_audio == "Movie" :
            audio_name = backbone_srt.generate_name(8)
            audio_path = audio.extract_audio(self.videeo_path, audio_name, 'wav')
        path_srt = backbone_srt.transcribe_audio(
                audio_path = audio_path,
                language_dest = self.lang_dest,
                language_src = self.lang_src,
                pdf_or_srt = self._pdf_or_srt,
                type = self.type,
                horo_name = self.horo_name,
                path_srt = self.path_srt
            )
        self.end_generate.emit("Retranscription Terminé😎", f"Path du srt : {path_srt}")
        self.path_srt_emit.emit(path_srt)