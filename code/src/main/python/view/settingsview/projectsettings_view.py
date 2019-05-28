from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5 import QtGui
from config import Resources
import os
from projectconfig import Projectsettings
import json


class ProjectSettingsView(QMainWindow):
    """A class used as the View for the settings window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(ProjectSettingsView, self).__init__()
        uic.loadUi(Resources.files.projectsettings_view, self)
        self.setStyleSheet(open(Resources.files.qss_dark, "r").read())

        """ centering the window """
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

        """imports settings instance and applies it"""
        self.projectsettingsInstance = Projectsettings.get_instance()
        self.projectsettings = self.projectsettingsInstance.get_dict_settings()
        self.addProjectsettings(self.projectsettings)

        """savesettings button"""
        saveButton = self.findChild(QPushButton, "saveButton")
        saveButton.clicked.connect(lambda: self.saveProjectsettings())

        cancelButton = self.findChild(QPushButton, "cancelButton")
        cancelButton.clicked.connect(lambda: self.close())

    def addProjectsettings(self, projectsettings):
        """
        this method goes through the settings dictionary and
        puts the settings in layouts in the tabs where they belong.
        """
        tabWidget = self.findChild(QTabWidget, 'tabWidget')
        i = 0
        for x in projectsettings:
            tabWidget.addTab(QWidget(), x)
            tabWidget.widget(i).layout = QVBoxLayout()
            for y in projectsettings[x]:
                testWidget = self.makeProjectsetting(x, y)
                tabWidget.widget(i).layout.addWidget(testWidget)
            tabWidget.widget(i).layout.setAlignment(Qt.AlignLeft)
            tabWidget.widget(i).setLayout(tabWidget.widget(i).layout)
            i += 1

    def makeProjectsetting(self, x, y):
        """
        constructs a setting in form of a QWidget with a QHBoxLayout
        """
        name = self.projectsettings[x][y].get("name")
        type = self.projectsettings[x][y].get("type")
        values = self.projectsettings[x][y].get("values")
        current = self.projectsettings[x][y].get("current")

        widget = QWidget()
        widget.setObjectName(name)
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name))

        if type == "dropdown":
            box = QComboBox()
            box.addItems(values)
            box.setCurrentIndex(current)
            layout.addWidget(box)
        elif type == "checkbox":
            checkbox = QCheckBox()
            checkbox.setChecked(current)
            layout.addWidget(checkbox)
        elif type == "textwindow":
            textwindow = QPlainTextEdit()
            textwindow.setPlainText(current)

            font = textwindow.document().defaultFont()
            fontmetrics = QtGui.QFontMetrics(font)
            textsize = fontmetrics.size(0, current)

            textwindow.setMaximumSize(textsize.width() + 60, textsize.height() + 10)

            layout.addWidget(textwindow)
        else:
            layout.addWidget(QLabel("I'm not implemented yet :("))
        widget.setLayout(layout)
        return widget

    def saveProjectsettings(self):
        """
        goes through all the settings and saves the values to the dictionary
        and saves the new dictionary with the save_settings() method from Settings.

        """
        tabWidget = self.findChild(QTabWidget, 'tabWidget')

        i = 0
        for x in self.projectsettings:
            for y in self.projectsettings[x]:
                name = self.projectsettings[x][y].get("name")
                widget = self.findChild(QWidget, name)
                self.saveProjectsetting(self.projectsettings[x][y].get("type"), widget, x, y)
                i += 1

        self.projectsettingsInstance.save_settings(self.projectsettings)
        self.close()

    def saveProjectsetting(self, type, widget, x, y):
        """
        takes the current UI settings element and the current position in the
        dictionary and saves the value that was maybe changed by the user
        """

        if type == "dropdown":
            combobox = widget.findChild(QComboBox)
            values = self.projectsettings[x][y].get("values")
            self.projectsettings[x][y]["current"] = combobox.currentIndex()
        elif type == "checkbox":
            checkbox = widget.findChild(QCheckBox)
            if checkbox.isChecked():
                self.projectsettings[x][y]["current"] = True
            else:
                self.projectsettings[x][y]["current"] = False
        elif type == "textwindow":
            textwindow = widget.findChild(QPlainTextEdit)
            self.projectsettings[x][y]["current"] = textwindow.toPlainText()
        else:
            return 0

    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()
