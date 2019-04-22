import sys

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, QGridLayout
from PyQt5.QtCore import QObject
from PIL import Image, ImageQt

from config import Resources


class Filemanager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Resources.get_instance().files.filemanager, self)
        self.pickButton = self.findChild(QObject,'pushButton_2')
        self.clearButton = self.findChild(QObject,'pushButton_3')
        self.listWidget = self.findChild(QObject,'listWidget')
        #self.listWidget.setSizeHint(QSize(0,200))

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

        if last_element.endswith(('.jpg','.JPEG','.JPG')):
            picture = Image.open(last_element)
            picture.thumbnail(((200,200)), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(last_element[:20] + "...", self.listWidget)
            item.setStatusTip(last_element)
            item.setIcon(icon)
        elif last_element.endswith('.mp4'):
            picture = Image.open(last_element)
            picture.thumbnail(((400,400)), Image.ANTIALIAS)
            icon = QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            item = QListWidgetItem(last_element[:20] + "...", self.listWidget)
            item.setStatusTip(last_element)
            item.setIcon(icon)
        elif last_element.endswith('.mp3'):
            pass # TO DO



    def clearFileNames(self):

        self.listWidget.clear()


def main():
    app = QApplication(sys.argv)
    window = Filemanager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
