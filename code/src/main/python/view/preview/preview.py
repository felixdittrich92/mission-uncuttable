from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from config import Resources
from PyQt5.QtCore import QObject, QMutex, Qt, QRect, QCoreApplication
import openshot
import sip
from model.project import TimelineModel
import time
from .videoWidget import VideoWidget

class PreviewView(QWidget):

    def __init__(self):
        self.video_running = False
        super(PreviewView, self).__init__()
        RESOURCES = Resources.get_instance()
        uic.loadUi(RESOURCES.files.preview_view, self)

        self.iconplay = QtGui.QPixmap(RESOURCES.images.play_button)
        self.iconpause = QtGui.QPixmap(RESOURCES.images.pause_button)
        iconfirstframe = QtGui.QPixmap(RESOURCES.images.first_frame_button)
        iconlastframe = QtGui.QPixmap(RESOURCES.images.last_frame_button)
        iconback = QtGui.QPixmap(RESOURCES.images.back_button)
        iconforward = QtGui.QPixmap(RESOURCES.images.forward_button)
        iconmax = QtGui.QPixmap(RESOURCES.images.max_button)
    
        self.playButton.setIcon(QIcon(self.iconplay))
        self.firstframeButton.setIcon(QIcon(iconfirstframe))
        self.lastframeButton.setIcon(QIcon(iconlastframe))
        self.backButton.setIcon(QIcon(iconback))
        self.forwardButton.setIcon(QIcon(iconforward))
        self.maxButton.setIcon(QIcon(iconmax))

        self.playButton.clicked.connect(self.play_pause)
        self.firstframeButton.clicked.connect(self.firstFrame)
        self.lastframeButton.clicked.connect(self.lastFrame)        
        self.backButton.pressed.connect(self.prevFrame)
        self.backButton.released.connect(self.stopLoop)        
        self.forwardButton.pressed.connect(self.nextFrame)
        self.forwardButton.released.connect(self.stopLoop)
        self.looprunning = False
        # self.volumeSlider.valueChanged.connect(self.volumeChange)

        tm = TimelineModel.get_instance()
        self.timeline = tm.getTimeline()
        self.player = openshot.QtPlayer()

        self.videoWidget = VideoWidget()
        self.renderer_address = self.player.GetRendererQObject()
        self.player.SetQWidget(sip.unwrapinstance(self.videoWidget))
        self.renderer = sip.wrapinstance(self.renderer_address, QObject)
        self.player.Reader(self.timeline)
        self.videoWidget.connectSignals(self.renderer)

        self.videoLayout.layout().insertWidget(0, self.videoWidget)

        
    def play_pause(self):
        from config import Resources
        if self.video_running:
            self.player.Pause()
            self.video_running = False
            self.playButton.setIcon(QIcon(self.iconplay))

        else:   
            self.player.Play()
            self.video_running = True
            self.playButton.setIcon(QIcon(self.iconpause))

    def firstFrame(self):
        self.player.Seek(1)

    def lastFrame(self):
        self.player.Play()
        self.player.Pause()
        self.player.Seek(self.getlastFrame())

    def stopLoop(self):
        self.looprunning = False

    def prevFrame(self):
        position = self.player.Position()
        self.player.Seek(position-1)
        self.looprunning = True
        while True:
            time.sleep(0.1)
            QCoreApplication.processEvents()
            if self.looprunning == False:
                break
            position = self.player.Position()
            self.player.Seek(position-5)

    def nextFrame(self):
        position = self.player.Position()
        self.player.Seek(position+1)
        self.looprunning = True
        while True:
            time.sleep(0.1)
            QCoreApplication.processEvents()
            if self.looprunning == False:
                break
            position = self.player.Position()
            self.player.Seek(position+5)
            



    def getlastFrame(self):
        
        last_frame = 0
        for c in self.timeline.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * self.timeline.info.fps.ToFloat()) + 1

        return last_frame

    # def volumeChange(self):
    #     slicerValue = self.volumeSlider.value()/10
    #     print(slicerValue)
    #     self.player.Volume(slicerValue)
    #     print(self.player.Volume())