from PyQt5.QtWidgets import QMainWindow, QWidget, QComboBox, QTabWidget, QPushButton, QVBoxLayout
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import os
from config import Settings


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
        
        settings = Settings.get_instance()
        self.settings = settings.get_settings()
        print(self.settings.color_theme[0].name)

        self.addSetting('blabla', 'neu', 'liste', 'null')
        

    def selectionChange(self,i):
        path = os.path.abspath('src/main/python/view/settingsview')
        # print('itemchanged')
        if(i == 0):
            self.setStyleSheet(open(path + '/style_dark.qss', "r").read())
        else:
            self.setStyleSheet(open(path + '/style_light.qss', "r").read())
            
        self.update()    

    def addSetting(self, name, category, type, setting):
        tabWidget = self.findChild(QTabWidget, 'tabWidget')
        newTab=True
        for i in range(tabWidget.count()):
            if(tabWidget.tabText(i)==category):
                print('found')
                testWidget = QPushButton(name)
                tabWidget.widget(i).layout = QVBoxLayout()
                tabWidget.widget(i).layout.addWidget(testWidget)
                tabWidget.widget(i).setLayout(tabWidget.widget(i).layout)
                newTab=False

        if newTab:
            tabWidget.addTab(QWidget(), category)


        # # if(category=='Design'):
        # # if(category=='ShortCuts'):
        # else:
        #     self.tab = QWidget
        #     TabWidget = self.findChild(QTabWidget, 'tabWidget')
        #     TabWidget.addTab(self.tab, name)



    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()
