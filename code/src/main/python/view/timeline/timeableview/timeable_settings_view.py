from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import *
from config import Settings, Language, Resources
from PyQt5 import uic


class TimeableSettingsView(QDialog):
    """
    A class used as the View for the timeable settings window.
    """
    def __init__(self):
        """Loads the UI-file"""

        super(TimeableSettingsView, self).__init__()

        uic.loadUi(Resources.files.timeable_settings, self)
        self.__qss_watcher = QFileSystemWatcher()
        self.init_stylesheet()
        self.__qss_watcher.fileChanged.connect(self.update_qss)

        self.setFixedSize(351, 120)
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)

        self.saveButton.clicked.connect(self.save_settings)
        self.cancelButton.clicked.connect(self.cancel_settings)
        self.volume_slider.valueChanged.connect(self.changed_volume)

        self.saveButton.setText(str(Language.current.timeablesettings.save))
        self.cancelButton.setText(str(Language.current.timeablesettings.cancel))

        self.current_volume_value = None
        self.old_value = None

    def init_stylesheet(self):
        current_stylesheet = Settings.get_instance().get_settings().design.color_theme.current
        if current_stylesheet == 0:
            self.setStyleSheet(open(Resources.files.qss_dark, "r").read())     
        elif current_stylesheet == 1:
            self.setStyleSheet(open(Resources.files.qss_light, "r").read())

    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.init_stylesheet()
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)
    
    def save_settings(self):
        self.accept()

    def cancel_settings(self):
        self.current_volume_value = self.old_value
        self.reject()

    def changed_volume(self):
        self.current_volume_value = self.volume_slider.value() / 10
        self.current_volume.setText(str(Language.current.timeablesettings.label 
                        + " " + str(int(self.current_volume_value*10)*10) + "%"))

    def update_values(self):
        self.volume_slider.setValue(self.current_volume_value*10)
        self.current_volume.setText(str(Language.current.timeablesettings.label
                        + " " + str(int(self.current_volume_value*10)*10) + "%"))

    def set_data(self, value):
        self.old_value = value
        self.current_volume_value = value
        self.update_values()
