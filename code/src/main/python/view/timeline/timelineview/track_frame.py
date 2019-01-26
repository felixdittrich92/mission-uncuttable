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

        self.setFixedSize(5000, 3000)

        # debug look (everything works just as good ad before if you
        # remove this code):
        from PyQt5.QtWidgets import QGridLayout, QPushButton
        self.setLayout(QGridLayout())
        for i in range(30):
            for j in range(4):
                self.layout().addWidget(QPushButton(str(i) + "," + str(j)), j, i)
        self.setStyleSheet("background-color: orange")
