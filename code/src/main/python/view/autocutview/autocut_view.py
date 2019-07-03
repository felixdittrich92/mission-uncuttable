from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QLabel
from PyQt5.QtCore import QFileSystemWatcher, Qt
from PyQt5 import uic
from config import Resources


class AutocutView(QMainWindow):
    """Class that displays the view for the autocut feature."""
    def __init__(self):
        """Loads the UI-file and sets up the GUI."""
        super(AutocutView, self).__init__()
        uic.loadUi(Resources.files.autocut_view, self)

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.size())

        self.setStyleSheet(
            open(Resources.files.qss_dark, "r").read())

        "QSS HOT RELOAD"
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

        # centering the window
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

        cross_path = Resources.images.cross
        tick_path = Resources.images.tick
        self.cross = QPixmap(cross_path).scaledToHeight(50, mode=1)
        self.tick = QPixmap(tick_path).scaledToHeight(50, mode=1)

        self.video_image_label.setPixmap(self.cross)
        self.pdf_image_label.setPixmap(self.cross)

    def show(self):
        """Starts the window normal (not maximized)."""
        self.showNormal()

    def change_icon(self, label):
        """Changes the icon of a label to a tick icon."""
        label.setPixmap(self.tick)
    
    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.setStyleSheet(open(Resources.files.qss_dark, "r").read())
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)
