# import json
import uuid
import locale
import openshot

from .timeline import TimelineModel
from util.timeline_utils import pos_to_seconds


class TimeableModel:
    def __init__(self, file_name):
        # otherwhise there is a json parse error
        locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')

        self.clip = openshot.Clip(file_name)
        self.clip.Id(str(uuid.uuid4()))
        self.file_name = file_name

        self.timeline_instance = TimelineModel.get_instance()
        self.timeline_instance.timeline.AddClip(self.clip)

    def get_first_frame(self):
        f = self.clip.Start() \
            * (self.clip.Reader().info.fps.num / self.clip.Reader().info.fps.num) + 1

        return int(f)

    def set_layer(self, layer):
        self.clip.Layer(layer)
        data = {"layer": layer}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def trim_start(self, pos):
        """ start = start + sec(pos) """
        new_start = self.clip.Start() + pos_to_seconds(pos)
        self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def set_start(self, pos, is_sec=False):
        new_start = pos
        if is_sec:
            self.clip.Start(pos)
        else:
            new_start = pos_to_seconds(pos)
            self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def trim_end(self, pos):
        """ end = end + sec(pos) """
        new_end = self.clip.End() + pos_to_seconds(pos)
        self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def set_end(self, pos, is_sec=False):
        new_end = pos
        if is_sec:
            self.clip.End(pos)
        else:
            new_end = pos_to_seconds(pos)
            self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def cut(self, pos):
        old_end = self.clip.End()
        self.set_end(self.clip.Start() + pos_to_seconds(pos), is_sec=True)

        data = {"end": self.clip.End()}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

        new_model = TimeableModel(self.file_name)
        new_model.set_start(self.clip.End(), is_sec=True)
        new_model.set_end(old_end, is_sec=True)
        new_model.move(self.clip.Position() + pos_to_seconds(pos), is_sec=True)

        return new_model

    def move(self, pos, is_sec=False):
        new_position = pos
        if is_sec:
            self.clip.Position(new_position)
        else:
            new_position = pos_to_seconds(pos)
            self.clip.Position(new_position)

        data = {"position": new_position}
        self.timeline_instance.change("update", ["clips", {"id": self.clip.Id()}], data)

    def delete(self):
        self.timeline_instance.change("delete", ["clips", {"id": self.clip.Id()}], {})
