from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from config import Resources

import openshot
from model.project import TimelineModel

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

        playButton.clicked.connect(self.play_pause)

        tm = TimelineModel.get_instance()
        self.player = openshot.QtPlayer()
        test = self.player.GetRendererQObject()
        print(test)
        # self.player.SetQWidget()
        self.player.SetSource("/home/valentin/Documents/Softwareprojekt/mission-uncuttable/code/video.mp4")
        
        
        
        '''
        firstframeButton.clicked.connect(self.firstFrame)
        lastframeButton.clicked.connect(self.lastFrame)        
        backButton.clicked.connect(self.back)
        forwardButton.clicked.connect(self.forward)
        '''

    def play_pause(self):
        self.player.Play()


