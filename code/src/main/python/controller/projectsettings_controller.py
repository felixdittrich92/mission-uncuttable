class ProjectSettingsController:
    """
    A class used as the Controller for the projectsettings window.

    Manages starting and stopping of the projectsettings window.
    """
    def __init__(self, view):
        self.__projectsettings_view = view

    def start(self):
        """Calls '__show_view()' of the projectsettings_view"""
        self.__projectsettings_view.show()

    def stop(self):
        """Closes the projectsettings window."""
        self.__projectsettings_view.close()