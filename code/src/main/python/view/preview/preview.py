from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from config import Resources
from PyQt5.QtCore import QObject, QCoreApplication, pyqtSignal, QPoint
from model.data import TimelineModel
from .videoWidget import VideoWidget
from threading import Thread

import openshot
import sip
import time

FRAMES_PER_SECOND = 25
SECONDS_PER_PIXEL = 16


class PreviewView(QWidget):
    """
    QWidget for Previewplayer
    """
    frame_changed = pyqtSignal(QPoint)

    __instance = None
    @staticmethod
    def get_instance():
        if PreviewView.__instance is None:
            PreviewView()
        return PreviewView.__instance

    def __init__(self):

        if PreviewView.__instance is not None:
            raise Exception("singleton")
        else:
            PreviewView.__instance = self

        #init qwidget, resources, ui file
        super(PreviewView, self).__init__()
        uic.loadUi(Resources.files.preview_view, self)

        self.video_running = False

        #get timelinemlodel, timeline
        tm = TimelineModel.get_instance()
        self.timeline = tm.getTimeline()

        #init Openshot Player
        self.player = openshot.QtPlayer()

        #init videoWidget
        self.videoWidget = VideoWidget()
        self.videoWidget.setObjectName("video_widget")

        #get renderer and renderer adress form QtPlayer
        self.renderer_address = self.player.GetRendererQObject()
        self.renderer = sip.wrapinstance(self.renderer_address, QObject)

        #get adress from videoWidget
        self.player.SetQWidget(sip.unwrapinstance(self.videoWidget))

        #connect signals of videoWidget and renderer
        self.videoWidget.connectSignals(self.renderer)


        #load timline into reader
        self.player.Reader(self.timeline)

        #init GUI
        self.initGUI()

    def initGUI(self):
        #load icons
        self.iconplay = QtGui.QPixmap(Resources.images.play_button)
        self.iconpause = QtGui.QPixmap(Resources.images.pause_button)
        iconfirstframe = QtGui.QPixmap(Resources.images.first_frame_button)
        iconlastframe = QtGui.QPixmap(Resources.images.last_frame_button)
        iconback = QtGui.QPixmap(Resources.images.back_button)
        iconforward = QtGui.QPixmap(Resources.images.forward_button)
        iconmax = QtGui.QPixmap(Resources.images.maximize_button)

        #set icons to buttons
        self.play_button.setIcon(QIcon(self.iconplay))
        self.first_frame_button.setIcon(QIcon(iconfirstframe))
        self.last_frame_button.setIcon(QIcon(iconlastframe))
        self.back_button.setIcon(QIcon(iconback))
        self.forward_button.setIcon(QIcon(iconforward))
        self.maximize_button.setIcon(QIcon(iconmax))

        #connect events
        self.play_button.clicked.connect(self.play_pause)
        self.first_frame_button.clicked.connect(self.firstFrame)
        self.last_frame_button.clicked.connect(self.lastFrame)
        self.back_button.pressed.connect(self.prevFrame)
        self.back_button.released.connect(self.stopLoop)
        self.forward_button.pressed.connect(self.nextFrame)
        self.forward_button.released.connect(self.stopLoop)
        self.progress_slider.valueChanged.connect(self.valuechange)
        self.looprunning = False
        # self.volumeSlider.valueChanged.connect(self.volumeChange)

        #set Widget into Layout
        self.video_layout.layout().insertWidget(0, self.videoWidget)

        self.current_frame_label = self.findChild(QWidget, "current_frame_label")

    def playing(self):
        """Thread that moves the needle, when Player is playing."""
        while self.video_running:
            current_frame = self.player.Position()
            self.current_frame_label.setText(str(current_frame))
            new_position = (current_frame * SECONDS_PER_PIXEL) / FRAMES_PER_SECOND
            self.frame_changed.emit(QPoint(new_position, 0))

            time.sleep(0.1)

    def play_pause(self):
        playing_thread = Thread(target=self.playing)

        if self.video_running:
            self.player.Pause()
            self.video_running = False
            self.play_button.setIcon(QIcon(self.iconplay))

        else:
            self.player.Play()
            self.video_running = True
            self.play_button.setIcon(QIcon(self.iconpause))
            playing_thread.start()

    def firstFrame(self):
        self.player.Seek(1)
        self.frame_changed.emit(QPoint(0, 0))

        self.current_frame_label.setText(str(self.player.Position()))

    def lastFrame(self):
        self.player.Seek(self.getlastFrame())
        new_position = (self.player.Position() * SECONDS_PER_PIXEL) / FRAMES_PER_SECOND
        self.frame_changed.emit(QPoint(new_position, 0))

        self.current_frame_label.setText(str(self.player.Position()))


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
        new_position = position - 1
        self.player.Seek(new_position)
        new_position = (new_position * SECONDS_PER_PIXEL) / FRAMES_PER_SECOND
        self.frame_changed.emit(QPoint(new_position, 0))
        self.looprunning = True
        while True:
            time.sleep(0.1)
            QCoreApplication.processEvents()
            if self.looprunning == False:
                break
            position = self.player.Position()
            new_position = position - 10
            self.player.Seek(new_position)
            new_position = (new_position * SECONDS_PER_PIXEL) / FRAMES_PER_SECOND
            self.frame_changed.emit(QPoint(new_position, 0))

            self.current_frame_label.setText(str(self.player.Position()))
        self.current_frame_label.setText(str(self.player.Position()))

    def stopLoop(self):
        self.looprunning = False

    def nextFrame(self):
        position = self.player.Position()
        new_position = position + 1
        self.player.Seek(new_position)
        new_position = (new_position * SECONDS_PER_PIXEL) / FRAMES_PER_SECOND
        self.frame_changed.emit(QPoint(new_position, 0))
        self.looprunning = True
        while True:
            time.sleep(0.1)
            QCoreApplication.processEvents()
            if self.looprunning == False:
                break
            position = self.player.Position()
            new_position = position + 10
            self.player.Seek(new_position)
            new_position = (new_position * SECONDS_PER_PIXEL) / FRAMES_PER_SECOND
            self.frame_changed.emit(QPoint(new_position, 0))

            self.current_frame_label.setText(str(self.player.Position()))
        self.current_frame_label.setText(str(self.player.Position()))

    def set_player_to_frame(self, frame):
        self.player.Seek(frame)
        print(frame)

    # def volumeChange(self):
    #     slicerValue = self.volumeSlider.value()/10
    #     print(slicerValue)
    #     self.player.Volume(slicerValue)
    #     print(self.player.Volume())

class ThreadProgress(QThread):
    def __init__(self):
        QThread.__init__(self)
    
    def __del__(self):
        self.wait

    def run(self):
        self.updateProgress()

    def updateProgress(self):
        self.progress_slider.setValue(self.player.Position())        