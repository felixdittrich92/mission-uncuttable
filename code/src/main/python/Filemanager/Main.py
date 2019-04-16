import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
import cv2


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Filemanager")

        pybutton = QPushButton('Browse', self)
        pybutton.clicked.connect(self.App)
        pybutton.resize(100, 32)
        pybutton.move(50, 50)

    class App(QWidget):

            def __init__(self):
                super().__init__()
                self.title = 'PyQt5 file dialogs - pythonspot.com'
                self.left = 10
                self.top = 10
                self.width = 640
                self.height = 480
                self.initUI()

            def initUI(self):
                self.setWindowTitle(self.title)
                self.setGeometry(self.left, self.top, self.width, self.height)

                self.openFileNameDialog()
                self.openFileNamesDialog()
                self.saveFileDialog()

                self.show()
    #du musst ein neues Fenster machen wo dann die gespeicherten dateien angezeigt werden mit :  print(line.rstrip())
    # und als filename dann eine variable die auf die zuletzt gelesene  Datei verweist

            def openFileNameDialog(self):
                options = QFileDialog.Options()
                fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                          "All Files (*);", options=options)
                if fileName('*.txt'):
                    print(fileName)
                if fileName('*.jpg'):
                    print(fileName)
                if fileName('*.pdf'):
                    print(fileName)
                if fileName('*.mp4'):
                    print(fileName)






if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
