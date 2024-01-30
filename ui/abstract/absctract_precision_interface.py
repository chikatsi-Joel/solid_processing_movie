from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import abc
from qfluentwidgets import *
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets.multimedia import SimpleMediaPlayBar, StandardMediaPlayBar, VideoWidget
        


class abstract_precision_interface(abc.ABC) :
    def __init__(self, **kwargs) :
        pass