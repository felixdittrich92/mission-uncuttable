import locale

import openshot

from .timeline import TimelineModel
from controller.timeline_controller import TimelineController
from model.project import Operation, Project


class TimeableModel:
    def __init__(self, file_name):
        # otherwhise there is a json parse error
        locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')

        self.clip = openshot.Clip(file_name)
        self.clip.Id(TimelineController.generate_id())

        self.file_name = file_name
        self.file_type = TimelineController.get_file_type(self.file_name)

        self.timeline_instance = TimelineModel.get_instance()
        self.project_history = Project.get_instance().get_history()

        # if the timeline has no clips, set some timeline data to the data of this clip
        if self.is_first_vid():
            self.set_timeline_data()

        self.add_to_timeline()

    def get_info_dict(self):
        return {
            "file_name": self.file_name,
            "id": self.clip.Id(),
            "position": self.clip.Position(),
            "start": self.clip.Start(),
            "end": self.clip.End()
        }

    def add_to_timeline(self):
        self.timeline_instance.timeline.AddClip(self.clip)

    def is_first_vid(self):
        """ Returns True if this is the first video in the timeline, False otherwhise """
        if not self.clip.Reader().info.has_video:
            return False

        for c in list(self.timeline_instance.timeline.Clips()):
            if c.Reader().info.has_video:
                return False

        return True

    def set_timeline_data(self):
        """ Sets the data of the timeline to data of this clip """
        fps_data = {
            "num": self.clip.Reader().info.fps.num,
            "den": self.clip.Reader().info.fps.den
        }
        self.timeline_instance.change("update", ["fps", ""], fps_data)

        self.timeline_instance.change("update", ["width"], self.clip.Reader().info.width)
        self.timeline_instance.change("update", ["height"], self.clip.Reader().info.height)

    def get_first_frame(self):
        """ Returns the frame that would be seen first """
        return int((self.clip.Start() * self.clip.Reader().info.fps.ToFloat()) + 1)

    def set_layer(self, layer):
        """ Sets the layer of the clip """
        self.clip.Layer(layer)
        data = {"layer": layer}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def trim_start(self, pos):
        """ start = start + sec(pos) """
        new_start = self.clip.Start() + TimelineController.pos_to_seconds(pos)
        self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def set_start(self, pos, is_sec=False):
        """ Sets the start of the clip """
        new_start = pos
        if is_sec:
            self.clip.Start(pos)
        else:
            new_start = TimelineController.pos_to_seconds(pos)
            self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def trim_end(self, pos):
        """ end = end + sec(pos) """
        new_end = self.clip.End() + TimelineController.pos_to_seconds(pos)
        self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def set_end(self, pos, is_sec=False):
        """ Sets the end of the clip """
        new_end = pos
        if is_sec:
            self.clip.End(pos)
        else:
            new_end = TimelineController.pos_to_seconds(pos)
            self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def cut(self, pos):
        """ Sets the end of the clip to pos and creates a new clip starting from there """
        old_end = self.clip.End()
        self.set_end(self.clip.Start() + TimelineController.pos_to_seconds(pos), is_sec=True)

        data = {"end": self.clip.End()}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

        new_model = TimeableModel(self.file_name)
        new_model.set_start(self.clip.End(), is_sec=True)
        new_model.set_end(old_end, is_sec=True)
        new_model.move(self.clip.Position() + TimelineController.pos_to_seconds(pos),
                       is_sec=True)

        return new_model

    def move(self, pos, is_sec=False):
        """ Sets the position of the clip """
        new_position = pos
        if is_sec:
            self.clip.Position(new_position)
        else:
            new_position = TimelineController.pos_to_seconds(pos)
            self.clip.Position(new_position)

        data = {"position": new_position}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def delete(self, view_info):
        """ Removes the clip from the timeline """
        # self.timeline_instance.change("delete", ["clips", {"id": self.clip.Id()}], {})

        op = DeleteOperation(view_info, self.get_info_dict())
        self.project_history.do_operation(op)


class CutOperation(Operation):
    def __init__(self, view_info, model_info):
        self.view_info = view_info
        self.model_info = model_info

    def do(self):
        pass

    def undo(self):
        pass


class DeleteOperation(Operation):
    def __init__(self, view_info, model_info):
        self.view_info = view_info
        self.model_info = model_info

    def do(self):
        TimelineModel.get_instance().change(
            "delete", ["clips", {"id": self.model_info["id"]}], {})
        TimelineController.get_instance().delete_timeable(self.view_info["view_id"])

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
