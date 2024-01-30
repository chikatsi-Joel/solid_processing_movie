from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
import sys

from  ui.chat_interface import Message_Zone
from functools import singledispatchmethod


class View(QWidget) :
    @singledispatchmethod
    def __init__(self, args) :
        raise NotImplementedError
    
    @__init__.register(str)
    def _(self, args : str) :
        pass

    @__init__.register(int)
    def _(self, args : int) :
        pass
    
    @__init__.register(dict)
    def _(self, args) :
        super(View, self).__init__()

        self.resize(800, 500)

class barre_label(QFrame) :

    def __init__(self, **kwargs) : 
        super(barre_label, self).__init__(**kwargs)
        self.central = VBoxLayout(None)

        self.viewBox = VBoxLayout(None)

        self.level_1 = PushSettingCard(text = "Chat", icon = FIF.CHAT, title = "Chat", content = "Contactez l'administration")
        self.level_2 = PushSettingCard(text = "Start", icon = "ui/Images/shortcut.png", title = "SHORT", content = "Raccourci")
        self.level_3 = PushSettingCard(text = "Start", icon = FIF.BOOK_SHELF, title = "Manuel", content = "Manuel d'utilisation")
        self.level_4 = PushSettingCard(text = "Start", icon = FIF.CODE, title = "Developper", content = "Contacter le développeur")

        self.viewBox.addWidgets([self.level_1, self.level_2, self.level_3])
        self.central.addLayout(self.viewBox)

        self.central.addStretch()

        self.central.addWidget(self.level_4)

        setTheme(Theme.DARK)
        self.setObjectName("fme")
        #self.setFrameShadow(QFrame.Shadow.Raised)
        self.setFrameShape(QFrame.Shape.Box)


        self.setStyleSheet(open("ui/style/settings.qss", 'r').read())
        self.setFixedWidth(350)
        self.setLayout(self.central)



class help_interface(QWidget):
    @singledispatchmethod
    def __init__(self, args) :
        raise NotImplementedError
    
    @__init__.register(int)
    def _(self, value : int) :
        pass

    @__init__.register(dict)
    def _(self, params : dict = {}) :
        super(help_interface, self).__init__()

        self.central = QHBoxLayout(self)
        self.stack_container = QStackedWidget()
        self.barre_label = barre_label()

        self.short = QWidget()
        self.dev = QWidget()
        self.manuel = QWidget()
        self.chat = Message_Zone(self)

        self.central.addWidget(self.stack_container)
        self.central.addWidget(self.barre_label)

        self.stack_container.addWidget(self.chat)
        self.stack_container.addWidget(self.dev)
        self.stack_container.addWidget(self.short)
        self.stack_container.addWidget(self.manuel)

        self.barre_label.level_1.clicked.connect(lambda: self.stack_container.setCurrentWidget(self.chat))
        self.barre_label.level_2.clicked.connect(lambda: self.stack_container.setCurrentWidget(self.short))
        self.barre_label.level_3.clicked.connect(lambda: self.stack_container.setCurrentWidget(self.manuel))
        self.barre_label.level_4.clicked.connect(lambda: self.stack_container.setCurrentWidget(self.dev))

        setTheme(Theme.DARK)
        self.setStyleSheet(open("ui/style/settings.qss", 'r').read())
        self.resize(1000, 500)




if __name__=='__main__' :
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    video_str = help_interface()
    video_str.show()
    app.exec()
