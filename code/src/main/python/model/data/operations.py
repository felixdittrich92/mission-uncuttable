# Todo: Add calls to superclass Operation in its subclasses here.

# Todo: Implement RenameOperation
# Todo: Implement GroupOperation
# Todo: Implement UngroupOperation
# Todo: Implement SetOverlayOperation
# Todo: Implement SetVolumeOperation

from model.project import Operation
from model.data import TimeableModel, TrackModel
from config import Settings
from util.timeline_utils import pos_to_seconds, generate_id


# def make_timeable_model(filename, id):
#     # this has to be imported here, otherwhise there are circular imports
#     from model.data import TimeableModel
#
#     return TimeableModel(id, filename)


class CreationOperation(Operation):
    """ Creates a new timeable """

    def __init__(self, filepath, track_id, name, x_pos, timeline_model):
        self.filepath = filepath
        self.track_id = track_id
        self.name = name
        self.x_pos = x_pos
        self.timeline_model = timeline_model

        # self.timeable_models = dict()  # {id: TimeableModel}
        self.timeable_model = None

    def do(self):
        # if Settings.get_instance().get_dict_settings()["general"]["autoaudio"]["current"]:
        #     raise(NotImplementedError("Autoaudio is not implemented yet."))
        #     # timeable_id_video = generate_id()
        #     # self.timeable_models[timeable_id_video]\
        #     #     = TimeableModel(timeable_id_video, self.filepath, self.name, True)
        #     # timeable_id_audio = generate_id()
        #     # self.timeable_models[timeable_id_audio]\
        #     #     = TimeableModel(timeable_id_audio, self.filepath, self.name, False)
        # else:
        timeable_id = generate_id()
        self.timeable_model\
            = TimeableModel(timeable_id, self.filepath, self.name)
        self.timeable_model.move(
            self.timeline_model.track_id_map[self.track_id],
            self.x_pos
        )

        # Controller should already get notified when a TimeableModel is added
        # to the TimelineModel. Therefore deactivate this code:
        # timeline_view = self.controller.get_timelineview()
        # timeline_view.create_timeable(None, self.track_id, self.name, self.x_pos, self.res_left, self.res_right,
        #                               self.mouse_pos)

    def undo(self):
        self.timeable_model.remove()


class DeleteOperation(Operation):
    """ Removes a timeable with do and creates the timeable again with undo """

    def __init__(self, timeable_id, timeline_model):
        self.timeable_id = timeable_id
        self.timeline_model = timeline_model

        self.timeable_model = None
        self.position = None
        self.track = None
        """
        The deleted C{TimeableModel}. None if the operation has not been
        done yet. Remembering the object itself and not only a few
        properties of it is needed because C{undo} has to recover the
        exact state from before C{do} was executed.
        """
        self.is_done = False

    def do(self):
        if self.is_done:
            raise RuntimeError(
                "Can't do DeleteOperation because it has already been done.")
        else:
            try:
                self.timeable_model = self.timeline_model\
                    .get_timeables()[self.timeable_id]
            except KeyError as E:
                raise KeyError(
                    "Timeable doesn't exist in the TimelineModel: ID={}"
                    .format(self.timeable_id)
                ) from E
            else:
                self.position = self.timeable_model.get_position()
                self.track = self.timeable_model.track
                self.timeable_model.remove()
                self.is_done = True

        # self.timeline_controller.ungroup(self.view_info["view_id"])
        # self.timeline_controller.get_timelinemodel().change(
        #     "delete", ["clips", {"id": self.model_info["id"]}], {})
        # self.timeline_controller.remove_timeable_view(self.view_info["view_id"])
        # self.timeline_controller.get_timelinemodel().update_duration()

    def undo(self):
        if not self.is_done:
            raise RuntimeError(
                "Can't undo DeleteOperation because it has not been done yet.")
        else:
            self.timeable_model.move(self.track, self.position)
            self.is_done = False
        # model = make_timeable_model(self.model_info["file_name"], self.model_info["id"])
        # model.set_start(self.model_info["start"], is_sec=True)
        # model.set_end(self.model_info["end"], is_sec=True)
        # model.move(self.model_info["position"], is_sec=True)
        #
        # self.timeline_controller.create_timeable(None, self.view_info["track_id"], self.view_info["name"], 50,
        #                                          self.view_info["x_pos"],,,
        #
        # self.timeline_controller.add_timeable_to_group(self.view_info["group_id"],
        #                                                self.view_info["view_id"])


