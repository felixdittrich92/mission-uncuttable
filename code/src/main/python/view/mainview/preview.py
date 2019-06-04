from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QSize
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
        uic.loadUi(Resources.files.preview_view, self)

        play_button = self.findChild(QPushButton, "play_button")
        first_frame_button = self.findChild(QPushButton, "first_frame_button")
        last_frame_button = self.findChild(QPushButton, "last_frame_button")
        back_button = self.findChild(QPushButton, "back_button")
        forward_button = self.findChild(QPushButton, "forward_button")
        maximize_button = self.findChild(QPushButton, "maximize_button")

        icon_play = QPixmap(Resources.images.play_button)
        icon_pause = QPixmap(Resources.images.pause_button)
        icon_firstframe = QPixmap(Resources.images.first_frame_button)
        icon_lastframe = QPixmap(Resources.images.last_frame_button)
        icon_back = QPixmap(Resources.images.back_button)
        icon_forward = QPixmap(Resources.images.forward_button)
        icon_max = QPixmap(Resources.images.maximize_button)
    
        play_button.setIcon(QIcon(icon_play))
        play_button.setIconSize(QSize(32, 32))
        first_frame_button.setIcon(QIcon(icon_firstframe))
        first_frame_button.setIconSize(QSize(24, 24))
        last_frame_button.setIcon(QIcon(icon_lastframe))
        last_frame_button.setIconSize(QSize(24, 24))
        back_button.setIcon(QIcon(icon_back))
        back_button.setIconSize(QSize(20, 20))
        forward_button.setIcon(QIcon(icon_forward))
        forward_button.setIconSize(QSize(20, 20))
        maximize_button.setIcon(QIcon(icon_max))
        maximize_button.setIconSize(QSize(32, 32))

        self.videoLabel = self.findChild(QLabel, "video_label")

        # FÜR DEVELOPMENT
        img = QPixmap(Resources.images.bunny)
        self.videoLabel.setPixmap(img)

        self.videoLabel.move(280, 120)
        self.videoLabel.resize(960, 720)
        # th = Thread(self)
        # th.changePixmap.connect(self.setImage)
        # th.start()

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
