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
        uic.loadUi(Resources.files.mainview, self)

        self.load_filemanager()
        self.load_timeline_widget()

        self.needle = self.findChild(QWidget, "needle_top")

        print(self.needle)

        self.load_preview()

        self.splittersizes = []
        self.fullscreen = False

        self.setStyleSheet(open(Resources.files.qss_dark, "r").read())

        "QSS HOT RELOAD"
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

    def test(self, frame):
        print(frame)

    def load_preview(self):
        previewview = PreviewView.get_instance()

        splitter = self.findChild(QSplitter, "verticalSplitter")
        splitter.replaceWidget(1, previewview)
        previewview.show()
        self.needle.needle_moved.connect(self.test)
        previewview.maximize_button.clicked.connect(self.maxim)

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
        self.filemanager = Filemanager()
        splitter = self.findChild(QSplitter, 'verticalSplitter')
        splitter.replaceWidget(0, self.filemanager)
        self.filemanager.show()

    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.setStyleSheet(open(Resources.files.qss_dark, "r").read())
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

    def maxim(self):
        v_splitter = self.findChild(QObject, 'verticalSplitter')
        h_splitter = self.findChild(QObject, 'horizontalSplitter')

        if(self.fullscreen == False):

            self.v_sizes = v_splitter.sizes()
            self.h_sizes = h_splitter.sizes()

            self.splittersizes = (self.v_sizes, self.h_sizes)

            width = self.frameGeometry().width()
            height = self.frameGeometry().height()
            v_splitter.setSizes([0, width])
            h_splitter.setSizes([height, 0])

            self.fullscreen = True

        else:
            v_splitter.setSizes(self.splittersizes[0])
            h_splitter.setSizes(self.splittersizes[1])

            self.fullscreen = False
            