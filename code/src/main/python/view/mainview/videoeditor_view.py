from PyQt5.QtWidgets import QMainWindow, QSplitter
from PyQt5.QtCore import QObject
from PyQt5 import uic
import os

from view.timeline.timelineview.timeline_view import TimelineView


class VideoEditorView(QMainWindow):
    """A class used as the View for the video-editor window."""
    def __init__(self):
        """Loads the UI-file."""
        super(VideoEditorView, self).__init__()
        path = os.path.abspath('src/main/python/view/mainview')
        uic.loadUi(path + '/main_window.ui', self)
        self.load_timeline_widget()

    def load_timeline_widget(self):
        """
        Replaces the 'bottomFrame'-named QObject with a new instance of
        TimelineView. The widget doesn't have any real content yet after
        execution of this method.
        """
        splitter = self.findChild(QObject, 'horizontalSplitter')
        bottom_frame = self.findChild(QObject, 'bottomFrame')
        i = splitter.indexOf(bottom_frame)
        timeline_view = TimelineView()
        splitter.replaceWidget(i, timeline_view)
        timeline_view.show()

    def show(self):
        """Starts the video-editor-window maximized."""
        self.showMaximized()
