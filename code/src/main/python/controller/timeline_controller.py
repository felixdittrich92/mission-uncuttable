"""
The controller module for communication between timelineview and
timelinemodel.
"""

import os

from model.project import Project
from model.data import TimeableModel, TimelineModel
from model.data.operations import (
    CreationOperation, DeleteOperation,
    MoveOperation,
    CutOperation,
    TrimStartOperation, TrimEndOperation,
    CreateTrackOperation, DeleteTrackOperation)
from util.timeline_utils import\
    (generate_id, seconds_to_pos, pos_to_seconds)


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

    def __init__(self, video_editor_controller, timeline_view):
        TimelineController.__instance = self

        self.__video_editor_controller = video_editor_controller

        self.__timeline_view = timeline_view
        self.__timeline_view.set_timeline_controller(self)
        self.__timeline_model = TimelineModel.get_instance()
        self.__timeline_model.set_controller(self)
        self.__history = Project.get_instance().get_history()

        self.__focus = 0
        """
        The focused position of the timeline. Operations can be called
        to happen at this position and it can be used by a preview
        player to display the focused frame.
        """

        self.__preview_timeable = None

    # =========================================================================
    # == View <==> controller                                                ==
    # =========================================================================

    # Todo: Add documentation for parameters
    def create_timeable(self, file_path, track_id, name, x_pos, hist=True):
        """
        Create a new object in the timeline model to represent a new timeable.

        @param file_path: The path of the file which the timeable should
                         use.
        @param data: The data needed to now what the timeable has to
                     contain and what track it has to be added to.
                     Important note: You may replace this parameter
                     with multiple ones if required while implementing
                     this method.
        @return:     Nothing.
        """
        op = CreationOperation(file_path, track_id, name, x_pos, self.__timeline_model)

        if hist:
            self.__history.do_operation(op)
        else:
            op.do()

        # very rude implementation to get the view of the created
        # timeable. It will be returned to the caller.
        # The purpose is to have a quick solution for the drag and drop
        # process from the file manager to the TimelineView.
        # This implementation is only temporary.
        timeable_model = op.timeable_model
        timeable_view = self.__timeline_view.\
            get_timeable_view_by_id(timeable_model.get_id())

        # Todo: Move this signal emitting to TimelineView
        #  The view knows the best about its changes so the view should
        #  be the one which notifies about them.
        self.__timeline_view.changed.emit()

        return timeable_view

    def delete_timeable(self, timeable_id, hist=True):
        """
        Delete the model's representation of a timeable.

        @param timeable_id:
        @param id: The timeable's unique ID.
        @return:   Nothing.
        """
        op = DeleteOperation(timeable_id, self.__timeline_model)
        if hist:
            self.__history.do_operation(op)
        else:
            op.do()

        # Todo: Move this signal emitting to TimelineView
        #  The view knows the best about its changes so the view should
        #  be the one which notifies about them.
        self.__timeline_view.changed.emit()

    def create_preview_timeable(self, filepath, name="preview timeable"):
        self.__preview_timeable = \
            TimeableModel(generate_id(), filepath, name)
        timeable_view = self.__timeline_view.create_preview_timeable(
            self.__preview_timeable.name,
            self.__preview_timeable.get_width(),
            50,
            0,
            0, 0,
            self.__preview_timeable.get_id(),
            None
        )
        print("Preview Timeable created: ID={}"
              .format(self.__preview_timeable.get_id()))
        return timeable_view

    def add_preview_timeable(self, track_id, name, x_pos):
        self.create_timeable(
            self.__preview_timeable.file_path,
            track_id,
            name,
            x_pos
        )

    # def remove_timeable_view(self, id):
    #     """
    #     Removes the View of a timeable from the Timeline.
    #     """
    #     self.__timeline_view.remove_timeable(id)

    def rename_timeable(self, id, name):
        """
        Rename the model's representation of a timeable.

        @param id:   The timeable's unique ID.
        @param name: The new name of the timeable.
        @return:     Nothing.
        """
        pass

    def move_timeable(self, timeable_id, track_id, pos):
        """
        Set a new start of the model's representation of a timeable.

        @param track_id:
        @param timeable_id:    The timeable's unique ID.
        @param pos:   The new position of the timeable.
        @return:      Nothing.
        """
        op = MoveOperation(timeable_id, track_id, pos, self.__timeline_model)
        self.__history.do_operation(op)

        # Todo: Move this signal emitting to TimelineView
        #  The view knows the best about its changes so the view should
        #  be the one which notifies about them.
        self.__timeline_view.changed.emit()

    # def drag_timeable(self, view_info_old, view_info_new, model_old, model_new):
    #     """
    #     Drags a timeable from one track to another track
    #     """
    #     op = DragOperation(view_info_old, view_info_new, model_old, model_new, self)
    #     self.__history.do_operation(op)
    #
    #     # _Todo: Move this signal emitting to TimelineView
    #     #  The view knows the best about its changes so the view should
    #     #  be the one which notifies about them.
    #     self.__timeline_view.changed.emit()

    def split_timeable(self, timeable_id, pos):
        """
        Split the model's representation of a timeable at a specified
        time relative to the start of the timeable.

        The split will happen after the time-th frame of the timeable.
        This means that the time-th frame will belong to the first but
        not the second one of the resulting timeables.

        @param timeable_id:   The timeable's unique ID.
        @param pos:           The position at which the timeable should
                              be split.
        @return:              Nothing.
        """
        op = CutOperation(timeable_id, pos, self.__timeline_model)
        self.__history.do_operation(op)

        # Todo: Move this signal emitting to TimelineView
        #  The view knows the best about its changes so the view should
        #  be the one which notifies about them.
        self.__timeline_view.changed.emit()

    def split_timeable_at_focus(self, view_id):
        self.split_timeable(view_id, self.__focus)

    def trim_timeable_start(self, timeable_id, trim_length):
        """Trim the start of the model's representation of a timeable by
        a given length.

        @param timeable_id: The ID of the timeable to be trimmed.
        @param trim_length: The number of frames to be trimmed.
        @type trim_length:  int
        """
        op = TrimStartOperation(timeable_id, trim_length, self.__timeline_model)
        self.__history.do_operation(op)

    def trim_timeable_end(self, timeable_id, trim_length):
        """Trim the end of the model's representation of a timeable by a
        given length.

        @param timeable_id: The ID of the timeable to be trimmed.
        @param trim_length: The number of frames to be trimmed.
        @type trim_length:  int
        """
        op = TrimEndOperation(timeable_id, trim_length, self.__timeline_model)
        self.__history.do_operation(op)

    # def resize_timeable(self, view_info_old, view_info_new):
    #     """
    #     Remove a part of the model's representation of a timeable
    #     between a start and an end time relative to the start of the
    #     timeable.
    #
    #     The removed part includes the frames specified by start and end.
    #
    #     @param id:    The timeable's unique ID.
    #     @param start: The number of the first frame removed.
    #     @param end:   The number of the last frame removed.
    #     @return:      Nothing.
    #     """
    #     op = ResizeOperation(view_info_old, view_info_new, self)
    #     self.__history.do_operation(op)
    #
    #     # _Todo: Move this signal emitting to TimelineView
    #     #  The view knows the best about its changes so the view should
    #     #  be the one which notifies about them.
    #     self.__timeline_view.changed.emit()

    # Todo: implement set_timeable_volume (with an operation)
    def set_timeable_volume(self, timeable_id, volume):
        print("set_timeable_volume({}, {})".format(timeable_id, volume))

    def create_track(self, name, layer):
        """Create a new Track.

        @param name:  The name of the track.
        @type name:   str
        @param layer: The layer of the track.
        @type layer:  int
        """
        op = CreateTrackOperation(name, layer, self.__timeline_model)
        self.__history.do_operation(op)

        # Todo: Move this signal emitting to TimelineView
        #  The view knows the best about its changes so the view should
        #  be the one which notifies about them.
        self.__timeline_view.changed.emit()

        # Todo: Move this signal emitting to TimelineModel
        #  The model knows the best about its changes so it should be
        #  the one which notifies about them.
        Project.get_instance().changed = True

    # Todo: Let this method perform on the model---not the view.
    def delete_track(self, track_id):
        """Removes a track from the C{TimelineModel}.

        @param track_id: id of the track which will be deleted
        @return: Nothing
        """
        op = DeleteTrackOperation(track_id, self.__timeline_model)
        self.__history.do_operation(op)

        # Todo: Move this signal emitting to TimelineView
        #  The view knows the best about its changes so the view should
        #  be the one which notifies about them.
        self.__timeline_view.changed.emit()
        # Todo: Move this signal emitting to TimelineModel
        #  The model knows the best about its changes so it should be
        #  the one which notifies about them.
        Project.get_instance().changed = True

    def is_overlay_track(self, track_id):
        """
        Checks if the track with track_id is an overlay track.

        @param track_id: id of the track which will be checked
        @return: True if track is overlay, False otherwhise
        @raise KeyError: If there is no track in the timeline model
                         with the specified ID.
        """
        try:
            track_model = self.__timeline_model.track_id_map[track_id]
        except KeyError:
            raise KeyError(
                "Track doesn't exist in TimelineModel: ID={}"
                .format(track_id))
        finally:
            return track_model.is_overlay()

    def set_track_overlay(self, track_id, val):
        """
        Makes the Track with track_id an Overlay Track if val = True, and makes
        it a non Overlay Track if val = False.
        """
        raise RuntimeWarning(
            "Overlay property of the track could not be set because it"
            "cannot be associated with an object in the model."
        )
        # if track_id not in self.__timeline_view.tracks:
        #     return
        #
        # track = self.__timeline_view.tracks[track_id]
        #
        # for t in track.items():
        #     t.model.corner(val)

    # =========================================================================
    # == Model <==> Controller                                               ==
    # =========================================================================

    # Todo: implement track_created
    def track_added(self, track_model):
        self.__timeline_view.create_video_track(
            track_model.get_track_id(),
            1000, 50,
            track_model.get_layer(),
            track_model.get_name(),
            track_model.is_overlay()
        )

    def track_removed(self, track_id):
        self.__timeline_view.remove_track(track_id)

    # def video_track_created(self, name, width, height, num, index=-1, is_overlay=False):
    #     """ Creates a new video track in the timeline """
    #     self.__timeline_view.create_video_track(
    #         name, width, height, num, index, is_overlay)

    # def audio_track_created(self, name, width, height, num, index=-1):
    #     """ Creates a new audio track in the timeline """
    #     self.__timeline_view.create_audio_track(name, width, height, num, index)

    def timeable_model_added(self, timeable_model):
        self.__timeline_view.create_timeable(
            timeable_model.track.get_track_id(),
            timeable_model.name,
            timeable_model.get_width(),
            50,
            timeable_model.get_position(),
            timeable_model.get_id(),
            0,
            0
        )
        print(
            "[DEBUG] TimeableModel added: ID={}"
            .format(timeable_model.get_id()))

    def timeable_model_removed(self, timeable_id):
        self.__timeline_view.remove_timeable(timeable_id)
        print("[DEBUG] TimeableModel removed: ID={}".format(timeable_id))

    def timeable_model_changed(self, timeable_model):
        # Try statement as a simple solution to not quite perfect call
        #  sequences: When a timeable gets moved to a new timeline there
        #  are update notifications occurring before the timeable has
        #  been added to the view. Obviously, it's inevitable to find a
        #  real solution to that but for now it's easier this way and
        #  shouldn't have any effect on how tangled things get.
        try:
            self.__timeline_view.set_timeable_trimming(
                timeable_model.get_id(),
                timeable_model.get_trim_start(),
                timeable_model.get_trim_end()
            )
            self.__timeline_view.set_timeable_length(
                timeable_model.get_id(),
                timeable_model.get_length())
            self.__timeline_view.move_timeable(
                timeable_model.get_id(),
                timeable_model.track.get_track_id(),
                timeable_model.get_start())
        except KeyError:
            pass
        print(
            "[DEBUG] TimeableModel changed: ID={}"
            .format(timeable_model.get_id()))

    # =========================================================================
    # Todo: Sort these methods to one of the groups above
    # =========================================================================

    def set_track_width(self, track_id, new_width):
        try:
            track = self.__timeline_view.tracks[track_id]
            track.set_width(new_width)
            self.adjust_tracks()
        except KeyError:
            pass

    def get_track_index(self, track):
        """ Returns the index of the track in its layout """

        # Todo: Move the track index information to the model
        #  The track index information is currently taken from the index
        #  of the TrackView in the layout it's the child of. This means
        #  that the view stores information about the order of the
        #  tracks. This is not conform to the MVC pattern.
        #  The order of the tracks should be stored explicitly inside
        #  the model.
        if track.is_video:
            return self.__timeline_view.video_track_frame.layout().indexOf(track)

        return self.__timeline_view.audio_track_frame.layout().indexOf(track)

    def get_project_timeline(self):
        """ Returns a dict with the data needed to recreate the timeline """

        # Todo: Move the information gathering to the model
        #  Currently, the view gives the information about the timeline.
        #  But all data should be stored in the model.
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
                self.video_track_created(t["name"], t["width"], t["height"], t["num"],
                                         is_overlay=t["is_overlay"])
            else:
                self.audio_track_created(t["name"], t["width"], t["height"], t["num"])

        for t in data["timeables"]:
            m = t["model"]
            model = TimeableModel(m["id"], m["file_name"])
            model.set_trim_start(m["start"])
            model.set_trim_end(m["end"])
            model.move(None, m["position"], is_sec=True)

            group = None
            if "group" in t:
                group = t["group"]

            self.create_timeable(None, t["track_id"], t["name"], t["start"], hist=False)

    def create_project_groups(self, data):
        """ Recreates all groups when the project is loaded """
        for g in data:
            self.create_group_with_id(g, data[g])

    def create_default_tracks(self):
        """ Creates 2 video and 2 audio tracks when the user chooses manual cut """
        self.__history.do_operation(
            CreateTrackOperation("Track 1", 0, self.__timeline_model)
        )

    def create_autocut_tracks(self):
        """
        Creates tracks for overlay, board, visualizer, audio when user chooses autocut
        """
        self.video_track_created("Overlay", 2000, 50, 3, is_overlay=True)
        self.video_track_created("Tafel", 2000, 50, 2)
        self.video_track_created("Visualizer", 2000, 50, 1)
        self.video_track_created("Folien", 2000, 50, 0)
        self.audio_track_created("Audio", 2000, 50, -1)

    def create_autocut_timeables(self, file_path, track, data):
        """
        Creates timeables for autocut.

        @param file_path: the path to the input video
        @param track:     the track where the timeables will be added
        @param data:      a list of tuples with start and end time of the video
        """
        for start, end in data:
            model = TimeableModel(generate_id(), file_path)
            model.set_trim_start(start)
            model.set_trim_end(end)
            model.move(None, start, is_sec=True)

            width = seconds_to_pos(model.clip.Duration())
            x_pos = seconds_to_pos(start)
            self.create_timeable(None, track, os.path.basename(file_path), x_pos, hist=False)

    def add_clip(self, file_path, track):
        """ Gets a path to file and a track and creates a timeable """
        model = TimeableModel(generate_id(), file_path)

        width = seconds_to_pos(model.clip.Duration())
        self.create_timeable(None, track, os.path.basename(file_path), 0, hist=False)

    def clear_timeline(self):
        """ Removes all timeline data """
        self.__timeline_model.remove_all_timeables()
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

    # Todo: Refactor and adapt ungroup
    def ungroup(self, timeable_id):
        """
        Removes a timeable from a group.

        @param timeable_id: the id of the timeable that will be removed from the group
        @return: Nothing
        """
        raise NotImplementedError("ungroup not implemented yet")
        # try:
        #     timeable = self.get_timeable_by_id(timeable_id)
        #     self.get_group_by_id(group_id).remove_timeable(timeable)
        #
        #     self.__timeline_view.changed.emit()
        # except AttributeError:
        #     pass

    def try_group_move(self, group_id, diff):
        """
        Checks if all timeables in the group can be moved and executes the moves
        if its possible.

        @param group_id: id of the group that is requested to move
        @param diff: the difference between the old and new position of the timeables
        @return: Nothing
        """
        raise NotImplementedError("grouping not implemented yet")
        # try:
        #     group = self.get_group_by_id(group_id)
        #     if group.is_move_possible(diff):
        #         for t in group.timeables:
        #             t.do_move(t.x_pos + diff)
        # except AttributeError:
        #     pass

    def group_move_operation(self, group_id, diff):
        """
        Creates as GroupMoveOperation that updates the models of all timeables
        in the group and saves the move in the history.

        @param group_id: the id of the group that got moved
        @return: Nothing
        """
        raise NotImplementedError("grouping not implemented yet")
        # op = GroupMoveOperation(group_id, diff, self)
        # self.__history.do_operation(op)
        #
        # self.__timeline_view.changed.emit()

    def group_selected(self):
        """ Groups all selected timeables """
        raise NotImplementedError("grouping not implemented yet")
        # items = self.__timeline_view.get_selected_timeables()
        # ids = [i.view_id for i in items]
        #
        # self.create_group(ids)

    def get_timelineview(self):
        """ Returns the timelineview connected with the controller """
        return self.__timeline_view

    def get_timelinemodel(self):
        """ Returns the timelinemodel connected with the controller """
        return self.__timeline_model

    def update_timecode(self, timecode):
        self.__timeline_view.update_timecode(timecode)
