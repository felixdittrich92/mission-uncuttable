from PyQt5.QtWidgets import QAction
from .settings_controller import SettingsController
from view.settingsview import SettingsView


class VideoEditorController:
    """
    A class used as the Controller for the video-editor window.

    Manages starting and stopping of the video-editor window.
    """
    def __init__(self, view):
        self.__video_editor_view = view
        self.__video_editor_view.action_settings.triggered.connect(self.__start_settings_controller)

    def __show_view(self):
        """Calls show() of 'VideoEditorView'."""
        self.__video_editor_view.show()

    def start(self):
        """Calls '__show_view()' of VideoEditorController"""
        self.__show_view()

    def stop(self):
        """Closes the video-editor Window."""
        self.__video_editor_view.close()

    def __start_settings_controller(self):
        "Opens the settings window"
        settings_view = SettingsView()
        self.__settings_controller = SettingsController(settings_view)
        self.__settings_controller.start()