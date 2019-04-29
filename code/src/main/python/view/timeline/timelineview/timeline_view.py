from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QObject
import os
from .timeline_scroll_area import TimelineScrollArea
from view.timeline.trackview import TrackView
from view.timeline.timeableview import TimeableView


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
        self.track_frame = self.findChild(QFrame, "track_frame")
        self.track_button_frame = self.findChild(QFrame, "track_button_frame")

        self.__show_tracks()
        self.__show_debug_info_on_gui()

    def __show_tracks(self):
        """shows some tracks with timeables to see if everything works"""
        tr1 = TrackView(2000, 100)
        tr1.add_timeable(TimeableView("timeable1", 200, 100, 0))
        tr1.add_timeable(TimeableView("timeable2", 400, 100, 300))
        self.track_frame.add_track(tr1)
        btn1 = QPushButton("Track 1")
        btn1.setFixedSize(100, 100)
        self.track_button_frame.add_button(btn1)

        tr2 = TrackView(2000, 100)
        tr2.add_timeable(TimeableView("timeable3", 200, 100, 150))
        self.track_frame.add_track(tr2)
        btn2 = QPushButton("Track 2")
        btn2.setFixedSize(100, 100)
        self.track_button_frame.add_button(btn2)

        tr3 = TrackView(2000, 100)
        tr3.add_timeable(TimeableView("timeable4", 300, 100, 700))
        self.track_frame.add_track(tr3)
        btn3 = QPushButton("Track 3")
        btn3.setFixedSize(100, 100)
        self.track_button_frame.add_button(btn3)

        tr4 = TrackView(2000, 100)
        tr4.add_timeable(TimeableView("timeable5", 300, 100, 400))
        tr4.add_timeable(TimeableView("timeable6", 100, 100, 0))
        self.track_frame.add_track(tr4)
        btn4 = QPushButton("Track 4")
        btn4.setFixedSize(100, 100)
        self.track_button_frame.add_button(btn4)

    def __show_debug_info_on_gui(self):
        """
        Setup the component somehow so that something can be seen which
        makes it possible to say if something works properly or not.
        """
        self.setStyleSheet('background-color: yellow')
