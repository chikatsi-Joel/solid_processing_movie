from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from ui import Setup
        

class CardSeparator(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(3)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if isDarkTheme():
            painter.setPen(QColor(255, 255, 255, 46))
        else:
            painter.setPen(QColor(0, 0, 0, 12))

        painter.drawLine(2, 1, self.width() - 2, 1)
        
class Precision(HeaderCardWidget) :
    def __init__(self, parent : QWidget | None = None) :
        super(Precision, self).__init__(parent = parent)
        self.setTitle("Generer Fichier")
        self.lang_cible = ComboBox(self)
        self.lang_dep = ComboBox(self)
        self.name = LineEdit()
        self.evolution = ProgressRing()
        self.typ = ComboBox()
        self.valider, self.visionner = PushButton("Valider"), PushButton("visionner", self, FIF.MOVIE)
        self.lang_cible.addItems(list(map(str.capitalize, list(Setup.Setup.lang.keys())[1:])))
        self.lang_dep.addItems(list(map(str.capitalize, Setup.Setup.lang.keys())))
        self.grid = QGridLayout()
        hbox = QHBoxLayout()
        self.montant_tarifaire = BodyLabel("")
        self.montant = TitleLabel("")
        b = QHBoxLayout()
        self.path_srt = ""
        self.sep = CardSeparator(self)
        self.srt_but = PushButton(text = "choose srt path", icon = FIF.FOLDER_ADD)
        self.typ.addItems(["SRT", "PDF"])
        b.addWidget(self.montant_tarifaire), b.addStretch(), b.addWidget(VerticalSeparator()), b.addStretch(), b.addWidget(self.montant)
        self.precision, self.val_precis  = LineEdit(), TransparentToolButton(FIF.ACCEPT)
        hbox.addWidget(self.evolution, 1, Qt.AlignmentFlag.AlignLeft), hbox.addStretch() ,hbox.addWidget(self.precision),  hbox.addStretch(), hbox.addWidget(self.val_precis)
        self.evolution.setTextVisible(True)
        self.grid.addWidget(BodyLabel("Définir le type de fichier : "), 0, 0), self.grid.addWidget(self.typ, 0, 1)
        self.grid.addWidget(BodyLabel("Select : "), 1, 0), self.grid.addWidget(self.srt_but, 1, 1)
        self.grid.addWidget(BodyLabel("Language De la Video : "), 2, 0), self.grid.addWidget(self.lang_dep, 2, 1)
        self.grid.addWidget(BodyLabel("Language Cible : "), 3, 0), self.grid.addWidget(self.lang_cible, 3, 1)
        self.grid.addWidget(BodyLabel("Nom du fichier : "), 4, 0), self.grid.addWidget(self.name, 4, 1)
        self.grid.addWidget(BodyLabel("Entrer la Precision : "), 5, 0), self.grid.addLayout(hbox, 5, 1)
        self.grid.addWidget(self.visionner, 7, 1, alignment = Qt.AlignmentFlag.AlignRight), self.grid.addWidget(self.valider, 7, 0, alignment = Qt.AlignmentFlag.AlignLeft)
        self.grid.addLayout(b, 6, 1), b.addSpacing(20)
        self.visionner.setFixedWidth(120), self.valider.setFixedWidth(120)
        self.visionner.setFixedHeight(45), self.valider.setFixedHeight(45)
        self.viewLayout.addLayout(self.grid)
        self.vBoxLayout.addWidget(self.sep)
        h = QHBoxLayout()
        h.addStretch(), h.addWidget(CaptionLabel("site web")), h.addWidget(TransparentToolButton(FIF.SHARE))
        h.setContentsMargins(10, 10, 10, 10)
        self.value = 0
        self.vBoxLayout.addLayout(h)
        self.precision.setValidator(QIntValidator())
        self.precision.setFixedWidth(80)
        
        self.val_precis.clicked.connect(self.evolution_slot)
        self.val_precis.clicked.connect(self.tarif_slot)
        self.srt_but.clicked.connect(self.selectionner_folder)

        self.setFixedHeight(538)

        self.setStyleSheet(open("ui/style/settings.qss", 'r').read())
        setTheme(Theme.DARK)
        self.par = parent if parent != None else self

    def evolution_slot(self) :
        self.value = self.evolution.value()
        self.timer = QTimer()
        if self.precision.text().strip() == '':
            return
        if(self.value == int(self.precision.text().strip())) :
            return
        self.timer.timeout.connect(self.count if self.value < int(self.precision.text()) else self.decount)
        self.timer.start(30)
        
    def count(self) :
        self.value  += 1 
        self.evolution.setValue(self.value)
        if(self.value == int(self.precision.text().strip())) :
            self.timer.stop()
            
    def decount(self) :
        self.value  -= 1 
        self.evolution.setValue(self.value)
        if(self.value == int(self.precision.text().strip())) :
            self.timer.stop()
            
    def tarif_slot(self) :
        if self.precision.text().strip() == "" :
            return
        if (montant :=Setup.Setup.tarif(int(self.precision.text()))) == 0 :
            self.montant_tarifaire.setText(""), self.montant.setText("")
        else :
            self.montant_tarifaire.setText(f"Le coût sera de  : ")
            self.montant.setText(f'  {montant} $')
            self.beta_mode()
            
    def beta_mode(self) :
        InfoBar.info(
            "Mode Payant",
            content = "La précision que vous avez \nsélectionnez est payante car, elle \nnécessite une grande puissance de \ncalcul",
            isClosable = True,
            orient = Qt.Orientation.Horizontal,
            position= InfoBarPosition.TOP_RIGHT,
            parent = self.par,
            duration = 5000
        )


    def selectionner_folder(self) :
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "Choisir Le Dossier",
            "Chemin d'accès  : "
        )
        if dir_name:
            self.path_srt = str(Path(dir_name))
    




