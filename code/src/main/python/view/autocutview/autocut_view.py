from PyQt5.QtWidgets import QDesktopWidget, QMainWindow
from PyQt5 import uic
from config import Resources


class AutocutView(QMainWindow):
    """

    """
    def __init__(self):
        """
        Loads the UI-file and sets up the GUI.
        """
        super(AutocutView, self).__init__()
        uic.loadUi(Resources.get_instance().files.autocut_view, self)

        # centering the window
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    def show(self):
        """Starts the window normal (not maximized)."""
        self.showNormal()
