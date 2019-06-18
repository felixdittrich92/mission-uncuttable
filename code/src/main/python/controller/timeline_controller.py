"""
The controller module for communication between timelineview and
timelinemodel.
"""

import os

from model.project import Project, Operation
from model.data import TimeableModel, TimelineModel
from util.timeline_utils import generate_id, pos_to_seconds, seconds_to_pos


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
        self.__history = Project.get_instance().get_history()

    def create_timeable(self, track_id, name, width, x_pos, model, id,
                        res_left=0, res_right=0, mouse_pos=0, hist=True, is_drag=False):
        """
        Create a new object in the timeline model to represent a new timeable.

        @param data: The data needed to now what the timeable has to
                     contain and what track it has to be added to.
                     Important note: You may replace this parameter
                     with multiple ones if required while implementing
                     this method.
        @return:     Nothing.
        """
        op = CreationOperation(track_id, name, width, x_pos, model, id,
                               res_left, res_right, mouse_pos, is_drag)

        if hist:
            self.__history.do_operation(op)
        else:
            op.do()

    def delete_timeable(self, view_info, model_info, hist=True):
        """
        Delete the model's representation of a timeable.

        @param id: The timeable's unique ID.
        @return:   Nothing.
        """
        op = DeleteOperation(view_info, model_info)
        if hist:
            self.__history.do_operation(op)
        else:
            op.do()

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
        op = MoveOperation(id, old_pos, new_pos)
        self.__history.do_operation(op)

    def drag_timeable(self, view_info_old, view_info_new, model_old, model_new):
        """
        Drags a timeable from one track to another track
        """
        op = DragOperation(view_info_old, view_info_new, model_old, model_new)
        self.__history.do_operation(op)

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
        op = CutOperation(view_id, res_right, width, model_end, pos)
        self.__history.do_operation(op)

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
        op = ResizeOperation(view_info_old, view_info_new)
        self.__history.do_operation(op)

    def is_overlay_track(self, track_id):
        if track_id not in self.__timeline_view.tracks:
            return False

        return self.__timeline_view.tracks[track_id].is_overlay

    def create_track(self, name, width, height, num, is_overlay=False):
        """ Creates a new track in the timeline """
        self.__timeline_view.create_track(name, width, height, num, is_overlay)

    def get_project_timeline(self):
        """ Returns a dict with the data needed to recreate the timeline """
        data = {
            "tracks": [],
            "timeables": []
        }

        for tr in self.__timeline_view.tracks.values():
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
            self.create_track(t["name"], t["width"], t["height"], t["num"])

        for t in data["timeables"]:
            m = t["model"]
            model = TimeableModel(m["file_name"], m["id"])
            model.set_start(m["start"], is_sec=True)
            model.set_end(m["end"], is_sec=True)
            model.move(m["position"], is_sec=True)

            self.create_timeable(t["track_id"], t["name"], t["width"], t["x_pos"],
                                 model, t["view_id"], res_left=t["resizable_left"],
                                 res_right=t["resizable_right"], hist=False)

    def create_default_tracks(self):
        """ Creates 3 default tracks when the user chooses manual cut """
        self.create_track("Track 1", 2000, 50, 2)
        self.create_track("Track 2", 2000, 50, 1)
        self.create_track("Track 3", 2000, 50, 0)

    def create_autocut_tracks(self):
        """
        Creates tracks for overlay, board, visualizer, audio when user chooses autocut
        """
        self.create_track("Overlay", 2000, 50, 3, is_overlay=True)
        self.create_track("Tafel", 2000, 50, 2)
        self.create_track("Visualizer", 2000, 50, 1)
        self.create_track("Folien", 2000, 50, 0)
        self.create_track("Audio", 2000, 50, -1)

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

    def adjust_tracks(self):
        """ Adjusts the track sizes so they all have the same length """
        self.__timeline_view.adjust_track_sizes()
        self.__timeline_view.track_frame.adjustSize()

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

    def get_timelineview(self):
        """ Returns the timelineview connected with the controller """
        return self.__timeline_view

    def update_timecode(self, timecode):
        self.__timeline_view.update_timecode(timecode)


