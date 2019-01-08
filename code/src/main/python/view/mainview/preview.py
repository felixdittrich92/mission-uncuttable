from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon 
#from PyQt5 import QObject
import os

class PreviewView(QWidget):
    def __init__(self):
        super(PreviewView, self).__init__()
        path = os.path.abspath('src/main/python/view/mainview')
        path2 = os.path.abspath('src/main/icons/preview_buttons/svg/')

        uic.loadUi(os.path.join(path, 'form.ui'), self)
        playButton = self.findChild(QPushButton, "playButton")
        icon = QtGui.QPixmap(os.path.join(path2,'002-play-button.svg'))
        playButton.setIcon(QIcon(icon))

        