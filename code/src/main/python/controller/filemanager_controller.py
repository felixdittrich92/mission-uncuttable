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
from view.mainview import FileListView


class Filemanager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Resources.get_instance().files.filemanager, self)
        self.deleteButton = self.findChild(QObject, 'pushButton_1')
        self.pickButton = self.findChild(QObject, 'pushButton_2')
        self.clearButton = self.findChild(QObject, 'pushButton_3')
        self.listWidget = FileListView()
        old_list_widget = self.findChild(QObject, 'listWidget')
        self.layout().replaceWidget(old_list_widget, self.listWidget)
        old_list_widget.deleteLater()
        # self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        # self.listWidget.setDragEnabled(True)
        # self.listWidget.setAcceptDrops(False)
        # self.listWidget.setMouseTracking(True)
        self.listWidget.setIconSize(QSize(100, 100))

        self.pickButton.clicked.connect(self.pickFileNames)
        self.clearButton.clicked.connect(self.clearFileNames)
        self.deleteButton.clicked.connect(self.remove)
        self.listWidget.itemSelectionChanged.connect(self.selected)

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

        for file in fileNames:
            QApplication.processEvents()
            self.addFileNames(file)


    def addFileNames(self, file):

        if file in self.file_list:
            print("The file exist")
            return

        if file.upper().endswith(('.JPG', '.PNG')):
            picture = Image.open(file)
            QApplication.processEvents()
                
        elif file.upper().endswith(('.MP4')):
            path = Resources.get_instance().images.media_symbols
            video_input_path = file
            cap = cv2.VideoCapture(str(video_input_path))

            ret, frame = cap.read()
            if not ret:
                return
            else:
                cv2.imwrite(os.path.join(path, "video%d.jpg" % self.current_frame), frame)
                filename = "video%d.jpg" % self.current_frame
                self.current_frame += 1
                preview_file = Path(path, filename)
            cap.release()
            cv2.destroyAllWindows()

            picture = Image.open(preview_file)
            QApplication.processEvents()
                
        elif file.upper().endswith(('.MP3', '*.WAV')):
            path = Resources.get_instance().images.media_symbols
            filename = "mp3logo.jpg"
            path_to_file = Path(path, filename)
            picture = Image.open(path_to_file)
            QApplication.processEvents()
                
        else:
            print("The datatype is not supported")
            pass

        time.sleep(0.5)
        picture = picture.resize(((275,200)), Image.ANTIALIAS)
        QApplication.processEvents()
        icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
        item = QListWidgetItem(os.path.basename(file)[:20], self.listWidget)
        item.setIcon(icon)
        item.setToolTip(file)
        item.setStatusTip(file)
        self.file_list.append(file)

    def clearFileNames(self, fileNames):
        self.listWidget.clear()
        self.file_list.clear()

    def remove(self):
        try:
            path = self.listWidget.currentItem().statusTip()
            self.file_list.remove(path)
            self.listWidget.takeItem(self.listWidget.currentRow())
        except:
            return

    def selected(self):
        try:
            path = self.listWidget.currentItem().statusTip() #String
        except:
            return

def main():
    app = QApplication(sys.argv)
    window = Filemanager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