class CreationOperation(Operation):
    """ Creates a new timeable """

    def __init__(self, track_id, name, width, x_pos, model, id,
                 res_left, res_right, mouse_pos, is_drag):
        self.track_id = track_id
        self.name = name
        self.width = width
        self.x_pos = x_pos
        self.model = model
        self.id = id
        self.res_left = res_left
        self.res_right = res_right
        self.mouse_pos = mouse_pos
        self.is_drag = is_drag

    def do(self):
        self.model.move(self.x_pos)
        timeline_view = TimelineController.get_instance().get_timelineview()
        timeline_view.create_timeable(self.track_id, self.name, self.width,
                                      self.x_pos, self.model, self.id,
                                      res_left=self.res_left, res_right=self.res_right,
                                      mouse_pos=self.mouse_pos, is_drag=self.is_drag)

    def undo(self):
        TimelineController.get_instance().get_timeable_by_id(self.id).delete(hist=False)


class DeleteOperation(Operation):
    """ Removes a timeable with do and creates the timeable again with undo """

    def __init__(self, view_info, model_info):
        self.view_info = view_info
        self.model_info = model_info

    def do(self):
        TimelineModel.get_instance().change(
            "delete", ["clips", {"id": self.model_info["id"]}], {})
        TimelineController.get_instance().remove_timeable_view(
            self.view_info["view_id"])

    def undo(self):
        model = TimeableModel(
            self.model_info["file_name"], self.model_info["id"])
        model.set_start(self.model_info["start"], is_sec=True)
        model.set_end(self.model_info["end"], is_sec=True)
        model.move(self.model_info["position"], is_sec=True)

        TimelineController.get_instance().create_timeable(
            self.view_info["track_id"], self.view_info["name"],
            self.view_info["width"], self.view_info["x_pos"], model,
            self.view_info["view_id"],
            res_left=self.view_info["resizable_left"],
            res_right=self.view_info["resizable_right"], hist=False)


class CutOperation(Operation):
    """ Cuts a timeable in two parts with do and makes it one timeable again with undo """

    def __init__(self, view_id, res_right, width, model_end, pos):
        self.view_id = view_id
        self.res_right = res_right
        self.width = width
        self.model_end = model_end
        self.pos = pos
        self.new_view_id = generate_id()
        self.new_model_id = generate_id()

    def do(self):
        controller = TimelineController.get_instance()
        timeable_left = controller.get_timeable_by_id(self.view_id)
        timeable_left.resizable_right = 0

        model_left = timeable_left.model
        model_left.set_end(model_left.clip.Start()
                           + pos_to_seconds(self.pos), is_sec=True)

        new_model = TimeableModel(model_left.file_name, self.new_model_id)
        new_model.set_start(model_left.clip.End(), is_sec=True)
        new_model.set_end(self.model_end, is_sec=True)
        new_model.move(model_left.clip.Position() + pos_to_seconds(self.pos),
                       is_sec=True)
        new_model.set_layer(timeable_left.model.clip.Layer())

        controller.create_timeable(timeable_left.track_id, timeable_left.name,
                                   timeable_left.width - self.pos,
                                   self.pos + timeable_left.x_pos, new_model,
                                   self.new_view_id,
                                   res_right=timeable_left.resizable_right,
                                   hist=False)

        timeable_left.set_width(self.pos)
        timeable_left.setPos(timeable_left.x_pos, 0)
        timeable_left.update_handles_pos()

    def undo(self):
        controller = TimelineController.get_instance()
        timeable_right = controller.get_timeable_by_id(
            self.new_view_id)
        timeable_right.delete(hist=False)

        timeable_left = controller.get_timeable_by_id(self.view_id)
        timeable_left.resizable_right = self.res_right
        timeable_left.set_width(self.width)
        timeable_left.setPos(timeable_left.x_pos, 0)
        timeable_left.update_handles_pos()
        timeable_left.model.set_end(self.model_end, is_sec=True)


