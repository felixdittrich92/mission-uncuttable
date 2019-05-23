from controller import VideoEditorController
from controller import AutocutController
from view import VideoEditorView
from view import AutocutView


class MainController:
    """A class used as the Controller, that manages the windows of the program."""
    def __init__(self, view):
        self.__start_view = view
        self.__start_view.manual_cut_button.clicked.connect(self.__start_main_controller)
        self.__start_view.auto_cut_button.clicked.connect(self.__start_autocut_controller)

    def start(self):
        """Calls show() of StartView"""
        self.__start_view.show()

    def stop(self):
        """Closes the start window and tries to close the video-editor window."""
        self.__start_view.close()
        try:
            self.__video_editor_controller.stop()
        except NameError:
            pass

    def __start_main_controller(self):
        """Closes the start window and starts the video-editor window."""
        self.__start_view.close()
        video_editor_view = VideoEditorView()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()

    def __start_autocut_controller(self):
        self.__start_view.close()
        autocut_view = AutocutView()
        self.__autocut_controller = AutocutController(autocut_view)
        self.__autocut_controller.start()
