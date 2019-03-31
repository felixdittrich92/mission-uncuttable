from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5 import uic
from config import Resources
import os


class ProjectSettingsView(QMainWindow):
    """A class used as the View for the settings window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(ProjectSettingsView, self).__init__()
        uic.loadUi(Resources.get_instance().files.projectsettings_view, self)

        # centering the window
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())


    def show(self):
        """Starts the settings window maximized."""
        self.showNormal()
