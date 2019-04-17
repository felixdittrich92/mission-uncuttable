from PyQt5.QtWidgets import QVBoxLayout
from .size_linkable_frame import SizeLinkableFrame


class TrackButtonFrame(SizeLinkableFrame):
    """
    Extends SizeLinkableFrame to a frame which is mainly intended to
    display TrackButtons.

    The TrackButtonFrame has the size-linkable property. For information
    on how to use this see the SizeLinkableFrame class.
    """

    def __init__(self, parent=None):
        """
        Create an empty TrackButtonFrame without any size linkage.

        :param parent: the parent component
        """
        super(TrackButtonFrame, self).__init__(parent)

        self.setLayout(QVBoxLayout())
        # self.setStyleSheet('background-color: orange')

    def add_button(self, button):
        """
        Adds a new Button to the TrackButtonFrame

        :param button: the button to add
        """
        button.setObjectName('track_button')
        self.layout().addWidget(button)
        self.adjustSize()
