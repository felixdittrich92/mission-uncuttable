from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QObject
from config import Resources
from .timeline_scroll_area import TimelineScrollArea
from view.timeline.trackview import TrackView
from view.timeline.timeableview import TimeableView
from controller import TimelineController


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

        uic.loadUi(Resources.files.timeline_view, self)

        timeline_scroll_area = self.findChild(QObject, 'timeline_scroll_area')
        self.layout().replaceWidget(timeline_scroll_area, TimelineScrollArea())
        timeline_scroll_area.deleteLater()

        self.track_frame = self.findChild(QFrame, "track_frame")
        self.track_button_frame = self.findChild(QFrame, "track_button_frame")

        self.timeables = dict()
        self.tracks = dict()

        self.controller = TimelineController(self)

        self.__show_debug_info_on_gui()

    def create_track(self, name, width, height, num):
        track = TrackView(width, height, num, name)
        self.tracks[num] = track

        btn1 = QPushButton(name)
        btn1.setFixedSize(80, 50)
        self.track_button_frame.add_button(btn1)

        self.track_frame.add_track(track)

        self.adjust_track_sizes()

    def adjust_track_sizes(self):
        """ Changes the width of all tracks to the size of the biggest track """
        if not self.tracks or len(self.tracks) == 1:
            return

        track_views = list(self.tracks.values())

        max_width = track_views[0].width

        for t in track_views[1:]:
            if t.width > max_width:
                max_width = t.width

        for t in track_views:
            t.set_width(max_width)

    def create_timeable(self, track_id, name, width, x_pos, model, id,
                        res_left=0, res_right=0, mouse_pos=0, is_drag=False):
        """ Creates and adds a timeable to the specified track """
        try:
            track = self.tracks[track_id]
        except KeyError:
            return

        x_pos = x_pos - mouse_pos
        if width + x_pos > track.width:
            track.set_width(width + x_pos)
            TimelineController.get_instance().adjust_tracks()

        timeable = TimeableView(name, width, track.height, x_pos, res_left, res_right,
                                model, id, track_id)
        timeable.mouse_press_pos = mouse_pos
        track.add_timeable(timeable)

        if is_drag:
            track.current_timeable = timeable

        # add timeable to dict
        self.timeables[id] = timeable

    def remove_timeable(self, id):
        """ Removes the timeable from the view and deletes it from the dict """
        try:
            timeable = self.timeables[id]
        except KeyError:
            return

        timeable.remove_from_scene()
        self.timeables.pop(id, None)

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

    def __show_debug_info_on_gui(self):
        """
        Setup the component somehow so that something can be seen which
        makes it possible to say if something works properly or not.
        """
        # self.setStyleSheet('background-color: yellow')
