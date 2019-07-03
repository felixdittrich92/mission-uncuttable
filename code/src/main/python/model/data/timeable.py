import locale

import openshot

from .timeline import TimelineModel
from util.timeline_utils import get_file_type, pos_to_seconds


class TimeableModel:
    def __init__(self, file_name, clip_id, is_video=True):
        # otherwhise there is a json parse error
        locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')

        self.clip = openshot.Clip(file_name)
        self.clip.Id(clip_id)

        self.is_video = is_video

        if self.is_video:
            self.clip.has_video = openshot.Keyframe(1)
            self.clip.has_audio = openshot.Keyframe(0)
        else:
            self.clip.has_video = openshot.Keyframe(0)
            self.clip.has_audio = openshot.Keyframe(1)
    


        

        self.file_name = file_name
        self.file_type = get_file_type(self.file_name)

        self.timeline_instance = TimelineModel.get_instance()

        # if the timeline has no clips, set some timeline data to the data of this clip
        if self.is_first_vid():
            self.set_timeline_data()

        # self.add_to_timeline()

    def get_info_dict(self):
        return {
            "file_name": self.file_name,
            "id": self.clip.Id(),
            "position": self.clip.Position(),
            "start": self.clip.Start(),
            "end": self.clip.End(),
            "layer:": self.clip.Layer()
        }

    def add_to_timeline(self):
        """ Adds the clip to the openshot timeline """
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

        self.timeline_instance.change(
            "update", ["width"], self.clip.Reader().info.width)
        self.timeline_instance.change(
            "update", ["height"], self.clip.Reader().info.height)

    def get_first_frame(self):
        """ Returns the frame that would be seen first """
        return int((self.clip.Start() * self.clip.Reader().info.fps.ToFloat()) + 1)

    def set_layer(self, layer):
        """ Sets the layer of the clip """
        self.clip.Layer(layer)
        data = {"layer": layer}
        self.timeline_instance.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    def trim_start(self, pos):
        """ start = start + sec(pos) """
        new_start = self.clip.Start() + pos_to_seconds(pos)
        self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_instance.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    def set_start(self, pos, is_sec=False):
        """ Sets the start of the clip """
        new_start = pos
        if is_sec:
            self.clip.Start(pos)
        else:
            new_start = pos_to_seconds(pos)
            self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_instance.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    def trim_end(self, pos):
        """ end = end + sec(pos) """
        new_end = self.clip.End() + pos_to_seconds(pos)
        self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_instance.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    def set_end(self, pos, is_sec=False):
        """ Sets the end of the clip """
        new_end = pos
        if is_sec:
            self.clip.End(pos)
        else:
            new_end = pos_to_seconds(pos)
            self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_instance.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    def move(self, pos, is_sec=False):
        """ Sets the position of the clip """
        new_position = pos
        if is_sec:
            self.clip.Position(new_position)
        else:
            new_position = pos_to_seconds(pos)
            self.clip.Position(new_position)

        data = {"position": new_position}
        self.timeline_instance.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    def corner(self, val):
        """ moves the clip to the bottom right """
        k1 = openshot.Keyframe()
        k2 = openshot.Keyframe()
        k3 = openshot.Keyframe()
        if val:
            k1.AddPoint(0, 0.2)
            k2.AddPoint(0, 0.4)
            k3.AddPoint(0, 0.4)
        else:
            k1.AddPoint(0, 1.0)
            k2.AddPoint(0, 0.0)
            k3.AddPoint(0, 0.0)

        self.clip.location_x = k2
        self.clip.location_y = k3
        self.clip.scale_x = k1
        self.clip.scale_y = k1
        self.clip.scale = openshot.SCALE_FIT
