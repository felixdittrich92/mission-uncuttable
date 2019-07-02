from model.project import Operation
from util.timeline_utils import pos_to_seconds


def make_timeable_model(filename, id):
    # this has to be imported here, otherwhise there are circular imports
    from model.data import TimeableModel

    return TimeableModel(filename, id)


class CreationOperation(Operation):
    """ Creates a new timeable """

    def __init__(self, track_id, name, width, x_pos, model, id,
                 res_left, res_right, mouse_pos, group, is_drag, controller):
        self.track_id = track_id
        self.name = name
        self.width = width
        self.x_pos = x_pos
        self.model = model
        self.id = id
        self.res_left = res_left
        self.res_right = res_right
        self.mouse_pos = mouse_pos
        self.group = group
        self.is_drag = is_drag
        self.controller = controller

    def do(self):
        self.model.move(self.x_pos)
        timeline_view = self.controller.get_timelineview()
        timeline_view.create_timeable(self.track_id, self.name, self.width,
                                      self.x_pos, self.model, self.id,
                                      self.res_left, self.res_right, self.group,
                                      self.mouse_pos, is_drag=self.is_drag)

    def undo(self):
        self.controller.get_timeable_by_id(self.id).delete(hist=False)


class DeleteOperation(Operation):
    """ Removes a timeable with do and creates the timeable again with undo """

    def __init__(self, view_info, model_info, controller):
        self.view_info = view_info
        self.model_info = model_info
        self.controller = controller

    def do(self):
        self.controller.remove_timeable_from_group(self.view_info["group_id"],
                                                   self.view_info["view_id"])
        self.controller.get_timelinemodel().change(
            "delete", ["clips", {"id": self.model_info["id"]}], {})
        self.controller.remove_timeable_view(self.view_info["view_id"])

    def undo(self):
        model = make_timeable_model(self.model_info["file_name"], self.model_info["id"])
        model.set_start(self.model_info["start"], is_sec=True)
        model.set_end(self.model_info["end"], is_sec=True)
        model.move(self.model_info["position"], is_sec=True)

        self.controller.create_timeable(
            self.view_info["track_id"], self.view_info["name"],
            self.view_info["width"], self.view_info["x_pos"], model,
            self.view_info["view_id"], res_left=self.view_info["resizable_left"],
            res_right=self.view_info["resizable_right"],
            group=self.view_info["group_id"], hist=False)

        self.controller.add_timeable_to_group(self.view_info["group_id"],
                                              self.view_info["view_id"])


class CutOperation(Operation):
    """ Cuts a timeable in two parts with do and makes it one timeable again with undo """

    def __init__(self, view_id, res_right, width, model_end, pos,
                 new_view_id, new_model_id, controller):
        self.view_id = view_id
        self.res_right = res_right
        self.width = width
        self.model_end = model_end
        self.pos = pos
        self.new_view_id = new_view_id
        self.new_model_id = new_model_id
        self.controller = controller

    def do(self):
        timeable_left = self.controller.get_timeable_by_id(self.view_id)
        timeable_left.resizable_right = 0

        model_left = timeable_left.model
        model_left.set_end(model_left.clip.Start()
                           + pos_to_seconds(self.pos), is_sec=True)

        new_model = make_timeable_model(model_left.file_name, self.new_model_id)
        new_model.set_start(model_left.clip.End(), is_sec=True)
        new_model.set_end(self.model_end, is_sec=True)
        new_model.move(model_left.clip.Position() + pos_to_seconds(self.pos),
                       is_sec=True)
        new_model.set_layer(timeable_left.model.clip.Layer())

        self.controller.create_timeable(timeable_left.track_id, timeable_left.name,
                                        timeable_left.width - self.pos,
                                        self.pos + timeable_left.x_pos, new_model,
                                        self.new_view_id, hist=False,
                                        res_right=timeable_left.resizable_right)

        timeable_left.set_width(self.pos)
        timeable_left.setPos(timeable_left.x_pos, 0)
        timeable_left.update_handles_pos()

    def undo(self):
        timeable_right = self.controller.get_timeable_by_id(
            self.new_view_id)
        timeable_right.delete(hist=False)

        timeable_left = self.controller.get_timeable_by_id(self.view_id)
        timeable_left.resizable_right = self.res_right
        timeable_left.set_width(self.width)
        timeable_left.setPos(timeable_left.x_pos, 0)
        timeable_left.update_handles_pos()
        timeable_left.model.set_end(self.model_end, is_sec=True)


class MoveOperation(Operation):
    """ Moves a timeable on its track """

    def __init__(self, view_id, old_pos, new_pos, controller):
        self.view_id = view_id
        self.old_pos = old_pos
        self.new_pos = new_pos
        self.controller = controller

    def do(self):
        timeable = self.controller.get_timeable_by_id(self.view_id)

        # set timeableview position
        timeable.do_move(self.new_pos)
        # set clip position on the timeline in seconds
        timeable.model.move(self.new_pos)

    def undo(self):
        timeable = self.controller.get_timeable_by_id(self.view_id)

        # set timeableview position
        timeable.do_move(self.old_pos)
        # set clip position on the timeline in seconds
        timeable.model.move(self.old_pos)


