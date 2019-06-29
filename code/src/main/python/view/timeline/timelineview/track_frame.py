from PyQt5.QtWidgets import QVBoxLayout, QWidget
from .size_linkable_frame import SizeLinkableFrame


class TrackFrame(SizeLinkableFrame):
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
        super(TrackFrame, self).__init__(parent)
        vbox_layout = QVBoxLayout()
        vbox_layout.setSpacing(0)
        vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox_layout)

    def add_track(self, track, index):
        """
        Adds a TrackView to the TrackFrame

        :param track: the Track to add
        """
        self.layout().insertWidget(index, track)
        needle = self.findChild(QWidget, "needle_bottom")
        track.stackUnder(needle)
        self.adjustSize()
        self.parent().adjustSize()

    def remove_track(self, track):
        """
        Removes a TrackView from the TrackFrame.

        @param track: the Track to remove
        """
        self.layout().removeWidget(track)
        track.deleteLater()
        self.adjustSize()
        self.parent().adjustSize()
