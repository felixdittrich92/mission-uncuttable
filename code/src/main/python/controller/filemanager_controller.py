import sys
import os

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QGridLayout
from PyQt5.QtCore import QObject, QSize
from PIL import Image, ImageQt

from config import Resources


class Filemanager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Resources.get_instance().files.filemanager, self)
        self.pickButton = self.findChild(QObject,'pushButton_2')
        self.clearButton = self.findChild(QObject,'pushButton_3')
        self.listWidget = self.findChild(QObject,'listWidget')

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

        if last_element.endswith(('.jpg','.JPEG','.JPG','.png', '.PNG')):
            picture = Image.open(last_element)
            #picture.thumbnail(((100,100)), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element), self.listWidget)
            item.setStatusTip(last_element)
            item.setIcon(icon)
        elif last_element.endswith('.mp4'):
            filename = "/home/felix/Schreibtisch/softwareprojekt/mission-uncuttable/code/src/main/resources/base/images/files/mp4logo.jpg"
            #ToDo
            picture = Image.open(filename)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element), self.listWidget)
            item.setStatusTip(last_element)
            item.setIcon(icon)
        elif last_element.endswith('.mp3'):
            filename = "/home/felix/Schreibtisch/softwareprojekt/mission-uncuttable/code/src/main/resources/base/images/files/mp3logo.jpg"
            #ToDo
            picture = Image.open(filename)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(os.path.basename(last_element), self.listWidget)
            item.setStatusTip(last_element)
            item.setIcon(icon)
        else:
            print("The datatype is not supported")
            pass



    def clearFileNames(self):

        self.listWidget.clear()


def main():
    app = QApplication(sys.argv)
    window = Filemanager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
