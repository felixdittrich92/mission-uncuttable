from controller import VideoEditorController
from view import VideoEditorView


class StartController:
    def __init__(self, view):
        self.start_view = view
        self.start_view.show()

        self.start_view.pushButton.clicked.connect(self.open_video_editor)

    def open_video_editor(self):
        v = VideoEditorView()
        video_editor_controller = VideoEditorController(v)


