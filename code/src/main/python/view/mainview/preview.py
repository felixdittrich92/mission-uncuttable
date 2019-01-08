from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon 
#from PyQt5 import QObject
import os

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtCore import Qt
import sys

import cv2 
import numpy



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

        self.label = QLabel(self)
        self.label.move(280, 120)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @pyqtSlot(QImage)
    def setImage(self, image):
       self.label.setPixmap(QPixmap.fromImage(image))

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture('./video.mp4')
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


        