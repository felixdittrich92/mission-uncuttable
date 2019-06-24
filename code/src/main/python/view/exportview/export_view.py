import os

from PyQt5.QtWidgets import (QDialog, QLineEdit, QPushButton, QDialogButtonBox,
                             QComboBox, QSpinBox, QLabel, QProgressBar)
from PyQt5 import uic

from config import Resources, Language
from model.data import TimelineModel

FORMAT_OPTIONS = {
    "mp4 (mpeg4)": {
        "videoformat": "mp4",
        "videocodec": "mpeg4",
        "audiocodec": "libmp3lame",
        "bitrate": {
            "video": {
                "high": 15000000,
                "medium": 5000000,
                "low": 384000
            },
            "audio": {
                "high": 192000,
                "medium": 128000,
                "low": 96000
            }
        }
    },
    "mp4 (h.264)": {
        "videoformat": "mp4",
        "videocodec": "libx264",
        "audiocodec": "aac",
        "bitrate": {
            "video": {
                "high": 15000000,
                "medium": 5000000,
                "low": 384000
            },
            "audio": {
                "high": 192000,
                "medium": 128000,
                "low": 96000
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
        uic.loadUi(Resources.files.export_view, self)

        self.setup_ui()

        self.canceled = False

    def setup_ui(self):
        self.setWindowTitle(str(Language.current.export.windowtitle))

        for name in ["filename", "folder", "format", "resolution", "quality"]:
            text = str(getattr(Language.current.export, name))
            self.findChild(QLabel, name + "_label").setText(text)

        self.filename_edit = self.findChild(QLineEdit, "filename_edit")
        self.filename_edit.setText(str(Language.current.export.untitled))

        # set default folder to home folder
        self.folder_edit = self.findChild(QLineEdit, "folder_edit")
        self.folder_edit.setText(os.path.expanduser('~'))

        self.pick_folder_button = self.findChild(QPushButton, "pick_folder_button")

        self.export_as_cb = self.findChild(QComboBox, "export_as_cb")

        self.export_button = QPushButton(str(Language.current.export.export))
        self.buttonBox.addButton(self.export_button, QDialogButtonBox.AcceptRole)

        self.cancel_button = QPushButton(str(Language.current.export.cancel))
        self.cancel_button.clicked.connect(self.cancel)
        self.buttonBox.addButton(
            self.cancel_button, QDialogButtonBox.RejectRole)

        self.format_cb = self.findChild(QComboBox, "format_cb")
        for k in FORMAT_OPTIONS.keys():
            self.format_cb.addItem(k)

        self.quality_cb = self.findChild(QComboBox, "quality_cb")
        self.quality_cb.addItem(str(Language.current.export.high))
        self.quality_cb.addItem(str(Language.current.export.medium))
        self.quality_cb.addItem(str(Language.current.export.low))

        self.size_cb = self.findChild(QComboBox, "size_cb")
        for k in SIZE_OPTIONS.keys():
            self.size_cb.addItem(k)

        last_frame = TimelineModel.get_instance().get_last_frame()

        self.start_frame_sb = self.findChild(QSpinBox, "start_sb")
        self.start_frame_sb.setRange(1, last_frame)
        self.start_frame_sb.setValue(1)

        self.end_frame_sb = self.findChild(QSpinBox, "end_sb")
        self.end_frame_sb.setRange(1, last_frame)
        self.end_frame_sb.setValue(last_frame)

        self.export_progress = self.findChild(QProgressBar, "export_progress")

    def get_data(self):
        """ Return dict with selected values """
        format_selected = FORMAT_OPTIONS[self.format_cb.currentText()]
        quality_index = self.quality_cb.currentIndex()
        audio_codec = format_selected["audiocodec"]
        video_codec = format_selected["videocodec"]
        if quality_index == 0:
            audio_bitrate = format_selected["bitrate"]["audio"]["high"]
            video_bitrate = format_selected["bitrate"]["video"]["high"]
        elif quality_index == 1:
            audio_bitrate = format_selected["bitrate"]["audio"]["medium"]
            video_bitrate = format_selected["bitrate"]["video"]["medium"]
        else:
            audio_bitrate = format_selected["bitrate"]["audio"]["low"]
            video_bitrate = format_selected["bitrate"]["video"]["low"]

        video_format = format_selected["videoformat"]

        size_selected = SIZE_OPTIONS[self.size_cb.currentText()]
        width = size_selected["width"]
        height = size_selected["height"]

        data = {
            "path": os.path.join(self.folder_edit.text(),
                                 self.filename_edit.text()),
            "has_audio": True,
            "has_video": True,
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

        return data

    def cancel(self):
        """ Cancel the export and close the view """
        self.canceled = True

        self.reject()
