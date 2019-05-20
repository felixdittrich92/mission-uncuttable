from .settings_controller import SettingsController
from .projectsettings_controller import ProjectSettingsController
from model.project import Project
from view.settingsview import SettingsView
from view.settingsview import ProjectSettingsView
from view.exportview import ExportView


class VideoEditorController:
    """
    A class used as the Controller for the video-editor window.

    Manages starting and stopping of the video-editor window.
    """
    def __init__(self, view):
        self.__video_editor_view = view
        self.__video_editor_view.action_settings.triggered.connect(
            self.__start_settings_controller)
        self.__video_editor_view.action_projectsettings.triggered.connect(
            self.__start_projectsettings_controller)
        self.__video_editor_view.actionExport.triggered.connect(
            self.__start_export_controller)
        self.__video_editor_view.actionUndo.triggered.connect(
            self.__start_undo)

        self.__history = Project.get_instance().get_history()

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
        """Opens the settings window"""
        settings_view = SettingsView()
        self.__settings_controller = SettingsController(settings_view)
        self.__settings_controller.start()

    def __start_projectsettings_controller(self):
        """Opens the projectsettings window"""
        projectsettings_view = ProjectSettingsView()
        self.__projectsettings_controller = ProjectSettingsController(projectsettings_view)
        self.__projectsettings_controller.start()

    def __start_export_controller(self):
        """shows the export view"""
        export_view = ExportView()
        export_view.start()

    def __start_undo(self):
        """ Undo last action """
        if self.__history.get_num_operations() > 0:
            self.__history.undo_last_operation()
