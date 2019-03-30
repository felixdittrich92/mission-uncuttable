class ProjectSettingsController:
    """
    A class used as the Controller for the settings window.

    Manages starting and stopping of the settings window.
    """
    def __init__(self, view):
        self.__projectsettings_view = view

    def start(self):
        """Calls '__show_view()' of SettingsController"""
        self.__projectsettings_view.show()

    def stop(self):
        """Closes the settings window."""
        self.__projectsettings_view.close()