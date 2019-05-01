import openshot

from model.project import TimelineModel
from view.exportview.export_error_view import ExportErrorView


class ExportController:
    @staticmethod
    def start_export(options):
        """ exports the timeline """
        tm = TimelineModel.get_instance()
        t = tm.timeline

        # testing data
        audio_options = [options["has_audio"], options["audio_codec"], t.info.sample_rate,
                         t.info.channels, t.info.channel_layout, options["audio_bitrate"]]
        video_options = [options["has_video"], options["video_codec"], t.info.fps,
                         t.info.width, t.info.height, openshot.Fraction(1, 1), False,
                         False, options["video_bitrate"]]

        # get the number of the last frame
        last_frame = 0
        for c in t.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * t.info.fps.ToFloat()) + 1

        try:
            tm.export(options["path"], audio_options, video_options, last_frame)
        except Exception as e:
            ExportErrorView(str(e))
