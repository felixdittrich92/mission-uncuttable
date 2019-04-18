import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtCore import QObject

from config import Resources


class Filemanager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(Resources.get_instance().files.filemanager, self)
        self.pushButton_3 = self.findChild(QObject,'pushButton_3')
        self.pushButton_2 = self.findChild(QObject,'pushButton_2')
        self.listWidget = self.findChild(QObject,'listWidget')
        self.pushButton_2.clicked.connect(self.pickFileNames)
        self.pushButton_3.clicked.connect(self.clearFileNames)

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
        self.listWidget.addItems(fileNames)

    def clearFileNames(self):
        self.listWidget.clear()


def main():
    app = QApplication(sys.argv)
    window = Filemanager()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

