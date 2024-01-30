from PyQt5.QtGui import QDragMoveEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, datetime
from qfluentwidgets.components import *
from qfluentwidgets.common import setTheme, Theme
from qframelesswindow import AcrylicWindow
from qfluentwidgets import FluentIcon as FIF




class ZoneMessage(QFrame) :
    def __init__(self, parent : QWidget | None = None) :
        super(ZoneMessage, self).__init__(parent)
        self.vbox = QVBoxLayout(self)
        self.scroll_areea = SmoothScrollArea()
        self.scroll_widget = QWidget()
        self.container = VBoxLayout(self.scroll_widget)

        self.setFrameShape(QFrame.Shape.Panel)

        self.setObjectName("zone_mess")
        self.scroll_areea.setWidgetResizable(True)


        self.scroll_areea.setWidget(self.scroll_widget)
    
        self.vbox.addWidget(self.scroll_areea)
        
        self.scroll_widget.setFixedHeight(self.container.sizeHint().height())
        self.scroll_widget.setFixedWidth(self.width() * 3 // 4)


        self.setFixedHeight(400), self.scroll_widget.setFixedWidth(self.width())

    def add_widget(self, mess: str, type : str = 'user'):
        sep = HorizontalSeparator(self)
        self.container.addSpacerItem(QSpacerItem(30, 90))
        self.container.addWidget(SubtitleLabel("ADMINISTRATION" if type == 'admin' else "Vous"))
        self.container.addWidget(sep)
        self.container.addWidget(lab := BodyLabel(mess + f"\n\n\t\t\t\t\t\t\t{datetime.datetime.now().strftime("%H:%M")}"))
        lab.setWordWrap(True)
        lab.setFixedWidth(500)
        if type == 'user' :
            lab.setStyleSheet("background-color: rgb(49, 49, 49);  padding: 20px; border-radius: 10px;")
        else :
            lab.setStyleSheet("background-color: rgb(133, 133, 135); padding: 20px; border-radius: 10px;")

        self.scroll_widget.setMinimumSize(self.scroll_widget.sizeHint())
        self.scroll_areea.verticalScrollBar().setValue(self.scroll_areea.verticalScrollBar().maximum())

class Zone_Saisie(QWidget) :
    def __init__(self, parent : QWidget | None = None) :
        super(Zone_Saisie, self).__init__(parent)
        self.central = QHBoxLayout(self)
        self.writable = PlainTextEdit()
        
        self.writable.setFixedHeight(80)
        self.central.addWidget(self.writable)


class Message_Zone(QWidget) :
    def __init__(self, parent : QWidget | None = ...) :
        super(Message_Zone, self).__init__()
        self.central = VBoxLayout(self)
        self.entete = TitleLabel("Zone de Chat", self)

        self.zone_message = ZoneMessage()
        self.zone_saisie = Zone_Saisie()

        self.central.addWidget(self.entete, 0, Qt.AlignmentFlag.AlignCenter)
        self.central.addWidget(self.zone_message)
        self.central.addWidget(self.zone_saisie)

        self.central.setSpacing(20)

        setTheme(Theme.DARK)
        
    def sendMessage(self) :
        text = self.zone_saisie.writable.toPlainText()
        self.zone_message.add_widget(text)

        
 
class Chat(QWidget) :
    def __init__(self, parent : QWidget | None = ..., **kwargs) :
        super(Chat, self).__init__(parent = parent, **kwargs)
        self.central = VBoxLayout(self)

        self.title = TitleLabel("Bienvenue dans la partie Chat")
        
        
if __name__ == '__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    #win = Pres("Images/moi.png", "Presentation", "je suis un putain de programmeur")
    win = Message_Zone()
    win.show()
    app.exec()