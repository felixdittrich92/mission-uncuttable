import locale

import openshot

from .timeline import TimelineModel
from util.timeline_utils import get_file_type, pos_to_seconds, frames_to_seconds
from projectconfig.projectsettings import Projectsettings


class TimeableModel:
    def __init__(self, file_name, clip_id):
        # otherwhise there is a js on parse error
        locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')

        self.clip = openshot.Clip(file_name)
        self.clip.Id(clip_id)

        self.file_name = file_name
        self.file_type = get_file_type(self.file_name)

        self.__project_settings = Projectsettings.get_instance()
        self.timeline_model = TimelineModel.get_instance()

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
        self.timeline_model.timeline.AddClip(self.clip)

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

    def trim_start(self, trim_frames):
        """
        Trim the timeable's start by a number of frames.

        @param trim_frames: The number of frames to remove.
        @return:            Nothing
        """
        fps = self.timeline_model.get_fps()
        trim_seconds = frames_to_seconds(trim_frames, fps)
        start_seconds = self.clip.Start() + trim_seconds
        self.set_start(start_seconds, is_sec=True)

    def set_start(self, start, is_sec=False):
        """
        Set the start time of the timeable in frames or seconds.

        @param start:  The new start time in frames or seconds
        @param is_sec: Specifies if the start is given in frames or in
                       seconds. False means frames and True means
                       seconds.
        @return:       Nothing
        """
        if is_sec:
            start_seconds = start
        else:
            fps = self.timeline_model.get_fps()
            start_seconds = frames_to_seconds(start, fps)
        self.clip.Start(start_seconds)

        data = {"start": start_seconds}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    # Todo: Invert the frames attribute. Currently it has to be
    #  negative to remove frames but it would be more intuitive if a
    #  trim function always _removes_ a number of frames. There should
    #  be no case in which one wanted to add frames at the end and
    #  therefore every call would use a negative argument.
    def trim_end(self, trim_frames):
        """
        Trim the timeable's end by a number of frames. To remove frames
        the frame number must be negative.

        @param trim_frames: The number of frames to add. To remove
                            frames, use a negative number.
        @return:            Nothing
        """
        fps = self.timeline_model.get_fps()
        trim_seconds = frames_to_seconds(trim_frames, fps)
        end_seconds = self.clip.End() + trim_seconds
        self.set_end(end_seconds, is_sec=True)

    def set_end(self, end, is_sec=False):
        """
        Set the end of the timeable in frames or seconds.

        @param end:    The new end of the timeable in frames or seconds.
        @param is_sec: Specifies if the end is given in frames or in
                       seconds. False means frames and True means
                       seconds.
        @return:       Nothing.
        """
        if is_sec:
            end_seconds = end
        else:
            fps = self.timeline_model.get_fps()
            end_seconds = frames_to_seconds(end, fps)
        self.clip.End(end_seconds)

        data = {"end": end_seconds}
        self.timeline_model.change(
            "update", ["clips", {"id": self.clip.Id()}], data)

    def move(self, start, is_sec=False):
        """
        Move the timeable to a new start time in frames or seconds.

        @param start:  The new start time in frames or seconds.
        @param is_sec: Specifies if the end is given in frames or in
                       seconds. False means frames and True means
                       seconds.
        @return:       Nothing.
        """
        if is_sec:
            start_seconds = start
        else:
            fps = self.timeline_model.get_fps()
            start_seconds = frames_to_seconds(start, fps)
        self.clip.Position(start_seconds)

        data = {"position": start_seconds}
        self.timeline_model.change(
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
