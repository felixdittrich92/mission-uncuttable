from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os


class VideoEditorView(QMainWindow):
    """
    @TODO Doc
    """
    def __init__(self):
        super(VideoEditorView, self).__init__()
        path = os.path.abspath('src/main/python/view/mainview')
        uic.loadUi(path + '/main_window.ui', self)

    def show(self):
        self.showMaximized()
