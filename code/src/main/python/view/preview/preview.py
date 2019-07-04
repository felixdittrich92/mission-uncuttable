from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from config import Resources
from PyQt5.QtCore import QObject, QCoreApplication, pyqtSignal, QPoint, Qt
from model.data import TimelineModel
from controller import TimelineController
from .videoWidget import VideoWidget
from util.timeline_utils import get_px_per_second
from threading import Thread
import openshot
import sip
import time
from ..view import View
from config import Settings
from util.classmaker import classmaker

class PreviewView(classmaker(QWidget, View)):

    """
    QWidget for Previewplayer
    """
    frame_changed = pyqtSignal(QPoint)
    needle_moved = pyqtSignal(int)

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

        # self.init_stylesheet()
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

    def init_stylesheet(self):
        current_stylesheet = Settings.get_instance().get_settings().design.color_theme.current
        if current_stylesheet == 0:
            self.setStyleSheet(open(Resources.files.qss_dark, "r").read())     
        elif current_stylesheet == 1:
            self.setStyleSheet(open(Resources.files.qss_light, "r").read())
            
    
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

        # set cursor to buttons
        self.play_button.setCursor(Qt.PointingHandCursor)
        self.first_frame_button.setCursor(Qt.PointingHandCursor)
        self.last_frame_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.forward_button.setCursor(Qt.PointingHandCursor)
        self.maximize_button.setCursor(Qt.PointingHandCursor)
        self.progress_slider.setCursor(Qt.PointingHandCursor)

        #connect events
        self.play_button.clicked.connect(self.play_pause)
        self.first_frame_button.clicked.connect(self.first_frame)
        self.last_frame_button.clicked.connect(self.last_frame)
        self.back_button.pressed.connect(self.prev_frame)
        self.back_button.released.connect(self.stop_loop)
        self.forward_button.pressed.connect(self.next_frame)
        self.forward_button.released.connect(self.stop_loop)
        self.progress_slider.sliderMoved.connect(self.change_progress_bar)
        self.looprunning = False

        #set Widget into Layout
        self.video_layout.layout().insertWidget(0, self.videoWidget)

    def playing(self):
        """Thread that moves the needle, when Player is playing."""
        while self.video_running:
            current_frame = self.player.Position()
            new_position = (current_frame * get_px_per_second()) \
                / TimelineModel.get_instance().get_fps()
            self.update_time_label()
            self.progress_slider.setValue(current_frame)
            self.frame_changed.emit(QPoint(new_position, 0))

            time.sleep(0.1)

    def play_pause(self):
        self.progress_slider.setMaximum(self.get_last_frame())
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

    def stop(self):
        if self.video_running:
            self.play_pause()

    def first_frame(self):
        self.update_player()
        self.player.Seek(1)
        self.frame_changed.emit(QPoint(0, 0))
        self.update_progress_bar()
        self.update_time_label()

    def last_frame(self):
        self.update_player()
        self.player.Seek(self.get_last_frame())
        self.player.Pause()
        self.play_button.setIcon(QIcon(self.iconplay))
        new_position = (self.player.Position() * get_px_per_second()) \
            / TimelineModel.get_instance().get_fps()
        self.frame_changed.emit(QPoint(new_position, 0))
        self.update_progress_bar()
        self.update_time_label()

    def get_last_frame(self):
        last_frame = 0
        for c in self.timeline.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * self.timeline.info.fps.ToFloat()) + 1

        return last_frame

    def prev_frame(self):
        self.update_player()
        position = self.player.Position()
        new_position = position - 1
        self.player.Seek(new_position)
        new_position = (new_position * get_px_per_second()) \
            / TimelineModel.get_instance().get_fps()
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
            new_position = (new_position * get_px_per_second()) \
                / TimelineModel.get_instance().get_fps()
            self.frame_changed.emit(QPoint(new_position, 0))
            self.update_time_label()
            self.update_progress_bar()
        self.update_time_label()
        self.update_progress_bar()

    def stop_loop(self):
        self.looprunning = False

    def next_frame(self):
        self.update_player()
        position = self.player.Position()
        new_position = position + 1
        self.player.Seek(new_position)
        new_position = (new_position * get_px_per_second()) \
            / TimelineModel.get_instance().get_fps()
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
            new_position = (new_position * get_px_per_second()) \
                / TimelineModel.get_instance().get_fps()
            self.frame_changed.emit(QPoint(new_position, 0))
            self.update_progress_bar()
            self.update_time_label()
        self.update_time_label()
        self.update_progress_bar()

    def set_player_to_frame(self, frame):
        self.player.Seek(frame)

    def change_progress_bar(self):
        self.player.Seek(self.progress_slider.value())
        new_position = (self.player.Position() * get_px_per_second()) / TimelineModel.get_instance().get_fps()
        self.update_time_label()

        self.frame_changed.emit(QPoint(new_position, 0))

    def update_progress_bar(self):
        self.progress_slider.setValue(self.player.Position())

    def update_time_label(self):
        current_frame = (self.player.Position() - 1)
        num_of_frames = (self.get_last_frame() - 1)
        frame_second = str(int(current_frame % TimelineModel.get_instance().get_fps()))
        global_frame_seconds = str(int(num_of_frames % TimelineModel.get_instance().get_fps()))
        if (num_of_frames % TimelineModel.get_instance().get_fps()) >= 10:
            None
        else:
            global_frame_seconds = str("0"+global_frame_seconds)
        if (current_frame % TimelineModel.get_instance().get_fps()) >= 10:
            None
        else:
            frame_second = str("0"+frame_second)
        current_time = str(time.strftime('%H:%M:%S', time.gmtime((1 / TimelineModel.get_instance().get_fps()) * current_frame)))
        num_of_time = str(time.strftime('%H:%M:%S', time.gmtime((1 / TimelineModel.get_instance().get_fps()) * num_of_frames)))
        timecode = (current_time + ":" + frame_second + " | " + num_of_time + ":" + global_frame_seconds)
        timecode_timeline = (current_time + ":" + frame_second)
        self.current_time_label.setText(timecode)
        TimelineController.get_instance().update_timecode(timecode_timeline)

    def update_player(self):
        if self.video_running:
            self.player.Pause()
            self.player.Play()
        else:
            self.player.Play()
            self.player.Pause()

    def update_information(self):
        self.update_player()
        self.update_progress_bar()
        self.update_time_label()

    def refresh(self):
        self.update()
