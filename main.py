from ui import (
    youtube_interface,
    video_extract_audio_interface,
    stream_video_interface,
    video_retranscript_interface,
    parameters_interface
)


from interface.download import DownLaod
from interface.decorator import decorator
from logique_metier.backbone.generate_srt import generate_file
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
    def _(self, user_info : dict[str, str | int | float]) :
        super(Main_Application, self).__init__()

        self.user_info = user_info
        self.settings = parameters_interface.parameters_interface()

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

        """
        outils configuration visionnage
        """
        self.path_srt = ""
        self.path_video = ""
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

        self.setWindowIcon(QIcon("ui/Images/logo.png"))
        self.titleBar
        self.setWindowTitle("Video Processing")

        
        self.youtube_interface.barr.send.clicked.connect(self.slots_youtube_down)
        self.youtube_interface.precision.video.valider.clicked.connect(self.slots_youtube_srt_generate)
        self.video_retranscribe_interface.precision.video.valider.clicked.connect(self.slots_srt_generate_video)
        self.youtube_interface.precision.video.visionner.clicked.connect(self.slots_visionnage_immediat_yout)
        self.video_retranscribe_interface.precision.video.visionner.clicked.connect(self.slots_visionnage_immediat_video)
        self.setFixedSize(1250, 676)


    """
    Slots pour le téléchargement des vidéos youtube
    """
    @decorator.youtube_verification
    def slots_youtube_down(self) : 
        params = {
            "url_video" : self.youtube_interface.barr.edit.text().strip(),
            "url_destination" : self.youtube_interface.barr.path_folder,
            "file_name" : self.youtube_interface.barr.edit_nom_video.text().strip(),
        }
        self.down = DownLaod(download_on_youtube(**params))
        self.down.start()

        self.stateTooltip = StateToolTip('Patientez un instant', 'Votre téléchargement est en cours.\nPatientez svp...', self)
        self.stateTooltip.show()

        self.down.endDownload.connect(self.set_video_path)
        self.down.endDownload.connect(lambda: self.stateTooltip.hide())
        self.down.lienInexistant.connect(self.youtube_interface.barr.slots_lien_In)
        self.down.erreur.connect(self.youtube_interface.barr.slots_lien_err)
        

    """
    Slots de génération de fichier srt via youtube
    """
    @decorator.precision_verification
    def slots_youtube_srt_generate(self) :
        try :
            params = self.youtube_interface.precision.get_params()
            try :
                url_video = self.youtube_interface.get_url_video()
                params.update({"file_path" : url_video})
                send_fil = generate_file(
                    **params,
                )
                send_fil.start()
                self.champ_info("Infos", "Retranscription Lancé")
                self.stateTooltip = StateToolTip('Patientez un instant', 'Votre Retranscription est en cours.\nPatientez svp...', self)
                self.stateTooltip.show()
                send_fil.path_srt_emit.connect(self.set_path_srt)
                send_fil.end_generate.connect(self.champ_success)
                send_fil.error_connexion.connect(self.youtube_interface.precision.connexion_slots)

            except AttributeError as e :
                self.champ_warning("Not Video Found", "Aucune vidéo n'a été \n sélectionné. Veuillez allé dans un autre bloc..")
            except Exception :
                self.champ_warning("Erreur rencontré", "Vous devez être connecté a internet\n pour éffectuer la retranscription..")
        except ValueError as e :
            self.champ_warning("Precision Vide", f"La précision mérite \nune valeur...\n {str(e)}")



    """
    Slots de génération de srt d'une vidéo
    """
    @decorator.precision_verification
    def slots_srt_generate_video(self) :
        try :
            params = self.video_retranscribe_interface.precision.get_params()
            try :
                url_video = self.video_retranscribe_interface.load_file.get_params()
                params.update(url_video)
                send_fil = generate_file(
                    **params,
                )
                send_fil.start()
                send_fil.error_connexion.connect(self.champ_warning)
                self.champ_info("Infos", "Retranscription Lancé")
                self.stateTooltip = StateToolTip('Patientez un instant', 'Votre Retranscription est en cours.\nPatientez svp...', self)
                self.stateTooltip.show()
                send_fil.path_srt_emit.connect(self.set_path_srt)
                send_fil.end_generate.connect(self.champ_success)
            except AttributeError as e :
                self.champ_warning("Not video FOund", "Aucune vidéo n'a été \n sélectionné. Veuillez choisir la vidéo")
            except Exception :
                self.champ_warning("Erreur rencontré", "Vous devez être connecté a internet\n pour éffectuer la retranscription..")
        except ValueError as e :
            self.champ_warning("Precision Vide", f"La précision mérite \nune valeur...\n {str(e)}")

    """
    slot de visionnage immédiat
    """

    def slots_visionnage_immediat_yout(self) :
        if self.video_interface.path_srt == "" :
            self.champ_warning("selecionnez le SRT", "Aucun fichier srt n'a été sélectionné")
            return         
        try :
            self.video_interface.path_video = self.youtube_interface.get_url_video()
        except AttributeError :
            self.champ_warning("Selectionnez la video", "Aucune video n'est sélectionné")
            return
        self.switchTo(self.video_interface)

        self.video_interface.play_video_slots()

    def slots_visionnage_immediat_video(self) :
        self.path_video = self.video_retranscribe_interface.get_video_path()
        if self.path_srt == "" :
            self.champ_warning("selecionnez le SRT", "Aucun fichier srt n'a été sélectionné")
            return 
        if self.path_video == "" :
            self.champ_warning("selecionnez la Video", "Aucune vidéo n'a été sélectionné")
            return 
        self.switchTo(self.video_interface)
        self.video_interface.path_srt = self.path_srt
        self.video_interface.path_video = self.path_video
        self.video_interface.play_video_slots()

    

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

    def notification_number(self, rootkey : str, number : int) :
        item = self.navigationInterface.widget(rootkey)
        InfoBadge.warning(
            text = str(number),
            parent = item.parent(),
            target = item
        )

    def set_video_path(self, path : str) :
        self.path_video = path

    def set_path_srt(self, path : str) :
        self.stateTooltip.hide()
        self.path_srt = path

if __name__=="__main__" :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  
    app = QApplication(sys.argv)
    input = Main_Application({"id" : 3, "name" : "Joel", 'age' : 20, 'solde' : 189211.1212})
    input.show()
    app.exec()