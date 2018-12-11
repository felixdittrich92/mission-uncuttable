class VideoEditorController:
    def __init__(self, view):
        self.__video_editor_view = view

    def __show_view(self):
        self.__video_editor_view.show()

    def start(self):
        self.__show_view()

    def stop(self):
        self.__video_editor_view.close()