class  Interface(QWidget) :
    send_all_data_by_validate = pyqtSignal(QWidget)
    def __init__(self, parent : QWidget | None = None):
        super(Interface, self).__init__(parent = parent)
        self.central = QHBoxLayout()
        self.box = QVBoxLayout(self)
        self.video = Precision(self)
        hbox = QHBoxLayout()
        ico = IconWidget(FIF.VIDEO)
        self.video_path, self.srt_path = "", ""
        self.lab = SubtitleLabel("Vous pourrez Voire et retranscrire Vos Videos")        
        hbox.addWidget(self.lab), hbox.addWidget(ico)
        self.box.addStretch(1), ico.setFixedSize(QSize(50, 50))
        self.lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(10, 10, 10, 10)
        self.central.addSpacing(30), self.central.addWidget(self.video)
        self.box.addLayout(hbox), self.box.addLayout(self.central)
        self.box.addSpacing(30)
        
        self.setStyleSheet(open("ui/style/settings.qss", 'r').read())
        setTheme(Theme.DARK)

        self.par = parent if parent != None else self


    #@Verification(type = "precision")
    def controle(self) :
        pass

    def get_params(self) :
        return {
            "horo_name" : self.video.name.text().strip(),
            "path_srt" : self.video.path_srt,
            "type" : self.video.typ.currentText(),
            "lang_dep" : self.video.lang_dep.currentText(),
            "lang_cible" : self.video.lang_cible.currentText(),
            "precision" : int(self.video.precision.text())
        }

        
    def champ_nr(self, name : str) :
        InfoBar.warning(
            "Champ non remplis",
            content = f"\nVous devez obligatoirement\nremplir le champ :\n{name}",
            isClosable = True,
            orient = Qt.Orientation.Horizontal,
            position= InfoBarPosition.TOP_RIGHT,
            parent = self.par,
            duration = 5000
        )
    def select_nr(self, name : str) :
        InfoBar.warning(
            "Sélection vide",
            content = f"\nVeuillez sélectionner le\n{name}",
            isClosable = True,
            orient = Qt.Orientation.Horizontal,
            position= InfoBarPosition.TOP_RIGHT,
            parent = self.par,
            duration = 5000
        )
    def connexion_slots(self) :
        InfoBar.info(
            "Connexion Echouée",
            "Connecté vous au serveur",
            duration  = 3000,
            position = InfoBarPosition.TOP_RIGHT,
            parent = self.par
        )

    def status_video_slots(self, status : int) : 
        if status != 200 :
            InfoBar.success(
                "Erreur envoie Vidéo.",
                "Erreur lors de l'envoie de la\n vidéo dns le serveur...",
                duration = 3000,
                position = InfoBarPosition.TOP_RIGHT,
                parent = self.par
            )

    def status_slots(self, status : int) :
        if status == 200 :
            InfoBar.success(
                "Retranscription Réussie.",
                "Votre Retranscription a\nété éffectué avec succès.",
                duration = 5000,
                position = InfoBarPosition.TOP_RIGHT,
                parent = self.par
            )
        if status == 404 :
            InfoBar.warning(
                "URL Non défini.",
                "L'url spécifié\n n'a pas été trouvé.",
                duration = 5000,
                position = InfoBarPosition.TOP_RIGHT,
                parent = self.par
            )
if __name__=='__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    win = Interface()
    win.show()
    app.exec()