from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QObject
import os

from .timeline_scroll_area import TimelineScrollArea


class TimelineView(QFrame):
    def __init__(self, parent=None):
        super(TimelineView, self).__init__(parent)
        path = os.path.abspath('src/main/python/view/timeline/timelineview')
        uic.loadUi(path + '/timeline_widget.ui', self)
        self.layout().addWidget(TimelineScrollArea())

        self.__show_debug_info_on_gui()

    def __show_debug_info_on_gui(self):
        """
        Sets up different background colors for the TimelineView and
        its own children. Besides this there is a label added to every
        component which shows the component's name.
        """
        toolbar_frame = self.findChild(QObject, 'toolbarFrame')
        toolbar_frame.setStyleSheet('background-color: brown')
        toolbar_frame.layout().insertWidget(
            0, QLabel(toolbar_frame.objectName())
        )
        self.setStyleSheet('background-color: yellow')


