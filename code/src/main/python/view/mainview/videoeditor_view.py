from PyQt5.QtCore import QObject, QFileSystemWatcher
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QSplitter
from PyQt5 import uic
from config import Resources
from view.preview.preview import PreviewView

from controller.filemanager_controller import Filemanager
from controller import TimelineController

from view.timeline.timelineview import TimelineView


class VideoEditorView(QMainWindow):
    """A class used as the View for the video-editor window."""
    def __init__(self):
        """Loads the UI-file and the shortcuts."""
        super(VideoEditorView, self).__init__()
        uic.loadUi(Resources.get_instance().files.mainview, self)

        self.load_filemanager()
        self.load_timeline_widget()

        self.needle = self.findChild(QWidget, "needle_top")

        self.load_preview()

        self.setStyleSheet(open(Resources.get_instance().files.qss_dark, "r").read())

        "QSS HOT RELOAD"
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.get_instance().files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

    def load_preview(self):
        previewview = PreviewView.get_instance()

        splitter = self.findChild(QSplitter, "verticalSplitter")
        splitter.replaceWidget(1, previewview)
        previewview.show()

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
        TimelineController(timeline_view)
        splitter.replaceWidget(i, timeline_view)
        timeline_view.show()

    def show(self):
        """Starts the video-editor-window maximized."""
        self.showMaximized()

    def load_filemanager(self):
        filemanager = Filemanager()
        splitter = self.findChild(QSplitter, 'verticalSplitter')
        splitter.replaceWidget(0, filemanager)
        filemanager.show()

    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.setStyleSheet(open(Resources.get_instance().files.qss_dark, "r").read())
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.get_instance().files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)
