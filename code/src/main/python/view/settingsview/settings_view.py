from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import os


class SettingsView(QWidget):
    """A class used as the View for the settings window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(SettingsView, self).__init__()
        path = os.path.abspath('src/main/python/view/settingsview')
        uic.loadUi(path + '/settings_window.ui', self)


    def show(self):
        """Starts the settings window maximized."""
        self.showMaximized()
