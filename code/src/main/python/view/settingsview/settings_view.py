from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import os


class SettingsView(QMainWindow):
    """A class used as the View for the settings window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(SettingsView, self).__init__()
        path = os.path.abspath('src/main/python/view/settingsview')
        uic.loadUi(path + '/settings_window.ui', self)
        comboBox = self.findChild(QComboBox, "comboBox")
        comboBox.currentIndexChanged.connect(self.selectionChange)
        self.setStyleSheet(open(path + '/style_dark.qss', "r").read())

    def selectionChange(self,i):
        path = os.path.abspath('src/main/python/view/settingsview')
        print('itemchanged')
        if(i == 0):
            self.setStyleSheet(open(path + '/style_dark.qss', "r").read())
        else:
            self.setStyleSheet(open(path + '/style_light.qss', "r").read())
            
        self.update()    

    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()
