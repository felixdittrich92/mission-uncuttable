

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget
from PyQt5 import uic
from PyQt5.QtCore import QObject
from config import Resources
import os
from PIL import Image

class Filemanager(QWidget):

    def __init__(self, parent=None):
        super(Filemanager, self).__init__(parent)
        uic.loadUi(Resources.get_instance().files.filemanager, self)
        self.setupUi()
        # self.retranslateUi()

    def setupUi(self):
        self.setObjectName("file_manager")
        #Dialog.resize(673, 280)
        self.pushButton_3 = self.findChild(QObject,'pushButton_3')
        self.pushButton_2 = self.findChild(QObject,'pushButton_2')
        self.listWidget = self.findChild(QObject,'listWidget')
        # self.retranslateUi(self)
        self.pushButton_2.clicked.connect(self.filePick)
        self.pushButton_3.clicked.connect(self.clearListWidget)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_3.setToolTip(_translate("Dialog", "<html><head/><body><p>Clear</p></body></html>"))
        self.pushButton_3.setText(_translate("Dialog", "Clear"))
        self.pushButton_2.setToolTip(_translate("Dialog", "<html><head/><body><p>Pick File</p></body></html>"))
        self.pushButton_2.setText(_translate("Dialog", "Pick Files"))
        self.pushButton.setToolTip(_translate("Dialog", "<html><head/><body><p>Exit</p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Exit"))

    def filePick(self):
        fileNames, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Image Files (*.png);; Sound Files(*.mp3);; Movie Files (*.mp4)")

        self.fillListWidget(fileNames)

    def fillListWidget(self, filenames):
        file = filenames[0]
        if file.endswith(".jpg"):
            image = Image.open(file)
            image.show()

        print(file)
        print(filenames)
        

        self.listWidget.addItems(filenames)

    def clearListWidget(self):
        self.listWidget.clear()

    def exit(self):
        sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Filemanager()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

