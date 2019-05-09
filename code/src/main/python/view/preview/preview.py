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
    """
    QWidget for Previewplayer
    """
    
    def __init__(self):
        
        self.video_running = False
        
        #involve qwidget, resources, ui file
        super(PreviewView, self).__init__()
        self.RESOURCES = Resources.get_instance()
        uic.loadUi(self.RESOURCES.files.preview_view, self)

        #get timeline instance
        tm = TimelineModel.get_instance()
        self.timeline = tm.getTimeline()
        
        #init Openshot Player
        self.player = openshot.QtPlayer()

        #init videoWidget
        self.videoWidget = VideoWidget()

        #get renderer adress form QtPlayer
        self.renderer_address = self.player.GetRendererQObject()
        self.renderer = sip.wrapinstance(self.renderer_address, QObject)

        #give adress from videoWidget to QtPlayer
        self.player.SetQWidget(sip.unwrapinstance(self.videoWidget))
        self.player.Reader(self.timeline)

        #connect signals of videoWidget and renderer
        self.videoWidget.connectSignals(self.renderer)

        #init GUI
        self.initGUI()
        

    def initGUI(self):    
        #load icons
        self.iconplay = QtGui.QPixmap(self.RESOURCES.images.play_button)
        self.iconpause = QtGui.QPixmap(self.RESOURCES.images.pause_button)
        iconfirstframe = QtGui.QPixmap(self.RESOURCES.images.first_frame_button)
        iconlastframe = QtGui.QPixmap(self.RESOURCES.images.last_frame_button)
        iconback = QtGui.QPixmap(self.RESOURCES.images.back_button)
        iconforward = QtGui.QPixmap(self.RESOURCES.images.forward_button)
        iconmax = QtGui.QPixmap(self.RESOURCES.images.max_button)
    
        #set icons to buttons
        self.playButton.setIcon(QIcon(self.iconplay))
        self.firstframeButton.setIcon(QIcon(iconfirstframe))
        self.lastframeButton.setIcon(QIcon(iconlastframe))
        self.backButton.setIcon(QIcon(iconback))
        self.forwardButton.setIcon(QIcon(iconforward))
        self.maxButton.setIcon(QIcon(iconmax))

        #connect events 
        self.playButton.clicked.connect(self.play_pause)
        self.firstframeButton.clicked.connect(self.firstFrame)
        self.lastframeButton.clicked.connect(self.lastFrame)        
        self.backButton.pressed.connect(self.prevFrame)
        self.backButton.released.connect(self.stopLoop)        
        self.forwardButton.pressed.connect(self.nextFrame)
        self.forwardButton.released.connect(self.stopLoop)
        self.looprunning = False
        # self.volumeSlider.valueChanged.connect(self.volumeChange)

        self.videoLayout.layout().insertWidget(0, self.videoWidget)
    
    def play_pause(self):
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

    def getlastFrame(self):
        last_frame = 0
        for c in self.timeline.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * self.timeline.info.fps.ToFloat()) + 1

        return last_frame

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
            self.player.Seek(position-10)

    def stopLoop(self):
        self.looprunning = False

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
            self.player.Seek(position+10)           

    # def volumeChange(self):
    #     slicerValue = self.volumeSlider.value()/10
    #     print(slicerValue)
    #     self.player.Volume(slicerValue)
    #     print(self.player.Volume())