import locale

import openshot

from .timeline import TimelineModel
from util.timeline_utils import get_file_type, pos_to_seconds


class TimeableModel:

    # Todo: Write documentation
    def __init__(self, file_name, clip_id, is_video=None):
        # otherwhise there is a json parse error
        locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')

        self.clip = openshot.Clip(file_name)
        self.clip.Id(clip_id)

        self.is_video = is_video

        if self.is_video is not None:
            if self.is_video:
                self.clip.has_video = openshot.Keyframe(1)
                self.clip.has_audio = openshot.Keyframe(0)
            else:
                self.clip.has_video = openshot.Keyframe(0)
                self.clip.has_audio = openshot.Keyframe(1)

        self.track = None

        self.timeline_controller = None
        self.timeline_model = TimelineModel.get_instance()

        self.file_name = file_name
        self.file_type = get_file_type(self.file_name)

        # if the timeline has no clips, set some timeline data to the data of this clip
        if self.is_first_vid():
            self.set_timeline_data()

    def get_info_dict(self):
        return {
            "file_name": self.file_name,
            "id": self.clip.Id(),
            "position": self.clip.Position(),
            "start": self.clip.Start(),
            "end": self.clip.End(),
            "layer:": self.clip.Layer()
        }

    def get_id(self):
        """ Return the timeable's ID. """
        return self.clip.Id()

    def set_controller(self, controller):
        """
        Set the C{TimelineController} which the C{TimeableModel} should
        be linked to.

        @param controller: The controller.
        @type controller:  controller.TimelineController
        """
        self.timeline_controller = controller

    def set_track(self, track):
        """
        Set the track of the timeable and update its properties
        according to the track. C{track=None} means that the timeable
        should not belong to any track.

        Updated properties
        ==================
          - The layer.

            If the track's layer is C{None} the timeable's
            layer will be set to C{-1} because the Openshot layer
            parameter can't be C{None}.

        @param track: The track.
        @type track:  model.data.TrackModel
        """
        self.track = track
        layer = track.get_layer()
        if layer is not None:
            self.set_layer(layer)
        else:
            self.set_layer(-1)

    def is_first_vid(self):
        """ Returns True if this is the first video in the timeline, False otherwhise """
        if not self.clip.Reader().info.has_video:
            return False

        for c in list(self.timeline_model.timeline.Clips()):
            if c.Reader().info.has_video:
                return False

        return True

    def set_timeline_data(self):
        """ Sets the data of the timeline to data of this clip """
        fps_data = {
            "num": self.clip.Reader().info.fps.num,
            "den": self.clip.Reader().info.fps.den
        }
        self.timeline_model.change("update", ["fps", ""], fps_data)

        self.timeline_model.change(
            "update", ["width"], self.clip.Reader().info.width)
        self.timeline_model.change(
            "update", ["height"], self.clip.Reader().info.height)

    def get_first_frame(self):
        """ Returns the frame that would be seen first """
        return int((self.clip.Start() * self.clip.Reader().info.fps.ToFloat()) + 1)

    def set_layer(self, layer):
        """ Sets the layer of the clip """
        self.clip.Layer(layer)
        data = {"layer": layer}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

        if self.timeline_controller:
            self.timeline_controller.timeable_model_changed(self)

    def trim_start(self, pos):
        """ start = start + sec(pos) """
        new_start = self.clip.Start() + pos_to_seconds(pos)
        self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

        if self.timeline_controller:
            self.timeline_controller.timeable_model_changed(self)

    def set_start(self, pos, is_sec=False):
        """ Sets the start of the clip """
        new_start = pos
        if is_sec:
            self.clip.Start(pos)
        else:
            new_start = pos_to_seconds(pos)
            self.clip.Start(new_start)

        data = {"start": new_start}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

        if self.timeline_controller:
            self.timeline_controller.timeable_model_changed(self)

    def trim_end(self, pos):
        """ end = end + sec(pos) """
        new_end = self.clip.End() + pos_to_seconds(pos)
        self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

        if self.timeline_controller:
            self.timeline_controller.timeable_model_changed(self)

    def set_end(self, pos, is_sec=False):
        """ Sets the end of the clip """
        new_end = pos
        if is_sec:
            self.clip.End(pos)
        else:
            new_end = pos_to_seconds(pos)
            self.clip.End(new_end)

        data = {"end": new_end}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

        if self.timeline_controller:
            self.timeline_controller.timeable_model_changed(self)

    def move(self, pos, is_sec=False):
        """ Sets the position of the clip """
        new_position = pos
        if is_sec:
            self.clip.Position(new_position)
        else:
            new_position = pos_to_seconds(pos)
            self.clip.Position(new_position)

        data = {"position": new_position}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

        if self.timeline_controller:
            self.timeline_controller.timeable_model_changed(self)

    def corner(self, val):
        """ moves the clip to the bottom right """
        k1 = openshot.Keyframe()
        k2 = openshot.Keyframe()
        k3 = openshot.Keyframe()
        if val:
            k1.AddPoint(0, 0.25)
            k2.AddPoint(0, 0.375)
            k3.AddPoint(0, 0.375)
        else:
            k1.AddPoint(0, 1.0)
            k2.AddPoint(0, 0.0)
            k3.AddPoint(0, 0.0)

        self.clip.location_x = k2
        self.clip.location_y = k3
        self.clip.scale_x = k1
        self.clip.scale_y = k1
        self.clip.scale = openshot.SCALE_FIT

        if self.timeline_controller:
            self.timeline_controller.timeable_model_changed(self)
