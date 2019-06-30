from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

from config import Resources


class AddTrackView(QDialog):
    """ Shows a Window that lets the user select options when adding a Track """

    def __init__(self, parent=None):
        super(AddTrackView, self).__init__(parent)
        uic.loadUi(Resources.files.add_track, self)
