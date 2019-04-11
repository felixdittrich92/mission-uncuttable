from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from config import Resources
import os
from config import Settings
import json


class SettingsView(QMainWindow):
    """A class used as the View for the settings window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(SettingsView, self).__init__()
        uic.loadUi(Resources.get_instance().files.settingsview, self)
        self.setStyleSheet(open(path + '/style_dark.qss', "r").read())
        comboBox.currentIndexChanged.connect(self.selectionChange)
        comboBox = self.findChild(QComboBox, "comboBox")
        self.settings = settings.get_dict_settings()
        settings = Settings.get_instance()

        # centering the window
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())
        self.addSettings(self.settings)
        

    def selectionChange(self,i):
        path = os.path.abspath('src/main/python/view/settingsview')
        # print('itemchanged')
        if(i == 0):
            self.setStyleSheet(open(path + '/style_dark.qss', "r").read())
        else:
            self.setStyleSheet(open(path + '/style_light.qss', "r").read())
            
        self.update()    

    def addSettings(self, settings):
        tabWidget = self.findChild(QTabWidget, 'tabWidget')
        i = 2
        for x in settings:
            i += 1
            tabWidget.addTab(QWidget(), x)
            tabWidget.widget(i).layout = QVBoxLayout()
            for y in settings[x]:
                testWidget = self.makeSetting(settings[x][y].get("name"))
                tabWidget.widget(i).layout.addWidget(testWidget)
            tabWidget.widget(i).setLayout(tabWidget.widget(i).layout)      
  
    def makeSetting(self, name):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name))
        layout.addWidget(QPushButton("testbutton"))
        widget.setLayout(layout)
        return widget

    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()

    # def addSetting(self, name, category, type, setting):
    #     tabWidget = self.findChild(QTabWidget, 'tabWidget')
    #     newTab=True
    #     layoutExists=False
    #     for i in range(tabWidget.count()):
    #         if(tabWidget.tabText(i)==category):
    #             layoutIstda = tabWidget.widget(i).layout
    #             if layoutIstda is not None:
    #                 layoutExists = True
    #             newTab=False

    #     if newTab:
    #         tabWidget.addTab(QWidget(), category)
            
    #     if layoutExists:
    #         for i in range(tabWidget.count()):
    #             if(tabWidget.tabText(i)==category):
    #                 testWidget = self.makeSetting(name)
    #                 print(tabWidget.widget(i).layout)
    #                 tabWidget.widget(i).insertWidget(testWidget)
    #     else:
    #         if(tabWidget.tabText(i)==category):
    #             testWidget = self.makeSetting(name)
    #             tabWidget.widget(i).layout = QVBoxLayout()
    #             tabWidget.widget(i).layout.addWidget(testWidget)
    #             tabWidget.widget(i).setLayout(tabWidget.widget(i).layout)
