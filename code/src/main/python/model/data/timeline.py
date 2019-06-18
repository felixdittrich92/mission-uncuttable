import json
import openshot


TIMELINE_DEFAULT_SETTINGS = {
    "fps": {
        "num": 25,
        "den": 1
    },
    "width": 1920,
    "height": 1080,
    "sample_rate": 48000,
    "channels": 2,
    "channel_layout": 3
}


class TimelineModel:
    __instance = None

    @staticmethod
    def get_instance():
        """ returns the timeline instance """
        if TimelineModel.__instance is None:
            TimelineModel()

        return TimelineModel.__instance

    def __init__(self, timeline_data=TIMELINE_DEFAULT_SETTINGS):
        """
        initalize the timeline model with given settings
        this class is a singleton so it can only be initialized once

        @param timeline_data: dict with timeline settings
                              (fps, width, height, sample_rate ...)
        """
        if TimelineModel.__instance is not None:
            raise Exception("singleton!")

        TimelineModel.__instance = self

        fps = timeline_data["fps"]
        width = timeline_data["width"]
        height = timeline_data["height"]
        sample_rate = timeline_data["sample_rate"]
        channels = timeline_data["channels"]
        channel_layout = timeline_data["channel_layout"]

        # create openshot timeline object
        self.timeline = openshot.Timeline(width, height, openshot.Fraction(
            fps["num"], fps["den"]), sample_rate, channels, channel_layout)

        self.timeline.Open()

        self.groups = []

    def get_clip_by_id(self, clip_id):
        """
        @param clip_id: id of the clip
        """
        for clip in self.timeline.Clips():
            if clip.Id() == clip_id:
                return clip

        return None

    def getTimeline(self):
        return self.timeline

    def get_fps(self):
        return self.timeline.info.fps.num / self.timeline.info.fps.den

    def change(self, change_type, key, data):
        """
        @param change_type: insert, delete or update
        @param key: defines what will be changed (clips or effects)
        @param data: dict with data to update
        """
        update_dict = {
            "type": change_type,
            "key": key,
            "value": data
        }

        update_string = json.dumps([update_dict])
        self.timeline.ApplyJsonDiff(update_string)

    def get_last_frame(self):
        """ returns the number of the last frame in the timeline """
        last_frame = 0
        for c in self.timeline.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * self.timeline.info.fps.ToFloat()) + 1

        return last_frame

    def export(self, filename, audio_options, video_options, start_frame, last_frame):
        """
        @param filename: name of the file in which the video is saved
        @param audio_options: list of audio options
        @param video_options: list of video options
        @param last_frame: number of the last frame that's exported
        """
        self.timeline.Open()

        # create writer
        w = openshot.FFmpegWriter(filename)

        # set options
        w.SetAudioOptions(*audio_options)
        w.SetVideoOptions(*video_options)

        w.Open()

        # export video
        for frame_number in range(start_frame, last_frame):
            w.WriteFrame(self.timeline.GetFrame(frame_number))

        w.Close()

    def remove_all_clips(self):
        """ Deletes all clips in the timeline (but not the views!!!) """
        for c in self.timeline.Clips():
            self.change("delete", ["clips", {"id": c.Id()}], {})
