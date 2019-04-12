from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtCore import Qt
from config import Resources
import sys
import os

import cv2 
import numpy

VIDEORUNNING = False

class PreviewView(QWidget):
    def __init__(self):
        super(PreviewView, self).__init__()
        RESOURCES = Resources.get_instance()
        uic.loadUi(RESOURCES.files.preview_view, self)

        playButton = self.findChild(QPushButton, "playButton")
        firstframeButton = self.findChild(QPushButton, "firstframeButton")
        lastframeButton = self.findChild(QPushButton, "lastframeButton")
        backButton = self.findChild(QPushButton, "backButton")
        forwardButton = self.findChild(QPushButton, "forwardButton")

        iconplay = QtGui.QPixmap(RESOURCES.images.play_button)
        iconpause = QtGui.QPixmap(RESOURCES.images.pause_button)
        iconfirstframe = QtGui.QPixmap(RESOURCES.images.first_frame_button)
        iconlastframe = QtGui.QPixmap(RESOURCES.images.last_frame_button)
        iconback = QtGui.QPixmap(RESOURCES.images.back_button)
        iconforward = QtGui.QPixmap(RESOURCES.images.forward_button)
    
        playButton.setIcon(QIcon(iconplay))
        firstframeButton.setIcon(QIcon(iconfirstframe))
        lastframeButton.setIcon(QIcon(iconlastframe))
        backButton.setIcon(QIcon(iconback))
        forwardButton.setIcon(QIcon(iconforward))

        self.videoLabel = self.findChild(QLabel, "videoLabel")

        self.videoLabel.move(280, 120)
        self.videoLabel.resize(960, 720)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    @pyqtSlot(QImage)
    def setImage(self, image):
       self.videoLabel.setPixmap(QPixmap.fromImage(image))

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture('./video.mp4')
        while VIDEORUNNING:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
