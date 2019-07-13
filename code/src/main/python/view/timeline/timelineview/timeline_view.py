from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QObject, pyqtSignal
from config import Resources
from .timeline_scroll_area import TimelineScrollArea
from view.timeline.trackview import TrackView
from view.timeline.timeableview import TimeableView
from controller import TimelineController
from ...view import View
from util.classmaker import classmaker

class TimelineView(classmaker(QFrame, View)):
    """
    Extends QFrame to the toplevel widget of the timeline view which
    shows the tracks and provides tools and controls to view and
    manipulate them.

    The widget holds the TimelineScrollArea which fulfills the task of
    displaying the tracks.
    """

    changed = pyqtSignal()

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

        self.video_track_frame = self.findChild(QFrame, "video_track_frame")
        self.audio_track_frame = self.findChild(QFrame, "audio_track_frame")

        self.track_frame_frame = self.findChild(QFrame, "track_frame_frame")

        self.track_button_frame_frame = self.findChild(QFrame, "track_button_frame_frame")

        self.video_track_button_frame = self.findChild(QFrame, "video_track_button_frame")
        self.audio_track_button_frame = self.findChild(QFrame, "audio_track_button_frame")

        self.timeables = dict()
        self.tracks = dict()

    def create_video_track(self, track_id, width, height, layer, name, is_overlay):
        btn = QPushButton(name)
        btn.setFixedSize(90, height)
        self.video_track_button_frame.add_button(btn, True, layer)

        track = TrackView(track_id, width, height, layer, name, btn, True, is_overlay)
        self.tracks[track_id] = track

        self.video_track_frame.add_track(track, layer)

        self.adjust_track_sizes()

    def create_audio_track(self, name, width, height, num, index):
        btn = QPushButton(name)
        btn.setFixedSize(90, height)
        self.audio_track_button_frame.add_button(btn, False, index)

        track = TrackView(None, width, height, num, name, btn, False)
        self.tracks[num] = track

        self.audio_track_frame.create_track(None, )

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

    # Change note: This method had to be redefined completely because
    #  it was nearly impossible to understand what was happening inside.
    #  The code seemed way more complicated than needed for creating and
    #  adding a single TimeableView and did things which should happen
    #  somewhere else.
    #
    #  Two and a half months ago the interface between the TimelineView
    #  and the TimelineController was specified by function heads.
    #  The principle was to give all the timeline information to the
    #  TimelineView in a form which is as simple as possible. For this
    #  timeable creation function the idea was to have all these
    #  properties of the TimeableModel as function parameters which are
    #  needed to display the timeable. Then the function could easily
    #  create the TimeableView and add it to its internal data
    #  structure.
    #
    #  After the method's head had been changed the method started to do
    #  some pretty complex stuff, consisting of calculations which
    #  actually should happen before this function is called, such as
    #  position calculations from an x_pos and a mouse_pos. Also, there
    #  were some computations related to the tracks which included a
    #  (seemingly) random creation of a new track (i.e. without a
    #  purpose).
    def create_timeable(self, track_id, name, width, height, x_pos, timeable_id, res_left, res_right, group=None):
        """
        Create the view elements for a timeable with the specified
        properties and add them to the view.

        @param track_id:    The ID of the track which the timeable
                            belongs to.
        @param name:        The timeable's display name.
        @param width:       The width of the timeable.
        @param height:      The height of the timeable.
        @param x_pos:       The x pos of the timeable.
        @param timeable_id: The ID of the timeable.
        @param res_left:    The left-side trim value.
        @param res_right:   The right-side trim value.
        @param group:       The ID of the group which this timeable
                            belongs to if there is one.
        """
        if timeable_id in self.timeables:
            raise ValueError(
                "There's already a timeable existing with ID = {}"
                .format(timeable_id)
            )
        else:
            t = TimeableView(name, width, height, x_pos, res_left, res_right, timeable_id, track_id, None)
            self.timeables[timeable_id] = t
            self.tracks[track_id].add_timeable(t)

        # This return is only temporary for the drag and drop handling
        # of files from the file manager to the TimelineView. Later
        # there will be made some changes for proper collision checking.
        # After that this return shouldn't be needed anymore.
        return t

    def create_preview_timeable(self,
            name,
            width, height, x_pos,
            res_left, res_right,
            view_id,
            track_id):
        # for drag from the file manager to the timeline (temporary for
        # the sake of time)
        t = TimeableView(name, width, height, x_pos, res_left, res_right, view_id, track_id, None)
        self.timeables[view_id] = t
        return t

    def remove_timeable(self, id):
        """ Removes the timeable from the view and deletes it from the dict """
        try:
            timeable = self.timeables[id]
        except KeyError:
            return

        timeable.remove_from_scene()
        self.timeables.pop(id, None)

    def get_timeable_view_by_id(self, timeable_id):
        return self.timeables[timeable_id]

    def get_selected_timeables(self):
        """ Returns a list of all selected items in the timeline """
        res = []

        for t in self.tracks.values():
            res.extend(t.scene().selectedItems())

        return res

    def remove_all_tracks(self):
        for track in self.tracks.values():
            if track.is_video:
                self.video_track_frame.remove_track(None)
                self.video_track_button_frame.remove_button(track.button)

            else:
                self.audio_track_frame.remove_track(None)
                self.audio_track_button_frame.remove_button(track.button)

    def remove_track(self, track_id):
        """ Removes the TrackView with track_id """
        try:
            track = self.tracks[track_id]
        except KeyError:
            return

        if track.is_video:
            self.video_track_frame.remove_track(track)
            self.video_track_button_frame.remove_button(track.button)

        else:
            self.audio_track_frame.remove_track(track)
            self.audio_track_button_frame.remove_button(track.button)

        self.tracks.pop(track_id)

    def update_timecode(self, timecode):
        self.time_label = self.findChild(QObject, 'time_label')
        self.time_label.setText(timecode)

    def refresh(self):
        self.update()