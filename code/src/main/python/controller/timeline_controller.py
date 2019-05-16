"""
The controller module for communication between timelineview and
timelinemodel.
"""

from model.project import Project, Operation
from model.data import TimeableModel, TimelineModel


# Todo: Fill the interface methods which translate actions from the
#       Ubicut frontend (view) to the backend (model) with some
#       function.


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

    def create_timeable(self, track_id, name, width, x_pos, model, res_left=0, res_right=0,
                        is_drag=True, mouse_pos=0):
        """
        Create a new object in the timeline model to represent a new
        timeable.

        @param data: The data needed to now what the timeable has to
                     contain and what track it has to be added to.
                     Important note: You may replace this parameter
                     with multiple ones if required while implementing
                     this method.
        @return:     Nothing.
        """
        # op = CreationOperation()
        # self.__history.do_operation(op)
        return self.__timeline_view.create_timeable(track_id, name, width, x_pos, model,
                                                    res_left=res_left, res_right=res_right,
                                                    is_drag=is_drag, mouse_pos=mouse_pos)

    def delete_timeable(self, view_info, model_info):
        """
        Delete the model's representation of a timeable.

        @param id: The timeable's unique ID.
        @return:   Nothing.
        """
        op = DeleteOperation(view_info, model_info)
        self.__history.do_operation(op)

    def remove_timeable_view(self, id):
        self.__timeline_view.remove_timeable(id)

    def rename_timeable(self, id, name):
        """
        Rename the model's representation of a timeable.

        @param id:   The timeable's unique ID.
        @param name: The new name of the timeable.
        @return:     Nothing.
        """
        pass

    def move_timeable(self, id, start):
        """
        Set a new start of the model 's representation of a timeable.

        @param id:    The timeable's unique ID.
        @param start: The new start time of the timeable.
        @return:      Nothing.
        """
        pass

    def split_timeable(self, id, pos):
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
        timeable_left = self.__timeline_view.timeables[id]
        timeable_left.resizable_right = 0

        new_model = timeable_left.model.cut(pos)
        new_model.set_layer(timeable_left.model.clip.Layer())

        self.__timeline_view.create_timeable(timeable_left.track_id, timeable_left.name,
                                             timeable_left.width - pos,
                                             pos + timeable_left.x_pos, new_model,
                                             res_right=timeable_left.resizable_right,
                                             is_drag=False)

        timeable_left.set_width(pos)
        timeable_left.setPos(timeable_left.x_pos, 0)
        timeable_left.update_handles_pos()

    def remove_timeable_part(self, id, start, end):
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
        pass

    def select_timeable(self, id, selected=True):
        """
        Set the selected-state of the model's representation of a
        timeable.

        @param id:       The timeable's unique ID.
        @param selected: The selected-state.
        @return:         Nothing.
        """
        pass

    def adjust_tracks(self):
        self.__timeline_view.adjust_track_sizes()
        self.__timeline_view.track_frame.adjustSize()


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
        model = TimeableModel(self.model_info["file_name"])
        model.set_start(self.model_info["start"], is_sec=True)
        model.set_end(self.model_info["end"], is_sec=True)
        model.move(self.model_info["position"], is_sec=True)

        new_id = TimelineController.get_instance().create_timeable(
            self.view_info["track_id"], self.view_info["name"],
            self.view_info["width"], self.view_info["x_pos"], model,
            res_left=self.view_info["resizable_left"],
            res_right=self.view_info["resizable_right"])

        self.view_info["view_id"] = new_id
        self.model_info["id"] = model.clip.Id()


class CutOperation(Operation):
    """ Cuts a timeable in two parts with do and makes it one timeable again with undo """

    def __init__(self, view_info, model_info, pos):
        self.view_info = view_info
        self.model_info = model_info
        self.pos = pos

        self.__controller = TimelineController.get_instance()

    def do(self):
        self.controller.split_timeable(self.view_info["view_id"])

    def undo(self):
        pass


class MoveOperation(Operation):
    """ Cuts a timeable in two parts with do and makes it one timeable again with undo """

    def __init__(self, view_info, model_info, pos):
        self.view_info = view_info
        self.model_info = model_info
        self.pos = pos

    def do(self):
        pass

    def undo(self):
        pass


class CreationOperation(Operation):
    """ Cuts a timeable in two parts with do and makes it one timeable again with undo """

    def __init__(self, view_info, model_info):
        self.view_info = view_info
        self.model_info = model_info

    def do(self):
        pass

    def undo(self):
        pass
