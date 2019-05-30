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
    """A class used as the View for the projectsettings window."""
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

        """imports projectsettings instance and applies it"""
        self.projectsettingsInstance = Projectsettings.get_instance()
        self.projectsettings = self.projectsettingsInstance.get_dict_projectsettings()
        self.addProjectsettings(self.projectsettings)

        """saveprojectsettings button"""
        saveButton = self.findChild(QPushButton, "saveButton")
        saveButton.clicked.connect(lambda: self.saveProjectsettings())

        cancelButton = self.findChild(QPushButton, "cancelButton")
        cancelButton.clicked.connect(lambda: self.close())


    def addProjectsettings(self, projectsettings):
        """
        this method goes through the projectsettings dictionary and
        puts the projectsettings in layouts in the tabs where they belong.
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
        constructs a projectsetting in form of a QWidget with a QHBoxLayout
        """
        name = self.projectsettings[x][y].get("name")
        type = self.projectsettings[x][y].get("type")
        values = self.projectsettings[x][y].get("values")
        current = self.projectsettings[x][y].get("current")

        widget = QWidget()
        widget.setObjectName(name)
        layout = QHBoxLayout()
        layout.addWidget(QLabel(name))

        """
        Adds the projectsettings to the layout according to the type of option
        More options to be added when needed
        """

        if type == "dropdown":
            box = QComboBox()
            box.addItems(values)
            box.setCurrentIndex(current)
            layout.addWidget(box)
        elif type == "checkbox":
            checkbox = QCheckBox()
            checkbox.setChecked(current)
            layout.addWidget(checkbox)
        elif type == "text":
            textwindow = QPlainTextEdit()
            textwindow.setPlainText(current)
            """
            Resizing the window to fit the text properly
            """
            font = textwindow.document().defaultFont()
            fontmetrics = QtGui.QFontMetrics(font)
            textsize = fontmetrics.size(0, current)

            windowwidth = 300
            windowextraheight = 15

            textwindow.setMaximumSize(windowwidth, textsize.height() + windowextraheight)

            layout.addWidget(textwindow)
        else:
            layout.addWidget(QLabel("I'm not implemented yet :("))
        widget.setLayout(layout)
        return widget

    def saveProjectsettings(self):
        """
        goes through all the projectsettings and saves the values to the dictionary
        and saves the new dictionary with the save_projectsettings() method from Projectsettings.

        """
        tabWidget = self.findChild(QTabWidget, 'tabWidget')

        i = 0
        for x in self.projectsettings:
            for y in self.projectsettings[x]:
                name = self.projectsettings[x][y].get("name")
                widget = self.findChild(QWidget, name)
                self.saveProjectsetting(self.projectsettings[x][y].get("type"), widget, x, y)
                i += 1

        self.projectsettingsInstance.save_projectsettings(self.projectsettings)
        self.close()

    def saveProjectsetting(self, type, widget, x, y):
        """
        takes the current UI projectsettings element and the current position in the
        dictionary and saves the value that was maybe changed by the user

        different usage of the data according to the type of option ("textwindow","dropdown","checkbox",...)
        more types to be added
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
        """Starts the projectsettings window maximized."""
        self.showNormal()
