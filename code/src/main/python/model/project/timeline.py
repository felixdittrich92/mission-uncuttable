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
        if TimelineModel.__instance is None:
            TimelineModel()

        return TimelineModel.__instance

    def __init__(self, project_data=TIMELINE_DEFAULT_SETTINGS):
        if TimelineModel.__instance is not None:
            raise Exception("singleton!")

        TimelineModel.__instance = self

        fps = project_data["fps"]
        width = project_data["width"]
        height = project_data["height"]
        sample_rate = project_data["sample_rate"]
        channels = project_data["channels"]
        channel_layout = project_data["channel_layout"]

        self.timeline = openshot.Timeline(width, height, openshot.Fraction(
            fps["num"], fps["den"]), sample_rate, channels, channel_layout)

        self.timeline.Open()

    def get_clip_by_id(self, clip_id):
        """
        @param clip_id: id of the clip
        """
        for clip in self.timeline.Clips():
            if clip.Id() == clip_id:
                return clip

        return None

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

    def export(self, filename, audio_options, video_options, last_frame):
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
        for frame_number in range(1, last_frame):
            w.WriteFrame(self.timeline.GetFrame(frame_number))

        w.Close()
