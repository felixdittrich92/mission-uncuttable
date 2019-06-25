import os

import openshot
from PyQt5.QtWidgets import QFileDialog

from model.data import TimelineModel
from view.exportview.export_error_view import ExportErrorView


class ExportController:
    """ Controller for the export window """

    def __init__(self, view):
        self.view = view

        # self.view.pick_folder_button.clicked.connect(self.pick_folder)
        self.view.export_button.clicked.connect(self.export_video)

    def start(self):
        """ Shows the export view """
        self.view.exec_()

    def pick_folder(self):
        """ Open a filemanager to pick a foldeer for the exported file """
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.view.folder_edit.setText(file)

    def export_video(self):
        """ Exports the timeline """
        options = self.view.get_data()

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
            tm.export(path, audio_options, video_options, start_frame,
                      end_frame, self.view)
        except Exception as e:
            ExportErrorView(str(e))

        self.view.accept()
