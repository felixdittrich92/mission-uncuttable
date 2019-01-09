from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os


class VideoEditorView(QMainWindow):
    """A class used as the View for the video-editor window."""
    def __init__(self):
        """Loads the UI-file."""
        super(VideoEditorView, self).__init__()
        path = os.path.abspath('src/main/python/view/mainview')
        uic.loadUi(path + '/main_window.ui', self)

    def show(self):
        """Starts the video-editor-window maximized."""
        self.showMaximized()
