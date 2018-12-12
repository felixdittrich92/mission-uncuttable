from controller import VideoEditorController
from view import VideoEditorView


class MainController:
    def __init__(self, view):
        self.__start_view = view
        self.__start_view.manual_cut_button.clicked.connect(self.__start_main_controller)

    def start(self):
        self.__start_view.show()

    def stop(self):
        self.__start_view.close()
        try:
            self.__video_editor_controller.stop()
        except NameError:
            pass

    def __start_main_controller(self):
        self.__start_view.close()
        video_editor_view = VideoEditorView()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()
