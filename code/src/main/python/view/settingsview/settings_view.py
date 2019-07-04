from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QPushButton, QTabWidget,
                             QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QCheckBox, QLineEdit, QSpinBox)
from PyQt5.QtCore import Qt, QFileSystemWatcher, pyqtSignal
from PyQt5 import uic

from config import Resources, Language, Settings

class SettingsView(QMainWindow):
    """
    A class used as the View for the settings window.

    In this class the Settings from the json file get displayed.
    If you want to add a setting go to the "config.py" file and simply
    add the desired setting to the dictionary that you'll find there.
    """

    saved = pyqtSignal()

    def __init__(self, parent=None):
        """Loads the UI-file and the shortcuts."""

        super(SettingsView, self).__init__(parent)
        uic.loadUi(Resources.files.settingsview, self)

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.init_stylesheet()
        "QSS HOT RELOAD"
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)

        """ centering the window """
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

        self.saveButton = self.findChild(QPushButton,"saveButton")
        self.cancelButton = self.findChild(QPushButton, "cancelButton")

    def init_stylesheet(self):
        current_stylesheet = Settings.get_instance().get_settings().design.color_theme.current
        if current_stylesheet == 0:
            self.setStyleSheet(open(Resources.files.qss_dark, "r").read())     
        elif current_stylesheet == 1:
            self.setStyleSheet(open(Resources.files.qss_light, "r").read())

    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()

    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.init_stylesheet()
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

    def update_view(self):
        self.parent().update_window()