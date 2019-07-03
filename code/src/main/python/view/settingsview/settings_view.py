from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QPushButton, QTabWidget,
                             QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QCheckBox, QLineEdit, QSpinBox)
from PyQt5.QtCore import Qt, QFileSystemWatcher
from PyQt5 import uic

from config import Resources, Language
from config import Settings



class SettingsView(QMainWindow):
    """
    A class used as the View for the settings window.

    In this class the Settings from the json file get displayed.
    If you want to add a setting go to the "config.py" file and simply
    add the desired setting to the dictionary that you'll find there.
    """
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(SettingsView, self).__init__()
        uic.loadUi(Resources.files.settingsview, self)

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setStyleSheet(open(Resources.files.qss_dark, "r").read())
        "QSS HOT RELOAD"
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)


        """ centering the window """
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

        self.saveButton = self.findChild(QPushButton,"saveButton")

        self.cancelButton = self.findChild(QPushButton, "cancelButton")

    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()

    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.setStyleSheet(open(Resources.files.qss_dark, "r").read())
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)
