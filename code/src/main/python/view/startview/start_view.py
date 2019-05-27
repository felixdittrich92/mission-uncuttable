import os

from PyQt5.QtCore import QFileSystemWatcher
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QStackedLayout
from PyQt5 import uic
from config import Settings
from config import Resources


class StartView(QMainWindow):
    """
    A class used as the View for the start window.

    The start window shows up first, when the program is launched.
    Its a small window, where the user can either open a already existing
    project or create a new one. When the user decides to create a new project,
    the view changes and the user is able to chose between the auto-cut-mode
    and the manual-cut-mode.
    """
    def __init__(self):
        """
        Loads the UI-file and sets up the GUI.

        Initially hides 'new_project_frame' and binds switch_frame() to
        'new_project_button' and 'back_button'.
        """
        super(StartView, self).__init__()
        uic.loadUi(Resources.get_instance().files.startview, self)

        self.setStyleSheet(
            open(Resources.get_instance().files.qss_dark, "r").read())

        "QSS HOT RELOAD"
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.get_instance().files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

        self.select_project_widget = SelectProjectWidget()
        self.decision_widget = DecisionWidget()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.select_project_widget)
        self.stacked_layout.addWidget(self.decision_widget)

        self.centralWidget().setLayout(self.stacked_layout)

        new_project_button = self.findChild(QWidget, "new_project_button")
        back_button = self.findChild(QWidget, "back_button")

        new_project_button.clicked.connect(self.switch_frame)
        back_button.clicked.connect(self.switch_frame)

        # centering the window
        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

        settings = Settings.get_instance()
        self.settings = settings.get_settings()

        # new_settings = {
        # "color_theme":[{
        #     "name":"Color Theme",
        #     "category":"neudesign",
        #     "type":"dropdown",
        #     "setting":"dark"
        # }],
        # "Option_1":[{
        #     "name":"Color Theme",
        #     "category":"neudesign",
        #     "type":"checkbox",
        #     "setting":"dark"
        # }]
        # }

        # settings.save_settings(new_settings)

    def show(self):
        """Starts the start-window normal (not maximized)."""
        self.showNormal()

    def switch_frame(self):
        """
        Switches the visible Widget of StartView.

        When 'select_project_widget' is visible, hide it and show
        'decision_widget', but when 'decision_widget' is visible, hide it and
        show 'select_project_widget'.
        """

        self.select_project_widget.setHidden(not self.select_project_widget.isHidden())
        self.decision_widget.setHidden(not self.decision_widget.isHidden())

    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.setStyleSheet(open(Resources.get_instance().files.qss_dark, "r").read())
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.get_instance().files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)


class SelectProjectWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        uic.loadUi(Resources.get_instance().files.select_project_widget, self)

        self.projects_list_view = self.findChild(QWidget, "projects_list_view")
        self.projects_list_view.addItem(
            os.path.join(os.path.expanduser("~"), "test.uc"))
        self.projects_list_view.addItem("Algorithmen und Datenstrukturen")


class DecisionWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        uic.loadUi(Resources.get_instance().files.decision_widget, self)
