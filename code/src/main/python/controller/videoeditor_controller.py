import openshot

from .settings_controller import SettingsController
from view.settingsview import SettingsView
from .projectsettings_controller import ProjectSettingsController
from view.settingsview import ProjectSettingsView

from model.project.timeline import TimelineModel


class VideoEditorController:
    """
    A class used as the Controller for the video-editor window.

    Manages starting and stopping of the video-editor window.
    """
    def __init__(self, view):
        self.__video_editor_view = view
        self.__video_editor_view.action_settings.triggered.connect(self.__start_settings_controller)
        self.__video_editor_view.action_projectsettings.triggered.connect(self.__start_projectsettings_controller)
        self.__video_editor_view.actionExport.triggered.connect(self.__export)

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

    def __start_projectsettings_controller(self):
        "Opens the projectsettings window"
        projectsettings_view = ProjectSettingsView()
        self.__projectsettings_controller = ProjectSettingsController(projectsettings_view)
        self.__projectsettings_controller.start()

    def __export(self):
        """exports the timeline"""
        tm = TimelineModel.get_instance()
        t = tm.timeline

        # testing data
        audio_options = [True, "aac", 48000, 2, 3, 96000]
        video_options = [True, "libx264", t.info.fps, t.info.width,
                         t.info.height, openshot.Fraction(1, 1), False, False, 384000]

        # get the number of the last frame
        last_frame = 0
        for c in t.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * t.info.fps.ToFloat()) + 1

        tm.export("exported.mp4", audio_options, video_options, last_frame)
