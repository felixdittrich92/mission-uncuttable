"""
The controller module for communication between timelineview and
timelinemodel.
"""

import os

from model.project import Project
from model.data import TimeableModel, TimelineModel
from model.data.operations import (CreationOperation, DeleteOperation, MoveOperation,
                                   DragOperation, CutOperation, ResizeOperation,
                                   CreateTrackOperation, DeleteTrackOperation,
                                   GroupMoveOperation)
from util.timeline_utils import generate_id, seconds_to_pos


class TimelineController:
    """
    The controller between the TimelineView and the TimelineModel.
    """

    __instance = None

    @staticmethod
    def get_instance():
        if TimelineController.__instance is None:
            raise Exception("TimelineController not initialized")

        return TimelineController.__instance

    def __init__(self, timeline_view):
        TimelineController.__instance = self

        self.__timeline_view = timeline_view
        self.__timeline_model = TimelineModel.get_instance()
        self.__history = Project.get_instance().get_history()

    def create_timeable(self, track_id, name, width, x_pos, model, id,
                        res_left=0, res_right=0, mouse_pos=0, hist=True,
                        group=None, is_drag=False):
        """
        Create a new object in the timeline model to represent a new timeable.

        @param data: The data needed to now what the timeable has to
                     contain and what track it has to be added to.
                     Important note: You may replace this parameter
                     with multiple ones if required while implementing
                     this method.
        @return:     Nothing.
        """
        op = CreationOperation(track_id, name, width, x_pos, model, id, res_left,
                               res_right, mouse_pos, group, is_drag, self)

        if hist:
            self.__history.do_operation(op)
        else:
            op.do()

        self.__timeline_view.changed.emit()

    def delete_timeable(self, view_info, model_info, hist=True):
        """
        Delete the model's representation of a timeable.

        @param id: The timeable's unique ID.
        @return:   Nothing.
        """
        op = DeleteOperation(view_info, model_info, self)
        if hist:
            self.__history.do_operation(op)
        else:
            op.do()

        self.__timeline_view.changed.emit()

    def remove_timeable_view(self, id):
        """
        Removes the View of a timeable from the Timeline.
        """
        self.__timeline_view.remove_timeable(id)

    def rename_timeable(self, id, name):
        """
        Rename the model's representation of a timeable.

        @param id:   The timeable's unique ID.
        @param name: The new name of the timeable.
        @return:     Nothing.
        """
        pass

    def move_timeable(self, id, old_pos, new_pos):
        """
        Set a new start of the model 's representation of a timeable.

        @param id:    The timeable's unique ID.
        @param pos:   The new position of the timeable.
        @return:      Nothing.
        """
        op = MoveOperation(id, old_pos, new_pos, self)
        self.__history.do_operation(op)

        self.__timeline_view.changed.emit()

    def drag_timeable(self, view_info_old, view_info_new, model_old, model_new):
        """
        Drags a timeable from one track to another track
        """
        op = DragOperation(view_info_old, view_info_new, model_old, model_new, self)
        self.__history.do_operation(op)

        self.__timeline_view.changed.emit()

    def split_timeable(self, view_id, res_right, width, model_end, pos):
        """
        Split the model's representation of a timeable at a specified
        time relative to the start of the timeable.

        The split will happen after the time-th frame of the timeable.
        This means that the time-th frame will belong to the first but
        not the second one of the resulting timeables.

        @param id:   The timeable's unique ID.
        @param pos:  The position at which the timeable should be split.
        @return:     Nothing.
        """
        op = CutOperation(view_id, res_right, width, model_end, pos,
                          generate_id(), generate_id(), self)
        self.__history.do_operation(op)

        self.__timeline_view.changed.emit()

    def resize_timeable(self, view_info_old, view_info_new):
        """
        Remove a part of the model's representation of a timeable
        between a start and an end time relative to the start of the
        timeable.

        The removed part includes the frames specified by start and end.

        @param id:    The timeable's unique ID.
        @param start: The number of the first frame removed.
        @param end:   The number of the last frame removed.
        @return:      Nothing.
        """
        op = ResizeOperation(view_info_old, view_info_new, self)
        self.__history.do_operation(op)

        self.__timeline_view.changed.emit()

    def add_track(self, name, width, height, index, is_video):
        """
        Creates a new Track.

        @param track_id: id of the track which will be created
        @return: Nothing
        """
        track_id = max(self.__timeline_view.tracks.keys()) + 1
        op = CreateTrackOperation(track_id, name, width, height, index, is_video, self)
        self.__history.do_operation(op)

        self.__timeline_view.changed.emit()
        Project.get_instance().changed = True

    def delete_track(self, track_id):
        """
        Removes a track and all the timeables in it.

        @param track_id: id of the track which will be deleted
        @return: Nothing
        """
        track = self.__timeline_view.tracks[track_id]
        if track is None:
            return

        track_data = track.get_info_dict()
        timeables = [t.get_info_dict() for t in track.items()]
        index = self.get_track_index(track)

        op = DeleteTrackOperation(track_id, track_data, timeables, index, self)
        self.__history.do_operation(op)

        self.__timeline_view.changed.emit()
        Project.get_instance().changed = True

    def is_overlay_track(self, track_id):
        """
        Checks if the track with track_id is the overlay track.

        @param track_id: id of the track which will be checked
        @return: True if track is overlay, False otherwhise
        """
        if track_id not in self.__timeline_view.tracks:
            return False

        return self.__timeline_view.tracks[track_id].is_overlay

    def create_video_track(self, name, width, height, num, index=-1, is_overlay=False):
        """ Creates a new video track in the timeline """
        self.__timeline_view.create_video_track(
            name, width, height, num, index, is_overlay)

    def create_audio_track(self, name, width, height, num, index=-1):
        """ Creates a new audio track in the timeline """
        self.__timeline_view.create_audio_track(name, width, height, num, index)

    def set_track_width(self, track_id, new_width):
        try:
            track = self.__timeline_view.tracks[track_id]
            track.set_width(new_width)
        except KeyError:
            pass

    def get_track_index(self, track):
        """ Returns the index of the track in its layout """
        if track.is_video:
            return self.__timeline_view.video_track_frame.layout().indexOf(track)

        return self.__timeline_view.audio_track_frame.layout().indexOf(track)

    def get_project_timeline(self):
        """ Returns a dict with the data needed to recreate the timeline """
        data = {
            "tracks": [],
            "timeables": []
        }

        for _, tr in sorted(self.__timeline_view.tracks.items(), reverse=True):
            data["tracks"].append(tr.get_info_dict())

        for ti in self.__timeline_view.timeables.values():
            data["timeables"].append(ti.get_info_dict())

        return data

    def create_project_timeline(self, data):
        """
        Recreates the timeline when a project is loaded

        @param data: dictionary with info of timeables
        """
        for t in data["tracks"]:
            if t["type"]:
                self.create_video_track(t["name"], t["width"], t["height"], t["num"],
                                        is_overlay=t["is_overlay"])
            else:
                self.create_audio_track(t["name"], t["width"], t["height"], t["num"])

        for t in data["timeables"]:
            m = t["model"]
            model = TimeableModel(m["file_name"], m["id"])
            model.set_start(m["start"], is_sec=True)
            model.set_end(m["end"], is_sec=True)
            model.move(m["position"], is_sec=True)

            group = None
            if "group" in t:
                group = t["group"]

            self.create_timeable(t["track_id"], t["name"], t["width"], t["x_pos"],
                                 model, t["view_id"], res_left=t["resizable_left"],
                                 res_right=t["resizable_right"], group=group,
                                 hist=False)

    def create_project_groups(self, data):
        """ Recreates all groups when the project is loaded """
        for g in data:
            self.create_group_with_id(g, data[g])

    def create_default_tracks(self):
        """ Creates 2 video and 2 audio tracks when the user chooses manual cut """
        self.create_video_track("Video 1", 2000, 50, 4)
        self.create_video_track("Video 2", 100, 50, 3)

        self.create_audio_track("Audio 1", 100, 50, 2)
        self.create_audio_track("Audio 2", 200, 50, 1)

    def create_autocut_tracks(self):
        """
        Creates tracks for overlay, board, visualizer, audio when user chooses autocut
        """
        self.create_video_track("Overlay", 2000, 50, 3, is_overlay=True)
        self.create_video_track("Tafel", 2000, 50, 2)
        self.create_video_track("Visualizer", 2000, 50, 1)
        self.create_video_track("Folien", 2000, 50, 0)
        self.create_audio_track("Audio", 2000, 50, -1)

    def create_autocut_timeables(self, file_path, track, data):
        """
        Creates timeables for autocut.

        @param file_path: the path to the input video
        @param track:     the track where the timeables will be added
        @param data:      a list of tuples with start and end time of the video
        """
        for start, end in data:
            model = TimeableModel(file_path, generate_id())
            model.set_start(start, is_sec=True)
            model.set_end(end, is_sec=True)
            model.move(start, is_sec=True)

            width = seconds_to_pos(model.clip.Duration())
            x_pos = seconds_to_pos(start)
            self.create_timeable(track, os.path.basename(file_path),
                                 width, x_pos, model, generate_id(), hist=False)

    def add_clip(self, file_path, track):
        """ Gets a path to file and a track and creates a timeable """
        model = TimeableModel(file_path, generate_id())

        width = seconds_to_pos(model.clip.Duration())
        self.create_timeable(track, os.path.basename(file_path),
                             width, 0, model, generate_id(), hist=False)

    def clear_timeline(self):
        """ Removes all timeline data """
        self.__timeline_model.remove_all_clips()
        self.__timeline_view.remove_all_tracks()

        self.__history.clear_history()

    def adjust_tracks(self):
        """ Adjusts the track sizes so they all have the same length """
        self.__timeline_view.adjust_track_sizes()
        self.__timeline_view.audio_track_frame.adjustSize()
        self.__timeline_view.video_track_frame.adjustSize()
        self.__timeline_view.track_frame_frame.adjustSize()
        self.__timeline_view.audio_track_button_frame.adjustSize()
        self.__timeline_view.video_track_button_frame.adjustSize()
        self.__timeline_view.track_button_frame_frame.adjustSize()

    def get_timeable_by_id(self, id):
        """
        Returns the timeableview with the given id, if it exists.

        @param id: The timeables unique ID.
        @return:   the TimeableView with the id or None if it doesn't exist.
        """
        try:
            return self.__timeline_view.timeables[id]
        except KeyError:
            return None

    def create_group(self, ids):
        """
        Create a TimeableGroup with all timeables in ids in it.
        The group will be added to the timeline model.

        @param ids: list of ids of timeable views
        @return: Nothing
        """
        timeables = [self.get_timeable_by_id(i) for i in ids]
        self.__timeline_model.create_group(generate_id(), timeables)

    def create_group_with_id(self, group_id, ids):
        """ Create TimeableGroup with group_id and timeable ids """
        timeables = [self.get_timeable_by_id(i) for i in ids]
        self.__timeline_model.create_group(group_id, timeables)

    def get_group_by_id(self, group_id):
        """
        Returns the group with the id of group_id.

        @param group_id: id of the group that is requested
        @return: TimeableGroup with id = group_id
        """
        try:
            return self.__timeline_model.groups[group_id]
        except KeyError:
            return None

    def is_same_group(self, first_group_id, second_group_id):
        """
        Checks if two timeables are in the same group

        @param first_group_id: group id of first timeable
        @param second_group_id: group id of second timeable
        @return: True if both timeables are in same TimeableGroup, False otherwhise
        """
        if first_group_id is None or second_group_id is None:
            return False

        return first_group_id == second_group_id

    def add_timeable_to_group(self, group_id, timeable_id):
        try:
            timeable = self.get_timeable_by_id(timeable_id)
            self.get_group_by_id(group_id).add_timeable(timeable)

            self.__timeline_view.changed.emit()
        except AttributeError:
            pass

    def remove_timeable_from_group(self, group_id, timeable_id):
        """
        Removes a timeable from a group.

        @param group_id: the id of the group from which the timeable will be removed
        @param timeable_id: the id of the timeable that will be removed from the group
        @return: Nothing
        """
        try:
            timeable = self.get_timeable_by_id(timeable_id)
            self.get_group_by_id(group_id).remove_timeable(timeable)

            self.__timeline_view.changed.emit()
        except AttributeError:
            pass

    def try_group_move(self, group_id, diff):
        """
        Checks if all timeables in the group can be moved and executes the moves
        if its possible.

        @param group_id: id of the group that is requested to move
        @param diff: the difference between the old and new position of the timeables
        @return: Nothing
        """
        try:
            group = self.get_group_by_id(group_id)
            if group.is_move_possible(diff):
                for t in group.timeables:
                    t.do_move(t.x_pos + diff)
        except AttributeError:
            pass

    def group_move_operation(self, group_id, diff):
        """
        Creates as GroupMoveOperation that updates the models of all timeables
        in the group and saves the move in the history.

        @param group_id: the id of the group that got moved
        @return: Nothing
        """
        op = GroupMoveOperation(group_id, diff, self)
        self.__history.do_operation(op)

        self.__timeline_view.changed.emit()

    def group_selected(self):
        """ Groups all selected timeables """
        items = self.__timeline_view.get_selected_timeables()
        ids = [i.view_id for i in items]

        self.create_group(ids)

    def get_timelineview(self):
        """ Returns the timelineview connected with the controller """
        return self.__timeline_view

    def get_timelinemodel(self):
        """ Returns the timelinemodel connected with the controller """
        return self.__timeline_model

    def update_timecode(self, timecode):
        self.__timeline_view.update_timecode(timecode)
