import os

from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QDialogButtonBox, QComboBox, QSpinBox
from PyQt5 import uic

from config import Resources
from controller.export_controller import ExportController
from model.project.timeline import TimelineModel

FORMAT_OPTIONS = {
    "mp4 (mpeg4)": {
        "videoformat": "mp4",
        "videocodec": "mpeg4",
        "audiocodec": "libmp3lame",
        "bitrate": {
            "video": {
                "hoch": 15000000,
                "mittel": 5000000,
                "niedrig": 384000
            },
            "audio": {
                "hoch": 192000,
                "mittel": 128000,
                "niedrig": 96000
            }
        }
    },
    "mp4 (h.264)": {
        "videoformat": "mp4",
        "videocodec": "libx264",
        "audiocodec": "aac",
        "bitrate": {
            "video": {
                "hoch": 15000000,
                "mittel": 5000000,
                "niedrig": 384000
            },
            "audio": {
                "hoch": 192000,
                "mittel": 128000,
                "niedrig": 96000
            }
        }
    }
}

SIZE_OPTIONS = {
    "1920x1080": {
        "width": 1920,
        "height": 1080
    },
    "1280x720": {
        "width": 1280,
        "height": 720
    }
}


class ExportView(QDialog):
    """A Class used as the View for export window"""
    def __init__(self, parent=None):
        super(ExportView, self).__init__(parent)
        uic.loadUi(Resources.get_instance().files.export_view, self)

        timeline_instance = TimelineModel.get_instance()

        self.filename_edit = self.findChild(QLineEdit, "filename_edit")

        # set default folder to home folder
        self.folder_edit = self.findChild(QLineEdit, "folder_edit")
        self.folder_edit.setText(os.path.expanduser('~'))

        self.export_as_cb = self.findChild(QComboBox, "export_as_cb")

        self.export_button = QPushButton('Exportieren')
        self.export_button.clicked.connect(self.accept)
        self.buttonBox.addButton(self.export_button, QDialogButtonBox.AcceptRole)

        self.cancel_button = QPushButton('Abbrechen')
        self.cancel_button.clicked.connect(self.reject)
        self.buttonBox.addButton(self.cancel_button, QDialogButtonBox.RejectRole)

        self.format_cb = self.findChild(QComboBox, "format_cb")
        for k in FORMAT_OPTIONS.keys():
            self.format_cb.addItem(k)

        self.quality_cb = self.findChild(QComboBox, "quality_cb")

        self.size_cb = self.findChild(QComboBox, "size_cb")
        for k in SIZE_OPTIONS.keys():
            self.size_cb.addItem(k)

        last_frame = timeline_instance.get_last_frame()

        self.start_frame_sb = self.findChild(QSpinBox, "start_sb")
        self.start_frame_sb.setRange(1, last_frame)
        self.start_frame_sb.setValue(1)

        self.end_frame_sb = self.findChild(QSpinBox, "end_sb")
        self.end_frame_sb.setRange(1, last_frame)
        self.end_frame_sb.setValue(last_frame)

    def start(self):
        if self.exec_():
            has_audio = False
            has_video = False

            export_type = self.export_as_cb.currentText()
            if export_type == "Video und Audio":
                has_video = True
                has_audio = True
            elif export_type == "Nur Video":
                has_video = True
            elif export_type == "Nur Audio":
                has_audio = True

            format_selected = FORMAT_OPTIONS[self.format_cb.currentText()]
            quality_selected = self.quality_cb.currentText()
            audio_codec = format_selected["audiocodec"]
            audio_bitrate = format_selected["bitrate"]["audio"][quality_selected]
            video_codec = format_selected["videocodec"]
            video_bitrate = format_selected["bitrate"]["video"][quality_selected]
            video_format = format_selected["videoformat"]

            size_selected = SIZE_OPTIONS[self.size_cb.currentText()]
            width = size_selected["width"]
            height = size_selected["height"]

            data = {
                "path": os.path.join(self.folder_edit.text(),
                                     self.filename_edit.text()),
                "has_audio": has_audio,
                "has_video": has_video,
                "video_format": video_format,
                "audio_codec": audio_codec,
                "audio_bitrate": audio_bitrate,
                "video_codec": video_codec,
                "video_bitrate": video_bitrate,
                "width": width,
                "height": height,
                "start_frame": self.start_frame_sb.value(),
                "end_frame": self.end_frame_sb.value()
            }

            ExportController.start_export(data)
