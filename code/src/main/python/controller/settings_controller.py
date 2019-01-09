class SettingsController:
    """
    A class used as the Controller for the settings window.

    Manages starting and stopping of the settings window.
    """
    def __init__(self, view):
        self.__settings_view = view

    def __show_view(self):
        """Calls show() of 'SettingsView'."""
        self.__settings_view.show()

    def start(self):
        """Calls '__show_view()' of SettingsController"""
        self.__show_view()

    def stop(self):
        """Closes the settings window."""
        self.__settings_view.close()