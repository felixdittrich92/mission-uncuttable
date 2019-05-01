import os

from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QDialogButtonBox, QComboBox
from PyQt5 import uic

from config import Resources
from controller.export_controller import ExportController
# from model.project.timeline import TimelineModel


class ExportView(QDialog):
    """A Class used as the View for export window"""
    def __init__(self, parent=None):
        super(ExportView, self).__init__(parent)
        uic.loadUi(Resources.get_instance().files.export_view, self)

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

        # timeline_info = TimelineModel.get_instance().timeline.info

        self.video_codec_edit = self.findChild(QLineEdit, "vcodec_edit")
        self.video_codec_edit.setText("libx264")

        self.video_bitrate_edit = self.findChild(QLineEdit, "vbitrate_edit")
        self.video_bitrate_edit.setText("384000")

        self.audio_codec_edit = self.findChild(QLineEdit, "acodec_edit")
        self.audio_codec_edit.setText("aac")

        self.audio_bitrate_edit = self.findChild(QLineEdit, "abitrate_edit")
        self.audio_bitrate_edit.setText("96000")

    def show_window(self):
        if self.exec_():
            has_audio = False
            has_video = False

            export_type = self.export_as_cb.currentText()
            if export_type == "Video und Audio":
                has_video = True
                has_audio = True
            elif export_type == "Nur Video":
                has_video = True
            elif export_type == "Nur Video":
                has_audio = True

            data = {
                "path": os.path.join(self.folder_edit.text(),
                                     self.filename_edit.text()),
                "has_audio": has_audio,
                "has_video": has_video,
                "audio_codec": self.audio_codec_edit.text(),
                "audio_bitrate": int(self.audio_bitrate_edit.text()),
                "video_codec": self.video_codec_edit.text(),
                "video_bitrate": int(self.video_bitrate_edit.text())
            }

            ExportController.start_export(data)
