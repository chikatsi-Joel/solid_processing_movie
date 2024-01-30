from Admin.components.diagramme_circulaire_interface import diagramme_circulaire_interface
from components.utils import color as col
from qfluentwidgets import *
import sys
from PyQt5.QtWidgets import *


class windows(FluentWindow) :
    def __init__(self) :
        super(windows, self).__init__()

        self.circulaire_1 = diagramme_circulaire_interface(
            [90, 12, 89, 30, 1289],
            colors = col.get_color(5),
            names_regions = ['Pain', 'Parpin', 'Fer', 'Puce', 'Ordianteur']
        )
        self.circulaire_1.set_legende_title("Diagramme des Achats Pop")
        self.circulaire_1.setObjectName("circl")
        self.addSubInterface(
            interface = self.circulaire_1,
            icon = FluentIcon.GITHUB,
            text = "circle"
        )
    
if __name__ == '__main__' :
    app = QApplication(sys.argv)
    win = windows()
    win.show()
    app.exec()
