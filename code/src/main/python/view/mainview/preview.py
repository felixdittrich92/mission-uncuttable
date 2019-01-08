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
        firstframeButton = self.findChild(QPushButton, "firstframeButton")
        lastframeButton = self.findChild(QPushButton, "lastframeButton")
        backButton = self.findChild(QPushButton, "backButton")
        forwardButton = self.findChild(QPushButton, "forwardButton")

        iconplay = QtGui.QPixmap(os.path.join(path2,'002-play-button.svg'))
        iconfirstframe = QtGui.QPixmap(os.path.join(path2,'006-back.svg'))
        iconlastframe = QtGui.QPixmap(os.path.join(path2,'007-next-1.svg'))
        iconback = QtGui.QPixmap(os.path.join(path2,'013-previous.svg'))
        iconforward = QtGui.QPixmap(os.path.join(path2,'004-next.svg'))
        
        playButton.setIcon(QIcon(iconplay))
        firstframeButton.setIcon(QIcon(iconfirstframe))
        lastframeButton.setIcon(QIcon(iconlastframe))
        backButton.setIcon(QIcon(iconback))
        forwardButton.setIcon(QIcon(iconforward))


        