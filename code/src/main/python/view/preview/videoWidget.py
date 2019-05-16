from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui
from PyQt5.QtGui import *
from config import Resources
from PyQt5.QtCore import QObject, QMutex, Qt, QRect
import openshot
import sip
from model.data import TimelineModel
import time

class VideoWidget(QWidget):
    def __init__(self, *args):
        # Invoke parent init
        QWidget.__init__(self, *args)

        # Init aspect ratio, pixel ratio
        self.aspect_ratio = openshot.Fraction()
        self.pixel_ratio = openshot.Fraction()
        self.aspect_ratio.num = 16
        self.aspect_ratio.den = 9
        self.pixel_ratio.num = 1
        self.pixel_ratio.den = 1

        # set view properties
        super().setAttribute(Qt.WA_OpaquePaintEvent)
        super().setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        # Init current frame's QImage
        self.current_image = None

    def present(self, image, *args):
        """ Update current image """

        # Get frame's QImage from libopenshot
        self.current_image = image

        # Force repaint on this widget
        self.repaint()

    def connectSignals(self, renderer):
        """ Connect signal present from renderer to method present """
        renderer.present.connect(self.present)

    def paintEvent(self, event, *args):
        """ Custom paint event (repaint)"""

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

    def centeredViewport(self, width, height):
        """ Calculate size of viewport to maintain apsect ratio """

        aspectRatio = self.aspect_ratio.ToFloat() * self.pixel_ratio.ToFloat()
        heightFromWidth = width / aspectRatio
        widthFromHeight = height * aspectRatio

        if heightFromWidth <= height:
            return QRect(0, (height - heightFromWidth) / 2, width, heightFromWidth)
        else:
            return QRect((width - widthFromHeight) / 2.0, 0, widthFromHeight, height)
