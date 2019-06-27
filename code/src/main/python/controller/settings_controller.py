class SettingsController:
    """
    A class used as the Controller for the settings window.

    Manages starting and stopping of the settings window.
    """
    def __init__(self, view):
        self.__settings_view = view

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

    def stop(self):
        """Closes the settings window."""
        self.__settings_view.close()