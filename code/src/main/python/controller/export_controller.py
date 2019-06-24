import os

import openshot

from model.data import TimelineModel
from view.exportview.export_error_view import ExportErrorView
# from view.exportview.export_progress_view import ExportProgressView


class ExportController:
    @staticmethod
    def start_export(options, view):
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
                         options["width"], options["height"], openshot.Fraction(4, 3),
                         False, False, options["video_bitrate"]]

        start_frame = options["start_frame"]
        end_frame = options["end_frame"]

        # set the right file extension
        path = options["path"]
        video_format = options["video_format"]
        if os.path.splitext(path)[1] != ("." + video_format):
            path = "{}.{}".format(path, video_format)

        # try to start the export, show window with error message if theres an exception
        try:
            # view = ExportProgressView()
            tm.export(path, audio_options, video_options, start_frame, end_frame, view)
        except Exception as e:
            ExportErrorView(str(e))
