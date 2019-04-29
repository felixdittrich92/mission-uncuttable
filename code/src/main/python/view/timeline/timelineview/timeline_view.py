from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QObject

from config import Resources
from .timeline_scroll_area import TimelineScrollArea
from view.timeline.trackview import TrackView
from view.timeline.timeableview import TimeableView

from util.timeline_utils import seconds_to_pos, get_px_per_second
from model.project.timeable import TimeableModel


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

        uic.loadUi(Resources.get_instance().files.timeline_view, self)

        timeline_scroll_area = self.findChild(QObject, 'timeline_scroll_area')
        self.layout().replaceWidget(timeline_scroll_area, TimelineScrollArea())
        timeline_scroll_area.deleteLater()
        self.track_frame = self.findChild(QFrame, "track_frame")
        self.track_button_frame = self.findChild(QFrame, "track_button_frame")

        self.__show_tracks()
        self.__show_debug_info_on_gui()

        timeables = {}
        tracks = {}

    def add_timeable(self, id, name, start, length, marked=False):
        pass

    def remove_timeable(self, id):
        pass

    def set_timeable_name(self, id, name):
        pass

    def set_timeable_start(self, id, frame):
        pass

    def set_timeable_length(self, id, frames):
        pass

    def set_timeable_selected(self, id, selected=True):
        pass

    def set_timeable_picture(self, id, picture):
        pass

    def __show_tracks(self):
        """shows some tracks with timeables to see if everything works"""

        # testing data
        f = "video.mp4"
        model = TimeableModel(f)
        w = seconds_to_pos(model.clip.Duration(), get_px_per_second())

        tr1 = TrackView(4800, 100, 3)
        tr1.add_timeable(TimeableView("video.mp4", w, 100, 0, model))
        self.track_frame.add_track(tr1)
        btn1 = QPushButton("Track 1")
        btn1.setFixedSize(100, 100)
        self.track_button_frame.add_button(btn1)

        tr2 = TrackView(2000, 100, 2)
        self.track_frame.add_track(tr2)
        btn2 = QPushButton("Track 2")
        btn2.setFixedSize(100, 100)
        self.track_button_frame.add_button(btn2)

    def __show_debug_info_on_gui(self):
        """
        Setup the component somehow so that something can be seen which
        makes it possible to say if something works properly or not.
        """
        self.setStyleSheet('background-color: yellow')
