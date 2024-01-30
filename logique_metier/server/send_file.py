from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import logique_metier.server.server as  server


class send_file(QThread) :
    status_code = pyqtSignal(int)
    def __init__(
        self,
        server : server.requester,
        file_path : str,
        lang_dep : str,
        lang_cible : str,
        type : str,
        name : str,
        endpoint_file : str,
        path_srt : str,
        id_user : int
    ) :
        super(send_file, self).__init__()
        self.server = server
        self.file_path = file_path
        self.name = name
        self.lang_dep = lang_dep
        self.lang_cible = lang_cible
        self.type = type
        self.endpoint_file = endpoint_file
        self.path_srt = path_srt
        self.id_user = id_user
        
        
    def run(self) :
        response = self.server.send_file(self.file_path, self.endpoint_file, {
            "lang_dep" : self.lang_dep,
            "lang_cible" : self.lang_cible,
            "type" : self.type,
            "name" : self.name,
            'id' : self.id_user
        })

        reponse_2 = self.server.receive_file(f'srt/{self.name}', self.name, "srt", self.path_srt)
        self.status_code.emit(response.status_code)