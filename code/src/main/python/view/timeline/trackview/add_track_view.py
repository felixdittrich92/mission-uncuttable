from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QPushButton, QDialogButtonBox, QRadioButton,
                             QLineEdit)

from config import Resources, Language, Settings


class AddTrackView(QDialog):
    """ Shows a Window that lets the user select options when adding a Track """

    def __init__(self, parent=None):
        super(AddTrackView, self).__init__(parent)
        uic.loadUi(Resources.files.add_track_view, self)
        self.init_stylesheet()

        self.add_button = QPushButton("Ok")
        self.add_button.setObjectName("ok_button")
        self.button_box.addButton(self.add_button, QDialogButtonBox.AcceptRole)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_box.addButton(self.cancel_button, QDialogButtonBox.RejectRole)

        self.video_button = self.findChild(QRadioButton, "video_button")
        self.audio_button = self.findChild(QRadioButton, "audio_button")

        self.name_edit = self.findChild(QLineEdit, "name_edit")

        self.setWindowTitle(str(Language.current.track.add))

    def init_stylesheet(self):
        current_stylesheet = Settings.get_instance().get_settings().design.color_theme.current
        if current_stylesheet == 0:
            self.setStyleSheet(open(Resources.files.qss_dark, "r").read())     
        elif current_stylesheet == 1:
            self.setStyleSheet(open(Resources.files.qss_light, "r").read())