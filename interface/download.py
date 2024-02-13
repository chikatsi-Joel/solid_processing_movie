from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget
from pytube.exceptions import RegexMatchError
from logique_metier.download_file import download_file_logic
from logique_metier.abstract_logic.abstract_download import abstract_download 


class DownLaod(QThread) :
    endDownload = pyqtSignal(str)
    lienInexistant = pyqtSignal(str)
    erreur = pyqtSignal(str)

    def __init__(self, download_type : abstract_download, tool : QWidget) :
        super(DownLaod, self).__init__()
        self.download_type = download_type
        self.tool = tool

    def set_download_type(self, download_type : abstract_download) :
        self.downlad_type = download_type

    def run(self) : 
        try :
            self.tool.show()
            path = download_file_logic.download(self.download_type)
            self.endDownload.emit(path)
        except RegexMatchError as e : 
            self.lienInexistant.emit("Lien Inexistant")
            return
        except Exception as e :
            self.erreur.emit(str(e))
            return
