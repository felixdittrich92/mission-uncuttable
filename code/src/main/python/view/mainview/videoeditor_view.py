from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from shortcuts import ShortcutLoader
import os


class VideoEditorView(QMainWindow):
    """A class used as the View for the video-editor window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(VideoEditorView, self).__init__()
        path = os.path.abspath('src/main/python/view/mainview')
        uic.loadUi(path + '/main_window.ui', self)

        self.shortcuts = ShortcutLoader(self)

    def show(self):
        """Starts the video-editor-window maximized."""
        self.showMaximized()
