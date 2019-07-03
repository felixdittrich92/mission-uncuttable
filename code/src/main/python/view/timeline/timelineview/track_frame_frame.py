from PyQt5.QtWidgets import QVBoxLayout, QWidget
from .size_linkable_frame import SizeLinkableFrame
from .time_needle import TimeNeedle


class TrackFrameFrame(SizeLinkableFrame):
    """
    Extends SizeLinkableFrame to a frame which is mainly intended to
    show TrackViews.

    The TrackFrame has the size-linkable property. For information on
    how to use this see the SizeLinkableFrame class.
    """

    def __init__(self, parent=None):
        """
        Create an empty TrackFrame without any size linkage.

        :param parent: the parent component
        """
        super(TrackFrameFrame, self).__init__(parent)
        vbox_layout = QVBoxLayout()
        vbox_layout.setSpacing(0)
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox_layout)



    def add_track_frame(self, track_frame):
        """
        Adds a TrackView to the TrackFrame

        :param track: the Track to add
        """
        self.layout().addWidget(track_frame)
        needle = self.findChild(QWidget, "needle_bottom")
        track_frame.stackUnder(needle)
        self.adjustSize()

    def add_track(self, track_frame):
        """
        Adds a TrackView to the TrackFrame

        :param track: the Track to add
        """
        self.layout().addWidget(track_frame)
        needle = self.findChild(QWidget, "needle_bottom")
        track_frame.stackUnder(needle)
        self.adjustSize()