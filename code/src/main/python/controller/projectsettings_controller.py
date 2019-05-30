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

    def focus(self):
        self.__projectsettings_view.activateWindow()

    def checkIfClosed(self):
        if self.__projectsettings_view is not None:
            if self.__projectsettings_view.isVisible():
                return False
            else:
                return True
        else:
            return True

    def stop(self):
        """Closes the projectsettings window."""
        self.__projectsettings_view.close()