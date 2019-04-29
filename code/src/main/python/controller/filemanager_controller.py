import sys
import os
import numpy as np
import cv2

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QGridLayout
from PyQt5.QtCore import QObject, QSize
from PIL import Image, ImageQt
from pathlib import Path
import subprocess
from ffmpy import FFmpeg

from config import Resources


class Filemanager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Resources.get_instance().files.filemanager, self)
        self.pickButton = self.findChild(QObject,'pushButton_2')
        self.clearButton = self.findChild(QObject,'pushButton_3')
        self.listWidget = self.findChild(QObject,'listWidget')
        self.listWidget.setDragEnabled(True)
        self.listWidget.setAcceptDrops(False)
        self.listWidget.setMouseTracking(True)
        self.listWidget.setIconSize(QSize(100,100))

        self.pickButton.clicked.connect(self.pickFileNames)
        self.clearButton.clicked.connect(self.clearFileNames)

        self.current_frame = 0


    def pickFileNames(self):
        fileNames, _ = QFileDialog.getOpenFileNames(
            self,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                'All Files (*);;'
                'Image Files (*.png);;'
                'Sound Files(*.mp3);;'
                'Movie Files (*.mp4)'
            )
        )

        self.addFileNames(fileNames)

    def addFileNames(self, fileNames):
        last_element = fileNames[-1]

        if last_element.endswith(('.jpg','.JPEG', '.jpeg', '.JPG','.png', '.PNG')):
            picture = Image.open(last_element)
            picture = picture.resize(((275,183)), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element)[:20], self.listWidget)
            item.setIcon(icon)
            item.setToolTip(last_element)
            item.setStatusTip(last_element)
        elif last_element.endswith(('.mp4', '.MP4')):
            path = Resources.get_instance().images.media_symbols
            video_input_path = last_element
            cap = cv2.VideoCapture(str(video_input_path))

            frame = 0
            while (True):
                ret, frame = cap.read()
                if not ret or frame == 1:
                    break
                else:
                    cv2.imwrite(os.path.join(path, "video%d.jpg" % self.current_frame), frame)
                    filename = "video%d.jpg" % self.current_frame
                    self.current_frame += 1
                    frame += 1
            cap.release()
            cv2.destroyAllWindows()

            path_to_file = Path(path, filename)
            picture = Image.open(path_to_file)
            picture = picture.resize(((275,183)), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element)[:20], self.listWidget)
            item.setToolTip(last_element)
            item.setStatusTip(last_element)
            item.setIcon(icon)
        elif last_element.endswith(('.mp3', '.MP3')):
            path = Resources.get_instance().images.media_symbols
            print(path)
            filename = "mp3logo.jpg"
            path_to_file = Path(path, filename)
            picture = Image.open(path_to_file)
            picture = picture.resize(((275,183)), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element)[:20], self.listWidget)
            item.setIcon(icon)
            item.setToolTip(last_element)
            item.setStatusTip(last_element)

        else:
            print("The datatype is not supported")
            pass

    def clearFileNames(self):

        self.listWidget.clear()

    #def enterEvent(self, event):
     #   file_path = self.picture.statusTip()
     #   print(file_path)   


"""
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            print(event.mimeData().urls())
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction) 
            event.accept()
            l  = []
            for url in event.mimeData().urls():
                l.append(str(url.toLocalFile()))
            self.emit(SIGNAL("dropped"),l)
        else:
            event.ignore()  
    
    #self.connect(self.timeview, SIGNAL("dropped"), self.fileDropped)

    #def fileDropped(self, l):
    #    file = l[-1]

    #    if file.endswith(('.jpg','.JPEG', '.jpeg', '.JPG','.png', '.PNG')):
    #        addClip()
    #    elif file.endswith('.mp4'):
    #        addClip()
    #    elif file.endswith('.mp3'):
    #        addClip()
    #    else:
    #        pass
"""

def main():
    app = QApplication(sys.argv)
    window = Filemanager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