class MoveOperation(Operation):
    """ Moves a timeable on its track """

    def __init__(self, view_id, old_pos, new_pos):
        self.view_id = view_id
        self.old_pos = old_pos
        self.new_pos = new_pos

    def do(self):
        timeable = TimelineController.get_instance().get_timeable_by_id(self.view_id)

        # set timeableview position
        timeable.x_pos = self.new_pos
        timeable.setPos(timeable.x_pos, 0)
        # set clip position on the timeline in seconds
        timeable.model.move(self.new_pos)

    def undo(self):
        timeable = TimelineController.get_instance().get_timeable_by_id(self.view_id)

        # set timeableview position
        timeable.x_pos = self.old_pos
        timeable.setPos(timeable.x_pos, 0)
        # set clip position on the timeline in seconds
        timeable.model.move(self.old_pos)


class ResizeOperation(Operation):
    """ Resizes a timeable """

    def __init__(self, view_info_old, view_info_new):
        self.view_id = view_info_old["view_id"]
        self.view_info_old = view_info_old
        self.view_info_new = view_info_new

        if self.view_info_old["resizable_left"] != self.view_info_new["resizable_left"]:
            self.diff = (self.view_info_old["resizable_left"]
                         - self.view_info_new["resizable_left"])
            self.start = True
        else:
            self.diff = (self.view_info_old["resizable_right"]
                         - self.view_info_new["resizable_right"])
            self.start = False

    def do(self):
        timeable = TimelineController.get_instance().get_timeable_by_id(self.view_id)

        timeable.resizable_left = self.view_info_new["resizable_left"]
        timeable.resizable_right = self.view_info_new["resizable_right"]

        timeable.prepareGeometryChange()
        timeable.width = self.view_info_new["width"]

        if self.start:
            timeable.x_pos = self.view_info_new["x_pos"]
            timeable.setPos(timeable.x_pos, 0)
            timeable.model.trim_start(self.diff)
            timeable.model.move(timeable.x_pos)
        else:
            timeable.model.trim_end(self.diff)

        timeable.setRect(timeable.boundingRect())

    def undo(self):
        timeable = TimelineController.get_instance().get_timeable_by_id(self.view_id)

        timeable.resizable_left = self.view_info_old["resizable_left"]
        timeable.resizable_right = self.view_info_old["resizable_right"]

        timeable.prepareGeometryChange()
        timeable.width = self.view_info_old["width"]

        if self.start:
            timeable.x_pos = self.view_info_old["x_pos"]
            timeable.setPos(timeable.x_pos, 0)
            timeable.model.trim_start(-self.diff)
            timeable.model.move(timeable.x_pos)
        else:
            timeable.model.trim_end(-self.diff)

        timeable.setRect(timeable.boundingRect())


class DragOperation(Operation):
    """ Moves a timeable to another track """

    def __init__(self, view_info_old, view_info_new, model_old, model_new):
        self.view_info_old = view_info_old
        self.view_info_new = view_info_new
        self.model_old = model_old
        self.model_old.move(self.view_info_old["x_pos"])
        self.model_new = model_new
        self.was_created = True

    def do(self):
        if self.was_created:
            return

        controller = TimelineController.get_instance()
        controller.create_timeable(
            self.view_info_new["track_id"], self.view_info_new["name"],
            self.view_info_new["width"], self.view_info_new["x_pos"], self.model_new,
            self.view_info_new["view_id"], res_left=self.view_info_new["resizable_left"],
            res_right=self.view_info_new["resizable_right"], hist=False)
        controller.delete_timeable(
            self.view_info_old, self.model_old.get_info_dict(), hist=False)

    def undo(self):
        controller = TimelineController.get_instance()
        controller.create_timeable(
            self.view_info_old["track_id"], self.view_info_old["name"],
            self.view_info_old["width"], self.view_info_old["x_pos"], self.model_old,
            self.view_info_old["view_id"], res_left=self.view_info_old["resizable_left"],
            res_right=self.view_info_old["resizable_right"], hist=False)
        controller.delete_timeable(
            self.view_info_new, self.model_new.get_info_dict(), hist=False)
        self.was_created = False
