import sys
import os
import numpy as np
import cv2
import time

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QListWidget, QLabel, QPushButton, QListWidgetItem
from PyQt5.QtCore import QObject, QSize
from PIL import Image, ImageQt
from pathlib import Path
from config import Resources


class Filemanager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Resources.get_instance().files.filemanager, self)
        self.deleteButton = self.findChild(QObject,'pushButton_1')
        self.pickButton = self.findChild(QObject,'pushButton_2')
        self.clearButton = self.findChild(QObject,'pushButton_3')
        self.listWidget = self.findChild(QObject,'listWidget')
        self.listWidget.setDragEnabled(True)
        self.listWidget.setAcceptDrops(False)
        self.listWidget.setMouseTracking(True)
        self.listWidget.setIconSize(QSize(100,100))

        self.pickButton.clicked.connect(self.pickFileNames)
        self.clearButton.clicked.connect(self.clearFileNames)
        self.deleteButton.clicked.connect(self.remove)

        self.current_frame = 0
        self.file_list = []

    def pickFileNames(self):
        fileNames, _ = QFileDialog.getOpenFileNames(
            self,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                'Files ( *.png *.jpg *.mp3 *.wav *.mp4);;'
            )
        )

        self.addFileNames(fileNames)


    def addFileNames(self, fileNames):

        for file in fileNames:

            if file in self.file_list:
                print("The file exist")
                break

            if file.upper().endswith(('.JPG', '.PNG')):
                picture = Image.open(file)
                picture = picture.resize(((275,183)), Image.ANTIALIAS)
                icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
                item = QListWidgetItem(os.path.basename(file)[:20], self.listWidget)
                item.setIcon(icon)
                item.setToolTip(file)
                item.setStatusTip(file)
                self.file_list.append(file)

            elif file.upper().endswith(('.MP4')):
                path = Resources.get_instance().images.media_symbols
                video_input_path = file
                cap = cv2.VideoCapture(str(video_input_path))

                ret, frame = cap.read()
                if not ret:
                    break
                else:
                    cv2.imwrite(os.path.join(path, "video%d.jpg" % self.current_frame), frame)
                    filename = "video%d.jpg" % self.current_frame
                    self.current_frame += 1
                    preview_file = Path(path, filename)
                    time.sleep(0.5)
                cap.release()
                cv2.destroyAllWindows()

                picture = Image.open(preview_file)
                time.sleep(0.5)
                picture = picture.resize(((275,183)), Image.ANTIALIAS)
                icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
                item = QListWidgetItem(os.path.basename(file)[:20], self.listWidget)
                item.setToolTip(file)
                item.setStatusTip(file)
                item.setIcon(icon)
                self.file_list.append(file)

            elif file.upper().endswith(('.MP3', '*.WAV')):
                path = Resources.get_instance().images.media_symbols
                filename = "mp3logo.jpg"
                path_to_file = Path(path, filename)
                picture = Image.open(path_to_file)
                picture = picture.resize(((275,183)), Image.ANTIALIAS)
                icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
                item = QListWidgetItem(os.path.basename(file)[:20], self.listWidget)
                item.setIcon(icon)
                item.setToolTip(file)
                item.setStatusTip(file)
                self.file_list.append(file)

            else:
                print("The datatype is not supported")
                pass

    def clearFileNames(self, fileNames):
        self.listWidget.clear()
        self.file_list.clear()

    def remove(self):
        x = self.listWidget.currentItem().statusTip()
        print(x) #String for drag&drop ??
        self.file_list.remove(x)
        self.listWidget.takeItem(self.listWidget.currentRow())
        

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