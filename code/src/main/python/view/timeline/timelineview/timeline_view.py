from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal
from config import Resources
from .timeline_scroll_area import TimelineScrollArea
from view.timeline.trackview import TrackView
from view.timeline.timeableview import TimeableView
from view.timeline.util.timelineview_utils import *
from controller import TimelineController


class TimelineView(QFrame):
    """
    Extends QFrame to the toplevel widget of the timeline view which
    shows the tracks and provides tools and controls to view and
    manipulate them.

    The widget holds the TimelineScrollArea which fulfills the task of
    displaying the tracks.
    """

    zoom_factor_changed = pyqtSignal(float)

    def __init__(self, parent=None):
        """
        Create a TimelineView with a TimelineScrollArea.

        @param parent the parent component
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

        self.__zoom_factor = 1

    def create_track(self, name, width, height, num, is_overlay):
        """ Creates a new trackView and adds it to the track_frame """
        btn = QPushButton(name)
        btn.setFixedSize(90, height)
        self.track_button_frame.add_button(btn)
        track = TrackView(width, height, num, name, btn, is_overlay=is_overlay)
        self.tracks[num] = track

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

    def create_timeable(self, track_id, name, start, length, model, timeable_id, res_left=0, res_right=0, mouse_pos=0,
                        is_drag=False):
        """ Creates and adds a timeable to the specified track """
        try:
            track = self.tracks[track_id]
        except KeyError:
            return

        # Todo:
        #  Creating a TimeableView in the view should be as simple as
        #  possible. Therefore we should specify start as the start
        #  which the resulting timeable should really have. It should
        #  not depend on some drag parameters. Drag and drop should be
        #  handled completely before somehow.
        #  So, this start shift which was here originally should be
        #  removed and compensated before calling this function:
        start = start - mouse_pos

        # Change note:
        # Originally, the timeable was created later after adjusting
        # the track sizes. Because the timeable knows best about its own
        # size we should create the timeable first and then get its size
        # for actually adjusting the tracks.
        timeable = TimeableView(
            name,
            start, length,
            track.height,
            res_left, res_right,
            model,
            timeable_id, track_id)

        # Todo: Maybe bring setting the zoom factor to the track view
        #  where it would be done if a timeable is added.
        timeable.set_zoom_factor(self.__zoom_factor)
        self.zoom_factor_changed.connect(timeable.set_zoom_factor)

        if timeable.get_end_pos() > track.width:
            track.set_width(timeable.get_end_pos())
            TimelineController.get_instance().adjust_tracks()

        # Change note:
        # Leave this unchanged because I don't know what removing would
        # lead to.
        timeable.mouse_press_pos = mouse_pos
        track.add_timeable(timeable)

        if is_drag:
            track.current_timeable = timeable

        # add timeable to dict
        self.timeables[timeable_id] = timeable

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

    def update_timecode(self, timecode):
        self.time_label = self.findChild(QObject, 'time_label')
        self.time_label.setText(timecode)

    def set_zoom_factor(self, zoom_factor):
        """ Set the zoom factor.

        @param zoom_factor: The new zoom factor in pixels per frame.
        @type zoom_factor:  float
        """
        self.__zoom_factor = zoom_factor
        self.zoom_factor_changed.emit(self.__zoom_factor)
