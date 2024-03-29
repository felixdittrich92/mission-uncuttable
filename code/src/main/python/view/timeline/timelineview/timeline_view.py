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

    def create_video_track(self, name, width, height, num, index, is_overlay):
        btn = QPushButton(name)
        btn.setFixedSize(90, height)
        self.video_track_button_frame.add_button(btn, True, index)

        track = TrackView(width, height, num, name, btn, True, is_overlay)
        self.tracks[num] = track

        self.video_track_frame.add_track(track, index)

        self.adjust_track_sizes()

    def create_audio_track(self, name, width, height, num, index):
        btn = QPushButton(name)
        btn.setFixedSize(90, height)
        self.audio_track_button_frame.add_button(btn, False, index)

        track = TrackView(width, height, num, name, btn, False)
        self.tracks[num] = track

        self.audio_track_frame.add_track(track, index)

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
                        res_left, res_right, group, mouse_pos=0, is_drag=False, auto_audio=None):
        """ Creates and adds a timeable to the specified track """
        is_empty = False
        lastrack = None
        if track_id is not None:
            is_empty = True
            try:
                track = self.tracks[track_id]
            except KeyError:
                return
        else:
            for t in self.tracks:
                lastrack = t
                if self.tracks[t].is_video is False:
                    is_empty = True
                    for s in self.timeables:
                        if self.timeables[s].track_id == t:
                            is_empty = False
                if is_empty:      
                    track_id = t
                    track = self.tracks[t]
                    break

        if is_empty is not True:
            newtracknum = lastrack+1
            name = "Audio"+str(newtracknum)
            self.create_audio_track(name,1000,50,newtracknum, 1)
            track = self.tracks[newtracknum]

        x_pos = x_pos - mouse_pos
        if width + x_pos > track.width:
            track.set_width(width + x_pos)
            TimelineController.get_instance().adjust_tracks()

        timeable = TimeableView(name, width, track.height, x_pos, res_left, res_right,
                                model, id, track_id, group_id=group)
        timeable.mouse_press_pos = mouse_pos
        track.add_timeable(timeable)
   
        if is_drag:
            if auto_audio is not None:
                track2 = self.tracks[auto_audio]
                track2.current_timeable_2 = timeable
            else:
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

    def get_selected_timeables(self):
        """ Returns a list of all selected items in the timeline """
        res = []

        for t in self.tracks.values():
            res.extend(t.scene().selectedItems())

        return res

    def remove_all_tracks(self):
        for track in self.tracks.values():
            if track.is_video:
                self.video_track_frame.remove_track(track)
                self.video_track_button_frame.remove_button(track.button)

            else:
                self.audio_track_frame.remove_track(track)
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

        self.tracks.pop(track_id, None)

    def update_timecode(self, timecode):
        self.time_label = self.findChild(QObject, 'time_label')
        self.time_label.setText(timecode)

    def refresh(self):
        self.update()