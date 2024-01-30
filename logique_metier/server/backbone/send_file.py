from logique_metier.server.abstract_send_file import abstract_send_file
from logique_metier.server import server
from PyQt5.QtCore import *
from logique_metier.server import setup


class send_file_thread(QThread) :

    error = pyqtSignal(str, str)
    connexion_code = pyqtSignal(int)
    status_video_code = pyqtSignal(int)
    status_srt_code = pyqtSignal(int)
    
    def __init__(
        self,
        server : server.requester,
        file_path : str,
        lang_dep : str,
        lang_cible : str,
        type : str,
        name : str,
        precision : int,
        endpoint_file : str,
        path_srt : str,
        id_user : int,
    ) :
        super(send_file_thread, self).__init__()
        self.server = server
        self.file_path = file_path
        self.name = name
        self.lang_dep = lang_dep
        self.lang_cible = lang_cible
        self.pdf_or_srt = type.lower()
        self.endpoint_file = endpoint_file
        self.path_srt = path_srt
        self.id_user = id_user
        self.type = setup.get_type_by_precision(precision)

    def set_new_path(self, path : str) :
        self.file_path = path

    def run(self) :
        response = self.server.send_file(self.file_path, self.endpoint_file, {
            "lang_dep" : self.lang_dep,
            "lang_cible" : self.lang_cible,
            "type" : self.type,
            "name" : self.name,
            'id' : self.id_user
        })

        if response_code := response.status_code != 200 :
            self.status_video_code.emit(response_code)
        else :
            response_2 = self.server.receive_file(f"{self.pdf_or_srt}/{self.name}", self.name, self.pdf_or_srt, self.path_srt)
            self.status_srt_code.emit(response_2.status_code)
    

    