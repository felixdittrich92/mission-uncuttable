import sys
import os
import platform

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QGridLayout
from PyQt5.QtCore import QObject, QSize
from PIL import Image, ImageQt
from pathlib import Path
from pygame import mixer
import numpy as np
import cv2

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
            #picture.thumbnail(((100,100)), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element)[:20], self.listWidget)
            item.setToolTip(last_element)
            self.listWidget.setStatusTip(last_element)
            item.setIcon(icon)
        elif last_element.endswith('.mp4'):
            path = "/home/felix/Schreibtisch/softwareprojekt/mission-uncuttable/code/src/main/resources/base/images/files/"
            filename = "mp4logo.jpg"
            path_to_file = Path(path, filename)
            #ToDo path muss variabel über Einstellungen sein
            picture = Image.open(path_to_file)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element)[:20], self.listWidget)
            item.setToolTip(last_element)
            self.listWidget.setStatusTip(last_element)
            item.setIcon(icon)
        elif last_element.endswith('.mp3'):
            path = "/home/felix/Schreibtisch/softwareprojekt/mission-uncuttable/code/src/main/resources/base/images/files/"
            filename = "mp3logo.jpg"
            path_to_file = Path(path, filename)
            #ToDo path muss variabel über Einstellungen sein
            picture = Image.open(path_to_file)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element)[:20], self.listWidget)
            item.setToolTip(last_element)
            self.listWidget.setStatusTip(last_element)
            item.setIcon(icon)
        else:
            print("The datatype is not supported")
            pass

    def clearFileNames(self):

        self.listWidget.clear()

    def enterEvent(self, event):
        file_path = self.listWidget.statusTip()
        
        if file_path.endswith('.mp4'):
            cap = cv2.VideoCapture(str(file_path))

            while(cap.isOpened()):
                ret,frame = cap.read()
                #frame = cv2.resize(frame, (200,200))
                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()

        elif file_path.endswith('.mp3'):
            mixer.init()
            mixer.music.load(file_path) #pygame.error: Unrecognized music forma
            mixer.music.play()
        
        else:
            pass


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            print(event.mimeData().urls())
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
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


def main():
    app = QApplication(sys.argv)
    window = Filemanager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
