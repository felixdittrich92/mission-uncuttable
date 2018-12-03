from fbs_runtime.application_context import ApplicationContext
from controller import VideoEditorController
from view import VideoEditorView

import sys


class AppContext(ApplicationContext):
    def run(self):
        videoEditorView = VideoEditorView()
        videoEditorController = VideoEditorController(videoEditorView)
        return self.app.exec_()


if __name__ == '__main__':
    app = AppContext()
    exit_code = app.run()
    sys.exit(exit_code)