class CutOperation(Operation):
    """ Cuts a timeable in two parts with do and makes it one timeable again with undo """

    def __init__(self, timeable_id, pos, timeline_model):
        self.timeable_id = timeable_id
        self.pos = pos
        self.timeline_model = timeline_model

        self.first_part = None
        self.second_part = None

    def do(self):
        try:
            self.first_part =\
                self.timeline_model.get_timeables()[self.timeable_id]
        except KeyError as E:
            raise KeyError(
                    "Timeable doesn't exist in the TimelineModel: ID={}"
                    .format(self.timeable_id)
                ) from E
        else:
            pos_untrimmed = self.pos + self.first_part.get_trim_start()
            self.second_part \
                = TimeableModel(generate_id(), self.first_part.file_path, "Part two")
            self.second_part.set_trim_start(pos_untrimmed)
            self.second_part.set_trim_end(self.first_part.get_trim_end())
            # The parameter to trim_end currently has to be negative
            #  to remove frames. Will be changed in the future.
            self.first_part.trim_end(
                -(self.first_part.get_length() - self.pos))
            self.second_part.move(
                self.first_part.track,
                self.first_part.get_end() + 1
            )

    def undo(self):
        original_end = self.second_part.get_end()
        self.second_part.remove()
        self.first_part.set_trim_end(original_end)


class MoveOperation(Operation):
    """Operation which moves a C{TimeableModel} in a C{TimelineModel}"""

    def __init__(self, timeable_id, track_id, pos, timeline_model):
        self.timeable_id = timeable_id
        self.track_id = track_id
        self.pos = pos
        self.timeline_model = timeline_model

        self.timeable = None
        self.original_track = None
        self.original_pos = None

    def do(self):
        try:
            self.timeable\
                = self.timeline_model.get_timeables()[self.timeable_id]
        except KeyError as E:
            raise KeyError(
                    "Timeable doesn't exist in the TimelineModel: ID={}"
                    .format(self.timeable_id)
                ) from E
        else:
            try:
                track = self.timeline_model.track_id_map[self.track_id]
            except KeyError as E:
                raise KeyError(
                        "Track doesn't exist in the TimelineModel: ID={}"
                        .format(self.track_id)
                    ) from E
            else:
                self.original_track = self.timeable.track
                self.original_pos = self.timeable.get_position()
                self.timeable.move(track, self.pos)

    def undo(self):
        self.timeable.move(self.original_track, self.original_pos)


class TrimStartOperation(Operation):
    """Operation which trims the start of a timeable."""

    def __init__(self, timeable_id, trim_length, timeline_model):
        self.timeable_id = timeable_id
        self.trim_length = trim_length
        self.timeline_model = timeline_model

        self.timeable = None

    def do(self):
        try:
            self.timeable\
                = self.timeline_model.get_timeables()[self.timeable_id]
        except KeyError as E:
            raise KeyError(
                    "Timeable doesn't exist in the TimelineModel: ID={}"
                    .format(self.timeable_id)
                ) from E
        else:
            self.timeable.trim_start(self.trim_length)

    def undo(self):
        self.timeable.trim_start(-self.trim_length)


class TrimEndOperation(Operation):
    """Operation which trims the start of a timeable."""

    def __init__(self, timeable_id, trim_length, timeline_model):
        self.timeable_id = timeable_id
        self.trim_length = trim_length
        self.timeline_model = timeline_model

        self.timeable = None

    def do(self):
        try:
            self.timeable\
                = self.timeline_model.get_timeables()[self.timeable_id]
        except KeyError as E:
            raise KeyError(
                    "Timeable doesn't exist in the TimelineModel: ID={}"
                    .format(self.timeable_id)
                ) from E
        else:
            self.timeable.trim_end(self.trim_length)

    def undo(self):
        self.timeable.trim_end(-self.trim_length)


