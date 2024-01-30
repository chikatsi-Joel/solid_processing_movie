from ui import (
    youtube_interface,
    video_extract_audio_interface,
    stream_video_interface,
    video_retranscript_interface,
    help_interface,
    parameters_interface
)
from interface.download import DownLaod
import interface.decorator as decorator
from logique_metier.server.backbone import send_file
from logique_metier.server import server
from logique_metier.generate.download_file import download_on_youtube
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
        
from requests.exceptions import InvalidSchema
from functools import singledispatchmethod


class Main_Application(FluentWindow) :
    @singledispatchmethod
    def __init__(self, args) :
        raise NotImplementedError("méthode non implémenté")
    
    @__init__.register(int)
    def _(self, id : int) :
        pass

    @__init__.register(str)
    def _(self, email : str) :
        pass
    
    @__init__.register(dict)
    @__init__.register(QWidget)
    def _(self, user_info : dict[str, str | int | float], settings : QWidget) :
        super(Main_Application, self).__init__()

        self.user_info = user_info
        self.settings = settings
        self.help = help_interface.help_interface({})
        self.server = server.requester("", 5000)

        self.home = QWidget()
        self.video_interface = stream_video_interface.Video_Stream(parent = self)
        self.video_retranscribe_interface = video_retranscript_interface.Interface()
        self.video_extract_audio = video_extract_audio_interface.Interface()
        self.youtube_interface = youtube_interface.Interface()

        self.video_interface.setObjectName("video_interface")
        self.video_retranscribe_interface.setObjectName('video_retranscribe_interface')
        self.video_extract_audio.setObjectName('video_extract_audio')
        self.youtube_interface.setObjectName("youtube_interface")
        self.settings.setObjectName("settings")
        self.help.setObjectName("help")

        self.addSubInterface(
            interface = self.youtube_interface,
            icon = "ui/Images/you.png",
            text = "Youtube",
        )

        self.addSubInterface(
            interface = self.video_retranscribe_interface,
            icon = FIF.CLOUD_DOWNLOAD,
            text = "Video Retranscribe",
        )

        self.addSubInterface(
            interface = self.video_extract_audio,
            icon = FIF.MUSIC,
            text = "Audio Extract",
        )

        self.addSubInterface(
            interface = self.youtube_interface,
            icon = "Images/youtube.png",
            text = "Youtube Processing",
        )

        self.addSubInterface(
            interface = self.video_interface,
            icon = FIF.MOVIE,
            text = "Video Stream",
        )

        self.navigationInterface.addSeparator(position = NavigationItemPosition.BOTTOM)
        
        self.addSubInterface(
            interface =  self.settings,
            icon = FIF.SETTING,
            text = 'Paramètres',
            position = NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(
            interface =  self.help,
            icon = FIF.HELP,
            text = 'Aide',
            position = NavigationItemPosition.BOTTOM
        )

        self.setWindowIcon(QIcon("ui/Images/logo.png"))

        
        self.youtube_interface.barr.send.clicked.connect(self.slots_youtube_down)
        self.youtube_interface.precision.video.valider.clicked.connect(self.slots_youtube_srt_generate)
        self.video_retranscribe_interface.precision.video.valider.clicked.connect(self.slots_srt_generate_video)
        self.help.chat.zone_saisie.writable.send.clicked.connect(self.send_message_slots)

        self.setFixedSize(1250, 680)

    """
    Envoie des messages via le slot correspondant..
    """
    def send_message_slots(self) :
        text = self.help.chat.zone_saisie.writable.toPlainText()
        self.help.chat.zone_message.add_widget(text)
        self.help.chat.zone_saisie.writable.clear()

    

    def set_settings(self, sett_interface : QWidget) :
        self.settings = sett_interface
        self.settings.setObjectName("setting")

    """
    Slots pour le téléchargement des vidéos youtube
    """
    #@decorator.Verification(type = "youtube")
    def slots_youtube_down(self) : 
        params = {
            "url_video" : self.youtube_interface.barr.edit.text().strip(),
            "url_destination" : self.youtube_interface.barr.path,
            "file_name" : self.youtube_interface.barr.edit_nom_video.text().strip(),
        }
        self.down = DownLaod(download_on_youtube(**params))
        self.down.start()

        self.down.endDownload.connect(self.youtube_interface.barr.endDown)
        self.down.lienInexistant.connect(self.youtube_interface.barr.slots_lien_In)
        self.down.erreur.connect(self.youtube_interface.barr.slots_lien_err)
        

    """
    Slots de génération de fichier srt via youtube
    """
    def slots_youtube_srt_generate(self) :
        try :
            params = self.youtube_interface.precision.get_params()
            try :
                url_video = self.youtube_interface.get_url_video()
                params.update({"file_path" : url_video})
                send_fil = send_file.send_file_thread(
                    server = self.server,
                    endpoint_file = 'video',
                    id_user = self.user_info['id'],
                    **params,
                )
                send_fil.start()

                send_fil.connexion_code.connect(self.youtube_interface.precision.connexion_slots)
                send_fil.status_video_code.connect(self.youtube_interface.precision.status_video_slots)
                send_fil.status_srt_code.connect(self.youtube_interface.precision.status_slots)
            except AttributeError as e :
                self.champ_warning("Not Video Found", "Aucune vidéo n'a été \n sélectionné. Veuillez allé dans un autre bloc..")
            except InvalidSchema as e :
                self.champ_warning("Erreur de connexion", "Host et Port non défini..\nVous n'êtes pas connecté au serveur.")
            except InterruptedError as e:
                self.champ_warning("Erreur de connexion", "Connexion NOn établie..")
        except ValueError as e :
            self.champ_warning("Precision Vide", f"La précision mérite \nune valeur...\n {str(e)}")


    """
    Slots de génération de srt d'une vidéo
    """
    def slots_srt_generate_video(self) :
        try :
            params = self.video_retranscribe_interface.precision.get_params()
            try :
                url_video = self.video_retranscribe_interface.load_file.get_params()
                params.update(url_video)
                send_fil = send_file.send_file_thread(
                    server = self.server,
                    endpoint_file = 'video',
                    id_user = self.user_info['id'],
                    **params,
                )
                send_fil.run()

                send_fil.error.connect(self.champ_warning)
                send_fil.connexion_code.connect(self.video_retranscribe_interface.precision.connexion_slots)
                send_fil.status_video_code.connect(self.video_retranscribe_interface.precision.status_video_slots)
                send_fil.status_srt_code.connect(self.video_retranscribe_interface.precision.status_slots)
            except AttributeError as e :
                self.champ_warning("Not video FOund", "Aucune vidéo n'a été \n sélectionné. Veuillez choisir la vidéo")

            except InvalidSchema as e :
                self.champ_warning("Erreur de connexion", "Host et Port non défini..\nVous n'êtes pas connecté au serveur.")
            except InterruptedError as e:
                self.champ_warning("Erreur de connexion", "Connexion NOn établie..")
        except ValueError as e :
            self.champ_warning("Precision Vide", f"La précision mérite \nune valeur...\n {str(e)}")


    def champ_warning(self, title : str, content : str) :
        InfoBar.warning(
            title,
            content,
            duration = 3000,
            parent = self
        )
    
    def champ_info(self, title : str, content : str) :
        InfoBar.info(
            title,
            content,
            duration = 3000,
            parent = self
        )

    def champ_success(self, title : str, content : str) :
        InfoBar.success(
            title,
            content,
            duration = 3000,
            parent = self
        )

    def notification_number_clear(self, rootkey : str, number : int) :
        item = self.navigationInterface.widget(rootkey)
        item.clicked.connect()        

    def notification_number(self, rootkey : str, number : int) :
        item = self.navigationInterface.widget(rootkey)
        InfoBadge.warning(
            text = str(number),
            parent = item.parent(),
            target = item
        )

if __name__=="__main__" :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    input = Main_Application({"id" : 3, "name" : "Joel", 'age' : 23, 'solde' : 189211.1212}, settings = QWidget())
    input.set_settings(parameters_interface.parameters_interface("ui/Images/moi.png", "Joel", "https://beta.theb.ai/home", 21, 500, 800, "kappachikatsi@gmail.com", "Promotteur en chef du projet et Etudiant en licence 3 à l'université de Yaoundé 1"))
    input.show()
    app.exec()