from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
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

        # centering the window
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

        settings = Settings.get_instance()
        self.settings = settings.get_dict_settings()
        settings = Settings.get_instance()
        self.addSettings(self.settings)
        
    def addSettings(self, settings):
        tabWidget = self.findChild(QTabWidget, 'tabWidget')
        i = 0
        for x in settings:
            tabWidget.addTab(QWidget(), x)
            tabWidget.widget(i).layout = QVBoxLayout()
            for y in settings[x]:
                testWidget = self.makeSetting(settings[x][y].get("name"),settings[x][y].get("type"),settings[x][y].get("values"))
                tabWidget.widget(i).layout.addWidget(testWidget)
            tabWidget.widget(i).layout.setAlignment(Qt.AlignTop)
            tabWidget.widget(i).setLayout(tabWidget.widget(i).layout)
            i += 1      
  
    def makeSetting(self, name, type, values):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name))

        if type == "dropdown":
            box = QComboBox()
            box.addItems(values)
            layout.addWidget(box)
        elif type == "checkbox":
            layout.addWidget(QCheckBox())
        else:
            layout.addWidget(QLabel("I'm not implemented yet :("))
        widget.setLayout(layout)
        return widget

    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()