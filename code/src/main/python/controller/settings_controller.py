from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QPushButton, QTabWidget,
                             QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
                             QCheckBox, QLineEdit, QSpinBox)
                             
from PyQt5.QtCore import Qt, QFileSystemWatcher
from PyQt5 import uic

from config import Resources, Language
from config import Settings

class SettingsController:
    """
    A class used as the Controller for the settings window.

    Manages starting and stopping of the settings window.
    """
    def __init__(self, view):
        self.__settings_view = view

        """imports settings instance and applies it"""
        self.settingsInstance = Settings.get_instance()
        self.settings = self.settingsInstance.get_dict_settings()
        self.addSettings(self.settings)

        self.__settings_view.saveButton.setText(str(Language.current.settings.save))
        self.__settings_view.saveButton.clicked.connect(lambda: self.saveSettings())

        self.__settings_view.cancelButton.setText(str(Language.current.settings.cancel))
        self.__settings_view.cancelButton.clicked.connect(lambda: self.__settings_view.close())

    def start(self):
        """Calls '__show_view()' of SettingsController"""
        self.__settings_view.show()

    def focus(self):
        self.__settings_view.activateWindow()

    def checkIfClosed(self):
        if self.__settings_view is not None:
            if self.__settings_view.isVisible():
                return False
            else:
                return True
        else:
            return True

    def addSettings(self, settings):
        """
        this method goes through the settings dictionary and
        puts the settings in layouts in the tabs where they belong.
        """
        tabWidget = self.__settings_view.findChild(QTabWidget, 'tabWidget')
        i = 0
        for x in settings:
            if x != "Invisible":
                tabWidget.addTab(QWidget(), str(getattr(Language.current.settings, x)))
                tabWidget.widget(i).layout = QVBoxLayout()
                for y in settings[x]:
                    testWidget = self.makeSetting(x,y)
                    tabWidget.widget(i).layout.addWidget(testWidget)
                tabWidget.widget(i).layout.setAlignment(Qt.AlignTop)
                tabWidget.widget(i).setLayout(tabWidget.widget(i).layout)
                i += 1


    def makeSetting(self, x,y):
        """
        constructs a setting in form of a QWidget with a QHBoxLayout
        """
        type = self.settings[x][y].get("type")

        if(type != "invisible"):
            name = str(getattr(Language.current.settings, y))

            values = self.settings[x][y].get("values")
            current = self.settings[x][y].get("current")

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
            elif type == "text" or type == "shortcut":
                text_edit = QLineEdit()
                text_edit.setText(current)

                layout.addWidget(text_edit)
            elif type == "spinbox":
                sb = QSpinBox()
                sb.setMinimum(values[0])
                sb.setMaximum(values[1])
                sb.setValue(current)
                layout.addWidget(sb)
            else:
                layout.addWidget(QLabel("I'm not implemented yet :("))
            widget.setLayout(layout)
            return widget
        else:
            return None


    def saveSettings(self):
        """
        goes throug all the settings and saves the values to the dictionary
        and saves the new dictionary with the save_settings() method from Settings.
        """

        for x in self.settings:
            if x != "Invisible":
                for y in self.settings[x]:
                    name = str(getattr(Language.current.settings, y))
                    widget = self.__settings_view.findChild(QWidget, name)
                    self.saveSetting(self.settings[x][y].get("type"),widget,x,y)

        self.settingsInstance.save_settings(self.settings)
        self.__settings_view.close()

    def saveSetting(self, type, widget, x, y):
        """
        takes the current UI settings element and the current position in the
        dictionary and saves the value that was maybe changed by the user
        """

        if type == "dropdown":
            combobox = widget.findChild(QComboBox)
            self.settings[x][y]["current"]= combobox.currentIndex()
        elif type == "checkbox":
            checkbox = widget.findChild(QCheckBox)
            if checkbox.isChecked():
                self.settings[x][y]["current"] = True
            else:
                self.settings[x][y]["current"] = False
        elif type == "text":
            text_edit = widget.findChild(QLineEdit)
            self.settings[x][y]["current"] = text_edit.text()
        elif type == "shortcut":  # TODO VALIDIERUNG
            text_edit = widget.findChild(QLineEdit)
            self.settings[x][y]["current"] = text_edit.text()
        elif type == "spinbox":
            sb = widget.findChild(QSpinBox)
            self.settings[x][y]["current"] = sb.value()
        else:
            return 0

    def stop(self):
        """Closes the settings window."""
        self.__settings_view.close()