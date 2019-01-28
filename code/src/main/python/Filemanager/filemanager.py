

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QListWidget


class Filemanager(QWidget):

    def __init__(self, parent=None):
        super(Filemanager, self).__init__(parent)

        self.setupUi()
        # self.retranslateUi()

    def setupUi(self):
        self.setObjectName("file_manager")
        #Dialog.resize(673, 280)
        self.pushButton_3 = QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 10, 75, 23))
        self.pushButton_3.setObjectName("btnClear")
        self.pushButton_2 = QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.pushButton_2.setObjectName("btnPickFile")
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(580, 10, 75, 23))
        self.pushButton.setObjectName("btnExit")
        self.listWidget = QListWidget(self)
        # self.retranslateUi(self)
        self.pushButton.clicked.connect(self.exit)
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