class ResizeOperation(Operation):
    """ Resizes a timeable """

    def __init__(self, view_info_old, view_info_new, controller):
        self.view_id = view_info_old["view_id"]
        self.view_info_old = view_info_old
        self.view_info_new = view_info_new
        self.controller = controller

        if self.view_info_old["resizable_left"] != self.view_info_new["resizable_left"]:
            self.diff = (self.view_info_old["resizable_left"]
                         - self.view_info_new["resizable_left"])
            self.start = True
        else:
            self.diff = (self.view_info_old["resizable_right"]
                         - self.view_info_new["resizable_right"])
            self.start = False

    def do(self):
        timeable = self.controller.get_timeable_by_id(self.view_id)

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
        timeable = self.controller.get_timeable_by_id(self.view_id)

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

    def __init__(self, view_info_old, view_info_new, model_old, model_new, controller):
        self.view_info_old = view_info_old
        self.view_info_new = view_info_new
        self.model_old = model_old
        self.model_old.move(self.view_info_old["x_pos"])
        self.model_new = model_new
        self.was_created = True
        self.controller = controller

    def do(self):
        if self.was_created:
            return

        self.controller.create_timeable(
            self.view_info_new["track_id"], self.view_info_new["name"],
            self.view_info_new["width"], self.view_info_new["x_pos"], self.model_new,
            self.view_info_new["view_id"], res_left=self.view_info_new["resizable_left"],
            res_right=self.view_info_new["resizable_right"],
            group=self.view_info_new["group_id"], hist=False)
        self.controller.delete_timeable(
            self.view_info_old, self.model_old.get_info_dict(), hist=False)

    def undo(self):
        self.controller.create_timeable(
            self.view_info_old["track_id"], self.view_info_old["name"],
            self.view_info_old["width"], self.view_info_old["x_pos"], self.model_old,
            self.view_info_old["view_id"], res_left=self.view_info_old["resizable_left"],
            res_right=self.view_info_old["resizable_right"],
            group=self.view_info_old["group_id"], hist=False)
        self.controller.delete_timeable(
            self.view_info_new, self.model_new.get_info_dict(), hist=False)
        self.was_created = False


class GroupMoveOperation(Operation):
    """ Moves a TimeableGroup """

    def __init__(self, group_id, diff, controller):
        self.group_id = group_id
        self.diff = diff
        self.was_moved = True
        self.controller = controller

    def do(self):
        group = self.controller.get_group_by_id(self.group_id)
        for t in group.timeables:
            if not self.was_moved:
                t.do_move(t.x_pos + self.diff)

            t.model.move(t.x_pos)

        self.was_moved = False

    def undo(self):
        group = self.controller.get_group_by_id(self.group_id)
        for t in group.timeables:
            t.do_move(t.x_pos - self.diff)
            t.model.move(t.x_pos)


class CreateTrackOperation(Operation):
    """ Creates a new Track """

    def __init__(self, track_id, name, width, height, index, is_video, controller):
        self.track_id = track_id
        self.name = name
        self.width = width
        self.height = height
        self.index = index
        self.is_video = is_video
        self.controller = controller

    def do(self):
        if self.is_video:
            self.controller.create_video_track(
                self.name, self.width, self.height, self.track_id, index=self.index)
        else:
            self.controller.create_audio_track(
                self.name, self.width, self.height, self.track_id, index=self.index)

    def undo(self):
        self.controller.get_timelinemodel().remove_track(self.track_id)
        self.controller.get_timelineview().remove_track(self.track_id)


class DeleteTrackOperation(Operation):
    """ Removes a Track """

    def __init__(self, track_id, track_data, timeable_data, index, controller):
        """
        @param track_id: number of the track that will be removed
        @param track_data: dictionary with all the infos of the TrackView
        @param timeable_data: list of dictionaries with data for
                              every Timeable on this track
        """
        self.track_id = track_id
        self.track_data = track_data
        self.timeable_data = timeable_data
        self.index = index
        self.controller = controller

    def do(self):
        # removes clips from timeline model
        self.controller.get_timelinemodel().remove_track(self.track_id)

        # remove track view
        self.controller.get_timelineview().remove_track(self.track_id)

    def undo(self):
        if self.track_data["type"]:
            self.controller.create_video_track(
                self.track_data["name"], self.track_data["width"],
                self.track_data["height"], self.track_data["num"], index=self.index,
                is_overlay=self.track_data["is_overlay"])
        else:
            self.controller.create_audio_track(
                self.track_data["name"], self.track_data["width"],
                self.track_data["height"], self.track_data["num"], index=self.index)

        for t in self.timeable_data:
            m = t["model"]
            model = make_timeable_model(m["file_name"], m["id"])
            model.set_start(m["start"], is_sec=True)
            model.set_end(m["end"], is_sec=True)
            model.move(m["position"], is_sec=True)

            self.controller.create_timeable(
                self.track_id, t["name"], t["width"], t["x_pos"], model, t["view_id"],
                res_left=t["resizable_left"], res_right=t["resizable_right"],
                group=t["group_id"], hist=False)
