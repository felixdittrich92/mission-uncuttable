from fbs_runtime.application_context import ApplicationContext
from controller import VideoEditorController
from view import VideoEditorView
from controller import StartController
from view import StartView

import sys


class AppContext(ApplicationContext):
    def run(self):
        # video_editor_view = VideoEditorView()
        # video_editor_controller = VideoEditorController(video_editor_view)
        start_view = StartView()
        start_controller = StartController(start_view)
        return self.app.exec_()


if __name__ == '__main__':
    app = AppContext()
    exit_code = app.run()
    sys.exit(exit_code)
