from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QVBoxLayout,QSplitter
from PyQt5 import uic
from shortcuts import ShortcutLoader
import os
from .preview import PreviewView

from Filemanager.filemanager import Filemanager


class VideoEditorView(QMainWindow):
    """A class used as the View for the video-editor window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(VideoEditorView, self).__init__()
        path = os.path.abspath('src/main/python/view/mainview')
        uic.loadUi(path + '/main_window.ui', self)
        self.previewlayout = self.findChild(QVBoxLayout, "preview")
        previewview = PreviewView()
        self.previewlayout.addWidget(previewview)

        self.shortcuts = ShortcutLoader(self)
        self.load_filemanager()

    def show(self):
        """Starts the video-editor-window maximized."""
        self.showMaximized()

    def load_filemanager(self):
        filemanager=Filemanager()
        splitter=self.findChild(QSplitter,"verticalSplitter")
        splitter.replaceWidget(0,filemanager)
        filemanager.show()