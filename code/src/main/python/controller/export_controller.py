import os

import openshot

from model.project import TimelineModel
from view.exportview.export_error_view import ExportErrorView


class ExportController:
    @staticmethod
    def start_export(options):
        """
        exports the timeline

        @param options: dict with export options like codecs and bitrate
        """
        # get the openshot timeline
        tm = TimelineModel.get_instance()
        t = tm.timeline

        # set audio and video options
        audio_options = [options["has_audio"], options["audio_codec"], t.info.sample_rate,
                         t.info.channels, t.info.channel_layout, options["audio_bitrate"]]
        video_options = [options["has_video"], options["video_codec"], t.info.fps,
                         options["width"], options["height"], openshot.Fraction(4, 3), False,
                         False, options["video_bitrate"]]

        # get the number of the last frame
        last_frame = 0
        for c in t.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * t.info.fps.ToFloat()) + 1

        # set the right file extension
        path = options["path"]
        video_format = options["video_format"]
        if os.path.splitext(path)[1] != ("." + video_format):
            path = "{}.{}".format(path, video_format)

        # try to start the export, show window with error message if theres an exception
        try:
            tm.export(path, audio_options, video_options, 1, last_frame)
        except Exception as e:
            ExportErrorView(str(e))