# class ResizeOperation(Operation):
#     """ Resizes a timeable """
#
#     def __init__(self, view_info_old, view_info_new, controller):
#         self.view_id = view_info_old["view_id"]
#         self.view_info_old = view_info_old
#         self.view_info_new = view_info_new
#         self.controller = controller
#
#         if self.view_info_old["resizable_left"] != self.view_info_new["resizable_left"]:
#             self.diff = (self.view_info_old["resizable_left"]
#                          - self.view_info_new["resizable_left"])
#             self.start = True
#         else:
#             self.diff = (self.view_info_old["resizable_right"]
#                          - self.view_info_new["resizable_right"])
#             self.start = False
#
#     def do(self):
#         timeable = self.controller.get_timeable_by_id(self.view_id)
#
#         timeable.resizable_left = self.view_info_new["resizable_left"]
#         timeable.resizable_right = self.view_info_new["resizable_right"]
#
#         timeable.prepareGeometryChange()
#         timeable.width = self.view_info_new["width"]
#
#         if self.start:
#             timeable.x_pos = self.view_info_new["x_pos"]
#             timeable.setPos(timeable.x_pos, 0)
#             timeable.model.trim_start(self.diff)
#             timeable.model.move(None, timeable.x_pos)
#         else:
#             timeable.model.trim_end(self.diff)
#
#         timeable.setRect(timeable.boundingRect())
#
#     def undo(self):
#         timeable = self.controller.get_timeable_by_id(self.view_id)
#
#         timeable.resizable_left = self.view_info_old["resizable_left"]
#         timeable.resizable_right = self.view_info_old["resizable_right"]
#
#         timeable.prepareGeometryChange()
#         timeable.width = self.view_info_old["width"]
#
#         if self.start:
#             timeable.x_pos = self.view_info_old["x_pos"]
#             timeable.setPos(timeable.x_pos, 0)
#             timeable.model.trim_start(-self.diff)
#             timeable.model.move(None, timeable.x_pos)
#         else:
#             timeable.model.trim_end(-self.diff)
#
#         timeable.setRect(timeable.boundingRect())


# class DragOperation(Operation):
#     """ Moves a timeable to another track """
#
#     def __init__(self, view_info_old, view_info_new, model_old, model_new, controller):
#         self.view_info_old = view_info_old
#         self.view_info_new = view_info_new
#         self.model_old = model_old
#         self.model_old.move(None, self.view_info_old["x_pos"])
#         self.model_new = model_new
#         self.was_created = True
#         self.controller = controller
#
#     def do(self):
#         if self.was_created:
#             return
#
#         self.controller.create_timeable(None, self.view_info_new["track_id"], self.view_info_new["name"], 50,
#                                         self.view_info_new["x_pos"],,,
#         self.controller.delete_timeable(None, hist=False)
#
#     def undo(self):
#         self.controller.create_timeable(None, self.view_info_old["track_id"], self.view_info_old["name"], 50,
#                                         self.view_info_old["x_pos"],,,
#         self.controller.delete_timeable(None, hist=False)
#         self.was_created = False


# Todo: Implement something with groups
# class GroupMoveOperation(Operation):
#     """ Moves a TimeableGroup """
#
#     def __init__(self, group_id, diff, controller):
#         self.group_id = group_id
#         self.diff = diff
#         self.was_moved = True
#         self.controller = controller
#
#     def do(self):
#         group = self.controller.get_group_by_id(self.group_id)
#         for t in group.timeables:
#             if not self.was_moved:
#                 t.do_move(t.x_pos + self.diff)
#
#             t.model.move(None, t.x_pos)
#
#         self.was_moved = False
#
#     def undo(self):
#         group = self.controller.get_group_by_id(self.group_id)
#         for t in group.timeables:
#             t.do_move(t.x_pos - self.diff)
#             t.model.move(None, t.x_pos)


class CreateTrackOperation(Operation):
    """ Creates a new Track """

    def __init__(self, name, layer, timeline_model):
        self.name = name
        self.layer = layer
        self.timeline_model = timeline_model

        self.track = None

    def do(self):
        self.track = TrackModel(generate_id(), self.name)
        self.track.move(self.timeline_model, self.layer)

    def undo(self):
        self.track.remove()


class DeleteTrackOperation(Operation):
    """ Removes a Track """

    def __init__(self, track_id, timeline_model):
        """Init the C{DeleteTrackOperation}.

        @param track_id:       The ID of the track to be deleted.
        @param timeline_model: The C{TimelineModel} which the track
                               belongs to.
        @type timeline_model:  model.data.TimelineModel
        """
        self.track_id = track_id
        self.timeline_model = timeline_model

        self.track = None
        self.layer = None

    def do(self):
        try:
            self.track = self.timeline_model.track_id_map[self.track_id]
        except KeyError as E:
            raise KeyError(
                    "Track doesn't exist in the TimelineModel: ID={}"
                    .format(self.track_id)
                ) from E
        else:
            self.track.remove()

    def undo(self):
        self.track.move(self.timeline_model, self.layer)
