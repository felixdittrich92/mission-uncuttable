from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from config import Resources
from PyQt5.QtCore import QObject, QMutex, Qt, QRect
import openshot
import sip
from model.project import TimelineModel
import time

class PreviewView(QWidget):

    def __init__(self):
        self.video_running = False
        super(PreviewView, self).__init__()
        RESOURCES = Resources.get_instance()
        uic.loadUi(RESOURCES.files.preview_view, self)

        playButton = self.findChild(QPushButton, "playButton")
        firstframeButton = self.findChild(QPushButton, "firstframeButton")
        lastframeButton = self.findChild(QPushButton, "lastframeButton")
        backButton = self.findChild(QPushButton, "backButton")
        forwardButton = self.findChild(QPushButton, "forwardButton")
        maxButton = self.findChild(QPushButton, "fullScreen")

        iconplay = QtGui.QPixmap(RESOURCES.images.play_button)
        iconpause = QtGui.QPixmap(RESOURCES.images.pause_button)
        iconfirstframe = QtGui.QPixmap(RESOURCES.images.first_frame_button)
        iconlastframe = QtGui.QPixmap(RESOURCES.images.last_frame_button)
        iconback = QtGui.QPixmap(RESOURCES.images.back_button)
        iconforward = QtGui.QPixmap(RESOURCES.images.forward_button)
        iconmax = QtGui.QPixmap(RESOURCES.images.max_button)
    
        playButton.setIcon(QIcon(iconplay))
        firstframeButton.setIcon(QIcon(iconfirstframe))
        lastframeButton.setIcon(QIcon(iconlastframe))
        backButton.setIcon(QIcon(iconback))
        forwardButton.setIcon(QIcon(iconforward))
        maxButton.setIcon(QIcon(iconmax))

        playButton.clicked.connect(self.play_pause)
        '''
        firstframeButton.clicked.connect(self.firstFrame)
        lastframeButton.clicked.connect(self.lastFrame)        
        backButton.clicked.connect(self.back)
        forwardButton.clicked.connect(self.forward)
        '''

        tm = TimelineModel.get_instance()
        timeline = tm.getTimeline()
        self.player = openshot.QtPlayer()
        # test = self.player.GetRendererQObject()

        self.videoWidget = VideoWidget()
        self.renderer_address = self.player.GetRendererQObject()
        self.player.SetQWidget(sip.unwrapinstance(self.videoWidget))
        self.renderer = sip.wrapinstance(self.renderer_address, QObject)
        self.player.Reader(timeline)
        self.videoWidget.connectSignals(self.renderer)

        self.videoLayout.layout().insertWidget(0, self.videoWidget)

        
    def play_pause(self):
        from config import Resources
        if self.video_running:
            self.player.Pause()
            self.video_running = False
        else:   
            self.player.Play()
            self.video_running = True

class VideoWidget(QWidget):
    def __init__(self, *args):
    # Invoke parent init
        QWidget.__init__(self, *args)
        self.aspect_ratio = openshot.Fraction()
        self.pixel_ratio = openshot.Fraction()
        self.aspect_ratio.num = 16
        self.aspect_ratio.den = 9
        self.pixel_ratio.num = 1
        self.pixel_ratio.den = 1
    
        # Init Qt style properties (black background, etc...)
        # p = QPalette()
        # p.setColor(QPalette.Window, QColor("#ff0000"))
        # super().setPalette(p)
        super().setAttribute(Qt.WA_OpaquePaintEvent)
        super().setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Init current frame's QImage
        self.current_image = None
   
    def present(self, image, *args):

        # Get frame's QImage from libopenshot
        self.current_image = image

        # Force repaint on this widget
        self.repaint()
        

    def connectSignals(self, renderer):
        """ Connect signals to renderer """
        renderer.present.connect(self.present)

    def paintEvent(self, event, *args):
        
        """ Custom paint event """


        # Paint custom frame image on QWidget
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing, True)

        # Fill background black
        painter.fillRect(event.rect(), self.palette().window())

        if self.current_image:
            # DRAW FRAME
            # Calculate new frame image size, maintaining aspect ratio
            pixSize = self.current_image.size()
            pixSize.scale(event.rect().size(), Qt.KeepAspectRatio)

            # Scale image
            scaledPix = self.current_image.scaled(pixSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Calculate center of QWidget and Draw image
            center = self.centeredViewport(self.width(), self.height())
            # painter.drawImage(center, scaledPix)
            painter.drawImage(center, self.current_image)

       
        # End painter
        painter.end()

        # self.mutex.unlock()
 

    def centeredViewport(self, width, height):
        """ Calculate size of viewport to maintain apsect ratio """

        aspectRatio = self.aspect_ratio.ToFloat() * self.pixel_ratio.ToFloat()
        heightFromWidth = width / aspectRatio
        widthFromHeight = height * aspectRatio

        if heightFromWidth <= height:
            return QRect(0, (height - heightFromWidth) / 2, width, heightFromWidth)
        else:
            return QRect((width - widthFromHeight) / 2.0, 0, widthFromHeight, height)

