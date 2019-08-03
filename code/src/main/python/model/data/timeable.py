import locale
import openshot
from util.timeline_utils import (
    get_file_type, pos_to_seconds, seconds_to_pos)
from model.data.filetype import FileType


class TimeableModel:

    # Todo: Write documentation
    def __init__(self, timeable_id, file_path, name="timeable", is_video=None):
        # otherwhise there is a json parse error
        locale.setlocale(locale.LC_NUMERIC, 'en_US.utf8')

        self.clip = openshot.Clip(file_path)
        self.clip.Id(timeable_id)
        self.name = name
        self.is_video = is_video

        self.__original_length = seconds_to_pos(self.clip.Duration())
        self.__start = 0
        self.__trim_start = 0
        self.__trim_end = 0

        self.track = None

        self.file_path = file_path
        self.file_type = get_file_type(self.file_path)

        # Default length for image timeables
        if self.file_type == FileType.IMAGE_FILE:
            self.clip.Start(0)
            self.clip.End(1)

        if self.is_video is not None:
            if self.is_video:
                self.clip.has_video = openshot.Keyframe(1)
                self.clip.has_audio = openshot.Keyframe(0)
            else:
                self.clip.has_video = openshot.Keyframe(0)
                self.clip.has_audio = openshot.Keyframe(1)

        # if the timeline has no clips, set some timeline data to the data of this clip
        if self.is_first_vid():
            self.set_timeline_data()

    def get_info_dict(self):
        return {
            "file_name": self.file_path,
            "id": self.clip.Id(),
            "position": self.clip.Position(),
            "start": self.clip.Start(),
            "end": self.clip.End(),
            "layer:": self.clip.Layer()
        }

    def get_id(self):
        """Return the timeable's ID."""
        return self.clip.Id()

    def get_timeline_model(self):
        """Return the C{TimelineModel} which this timeable belongs to."""
        if self.track is not None:
            return self.track.get_timeline_model()
        else:
            return None

    def get_timeline_controller(self):
        """Return the C{TimelineController} which this timeable belongs to."""
        if self.track is not None:
            return self.track.get_timeline_controller()
        else:
            return None

    def is_first_vid(self):
        """ Returns True if this is the first video in the timeline, False otherwhise """
        if self.get_timeline_model() is not None:
            if not self.clip.Reader().info.has_video:
                return False

            for c in list(self.get_timeline_model().timeline.Clips()):
                if c.Reader().info.has_video:
                    return False
            return True
        else:
            return False

    def set_timeline_data(self):
        """ Sets the data of the timeline to data of this clip """
        if self.get_timeline_model() is not None:
            fps_data = {
                "num": self.clip.Reader().info.fps.num,
                "den": self.clip.Reader().info.fps.den
            }
            self.get_timeline_model().change("update", ["fps", ""], fps_data)
            self.get_timeline_model().change(
                "update", ["width"], self.clip.Reader().info.width)
            self.get_timeline_model().change(
                "update", ["height"], self.clip.Reader().info.height)

    def get_first_frame(self):
        """ Returns the frame that would be seen first """
        return int((self.clip.Start() * self.clip.Reader().info.fps.ToFloat()) + 1)

    def update_layer(self):
        """Update the layer of the timeable from its track."""
        layer = self.track.get_layer()
        if layer is not None:
            self._set_layer(layer)
        else:
            self._set_layer(-1)

    def get_start(self):
        return self.__start

    def get_length(self):
        return self.__original_length - self.__trim_start - self.__trim_end

    def get_end(self):
        return self.__start + self.get_length() - 1

    def get_width(self):
        return seconds_to_pos(self.clip.Duration())

    # Todo: Test for specification in the docstring
    # Todo: Specify the case for inverse arguments when the first
    #  operation isn't possible because either (if pos is negative)
    #  the timeable's base file is not long enough or (if pos is
    #  positive) the timeable is shorter than abs(pos).
    #  This can also be done by handling such cases as an Error
    def trim_start(self, pos):
        """start = start + sec(pos)

        Specification
        =============
          - Executing C{trim_start(n)} and C{trim_start(-n)} on the same
            C{TimeableModel} without any operation in-between will lead
            back to the state which the C{TimeableModel} had before the
            first of the two trim calls i.e. the state of the timeable
            will be the same as if the two calls wouldn't have happened.

        @param pos: The amount to trim in frames.
        @type pos:  int
        """
        self.__trim_start += pos
        self.__start += pos

        new_clip_start = pos_to_seconds(self.__trim_start)
        self.clip.Start(new_clip_start)

        data = {"start": new_clip_start}
        if self.get_timeline_model() is not None:
            self.get_timeline_model().change(
                "update", ["clips", {"id": self.clip.Id()}], data)

        if self.get_timeline_controller():
            self.get_timeline_controller().timeable_model_changed(self)

    def get_trim_start(self):
        return self.__trim_start

    def set_trim_start(self, pos):
        """Set the full length which is trimmed at the start of the
        timeable.

        @param pos: The amount to trim in frames.
        @type pos:  int
        """
        self.__start += pos - self.__trim_start
        self.__trim_start = pos

        new_clip_start = pos_to_seconds(self.__trim_start)

        self.clip.Start(new_clip_start)

        data = {"start": new_clip_start}
        if self.get_timeline_model() is not None:
            self.get_timeline_model().change(
                "update", ["clips", {"id": self.clip.Id()}], data)

        if self.get_timeline_controller():
            self.get_timeline_controller().timeable_model_changed(self)

    # Todo: Test for specification in docstring
    # Todo: Specify the case for inverse arguments when the first
    #  operation isn't possible because either (if pos is positive)
    #  the timeable's base file is not long enough or (if pos is
    #  negative) the timeable is shorter than abs(pos).
    #  This can also be done by handling such cases as an Error
    def trim_end(self, pos):
        """end = end + sec(pos)

        Specification
        =============
          - Executing C{trim_end(n)} and C{trim_end(-n)} on the same
            C{TimeableModel} without any operation in-between will lead
            back to the state which the C{TimeableModel} had before the
            first of the two trim calls i.e. the state of the timeable
            will be the same as if the two calls wouldn't have happened.

        @param pos: The amount to trim in frames. Must be negative to
                    remove frames.
        @type pos:  int
        """
        self.__trim_end -= pos
        new_end = pos_to_seconds(self.__original_length - self.__trim_end)

        self.clip.End(new_end)

        data = {"end": new_end}
        if self.get_timeline_model() is not None:
            self.get_timeline_model().change(
                "update", ["clips", {"id": self.clip.Id()}], data)

        if self.get_timeline_controller():
            self.get_timeline_controller().timeable_model_changed(self)

    def get_trim_end(self):
        return self.__trim_end

    def set_trim_end(self, pos):
        """Set the full length which is trimmed at the end of the
        timeable.

        @param pos: The amount to trim in frames.
        @type pos:  int
        """
        self.__trim_end = pos
        new_end = pos_to_seconds(self.__original_length - self.__trim_end)

        self.clip.End(new_end)

        data = {"end": new_end}
        if self.get_timeline_model() is not None:
            self.get_timeline_model().change(
                "update", ["clips", {"id": self.clip.Id()}], data)

        if self.get_timeline_controller():
            self.get_timeline_controller().timeable_model_changed(self)

    def get_position(self):
        """Return the position of the timeable on its track."""
        return seconds_to_pos(self.clip.Position())

    def move(self, track_model, pos, is_sec=False):
        """
        Set the position of the timeable in its timeline.

        B{Warning:} This method will only work properly for moving a
        timeable inside one single timeline and not from one to another.

        @param track_model: The track which the timeable should be moved
                            to or C{None} if it should stay in its
                            current track.
        @type track_model:  model.data.TrackModel
        @param pos:         The position which the timeable should be
                            moved to.
        @param is_sec:      Specifies if C{pos} is given in seconds
                            or in frames. C{False} means frames.
        """
        # Currently this method only provides movement _inside_ a
        # timeline and not between different ones. So the TimelineModel
        # and the TimelineController shouldn't change during the
        # movement. Therefore we don't need to store them before moving
        # for notification after finishing.

        if track_model is not None:
            self._set_track(track_model)

        if is_sec:
            self.__start = seconds_to_pos(pos)
        else:
            self.__start = pos

        new_clip_pos = pos_to_seconds(self.__start)
        self.clip.Position(new_clip_pos)

        data = {"position": new_clip_pos}
        if self.get_timeline_model() is not None:
            self.get_timeline_model().change(
                "update", ["clips", {"id": self.clip.Id()}], data)

        if self.get_timeline_controller():
            self.get_timeline_controller().timeable_model_changed(self)

    def remove(self):
        """Remove the timeable from its track."""
        self.track.remove_timeable(self.get_id())
        self.track = None

    def set_volume(self, volume):
        """ Set the volume of the timeable.

        @param volume: The volume level from 0 to 1.
        @type volume:  float
        """
        if volume < 0 or volume > 1:
            raise ValueError(
                "Can't set volume because it's not between 0 and 1: "
                "volume={}"
                    .format(volume)
            )
        else:
            self.clip.volume = openshot.Keyframe(volume)
            self.get_timeline_controller().timeable_model_changed(self)

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

        if self.get_timeline_controller():
            self.get_timeline_controller().timeable_model_changed(self)

    def _set_track(self, track):
        """Set the track of the timeable and update its properties
        according to the track. C{track=None} means that the timeable
        should not belong to any track.

        This method is only for convenience and internal use. It won't
        notify about the changes.

        Updated properties
        ==================
          - The layer.

            If the track's layer is C{None} the timeable's
            layer will be set to C{-1} because the Openshot layer
            parameter can't be C{None}.

          - The overlay state (called 'corner')

        @param track: The track.
        @type track:  model.data.TrackModel
        """
        if self.track is not None:
            self.track.remove_timeable(self.get_id())
        self.track = track
        self.update_layer()

        self.corner(track.is_overlay())

        track.add_timeable(self)

    def _set_layer(self, layer):
        """ Sets the layer of the clip """
        self.clip.Layer(layer)
        data = {"layer": layer}
        if self.get_timeline_model() is not None:
            self.get_timeline_model().change(
                "update", ["clips", {"id": self.clip.Id()}], data)

