from .size_connectable_frame import SizeLinkableFrame


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

        # set size
        self.setFixedWidth(50)
        self.setFixedHeight(200)

        # debug look (everything works just as good ad before if you
        # remove this code):
        from PyQt5.QtWidgets import QVBoxLayout, QPushButton
        self.setLayout(QVBoxLayout())
        for i in range(4):
            self.layout().addWidget(QPushButton(str(i)))
        self.setStyleSheet('background-color: orange')
