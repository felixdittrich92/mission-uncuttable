from PyQt5.QtWidgets import QFrame
from PyQt5 import uic
from PyQt5.QtCore import QObject
import os

from .timeline_scroll_area import TimelineScrollArea


class TimelineView(QFrame):
    """
    Extends QFrame to the toplevel widget of the timeline view which
    shows the tracks and provides tools and controls to view and
    manipulate them.

    The widget consists of a toolbar and a TimelineScrollArea. The
    latter one really fulfills the task of displaying the tracks.
    """
    def __init__(self, parent=None):
        """
        Create a TimelineView with a new toolbar and TimelineScrollArea.

        :param parent: the parent component
        """
        super(TimelineView, self).__init__(parent)
        path = os.path.abspath('src/main/python/view/timeline/timelineview')
        uic.loadUi(path + '/timeline_view.ui', self)

        timeline_scroll_area = self.findChild(QObject, 'timeline_scroll_area')
        self.layout().replaceWidget(timeline_scroll_area, TimelineScrollArea())
        timeline_scroll_area.deleteLater()

        self.__show_debug_info_on_gui()

    def __show_debug_info_on_gui(self):
        """
        Setup the component somehow so that something can be seen which
        makes it possible to say if something works properly or not.
        """
        self.setStyleSheet('background-color: yellow')


