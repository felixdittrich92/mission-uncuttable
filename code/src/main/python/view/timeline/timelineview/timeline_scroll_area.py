from PyQt5.QtWidgets import QFrame, QGridLayout, QScrollBar
from PyQt5.QtCore import Qt
from .track_button_frame import TrackButtonFrame
from .time_bar import TimeBar
from .track_frame import TrackFrame
from .connectable_scroll_area import ConnectableScrollArea
from .content_adjustable_connectable_scroll_area import \
    ContentAdjustableConnectableScrollArea

# Todo: Clean everything up and remove the spaghetti code.
# Todo: Think of (and write, if found) a better doc. The current one is
#  not completely on the point yet.


class TimelineScrollArea(QFrame):
    """
    Extends QFrame to a frame which shows the timeline's tracks, its
    track buttons and the time bar and allows the user to access and
    manipulate the tracks very conveniently.

    All contents are shown through a special scroll area so that the
    user can focus on small parts of the timeline at a higher
    resolution.

    The TimelineScrollArea holds the following main components (the
    names are the QObject.objectName properties, which can be used with
    QWidget.findChild()):
        track_frame -- The frame which all TrackViews are placed in

        track_button_frame -- The frame which all TrackButtons are
        placed in

        time_bar -- The time bar

    The TimelineScrollArea makes use of size-linkable components and
    ConnectableScrollAreas to achieve special dependencies between the
    different components. The result is a three-part scroll area with
    synchronous high performance scrolling over all three parts.
    """

    def __init__(self, parent=None):
        """
        Create a TimelineScrollArea with a new TrackFrame,
        TrackButtonFrame and TimeBar.

        :param parent: the parent component
        """
        super(TimelineScrollArea, self).__init__(parent)

        self.horizontal_scrollbar = QScrollBar(Qt.Horizontal)
        self.vertical_scrollbar = QScrollBar(Qt.Vertical)
        self.track_frame = TrackFrame()
        self.track_frame.setObjectName("track_frame")
        self.track_button_frame = TrackButtonFrame()
        self.track_button_frame.setObjectName("track_button_frame")
        self.time_bar = TimeBar()

        self.time_bar_scroll_area \
            = ContentAdjustableConnectableScrollArea()
        self.track_button_frame_scroll_area \
            = ContentAdjustableConnectableScrollArea()
        self.track_frame_scroll_area \
            = ConnectableScrollArea()

        self.setLayout(QGridLayout())

        self.layout() \
            .addWidget(self.time_bar_scroll_area, 0, 1)
        self.layout() \
            .addWidget(self.track_frame_scroll_area, 1, 1)
        self.layout() \
            .addWidget(self.track_button_frame_scroll_area, 1, 0)

        self.layout().addWidget(self.vertical_scrollbar, 0, 2, 2, 1)
        self.layout().addWidget(self.horizontal_scrollbar, 2, 0, 1, 2)

        self.time_bar_scroll_area.setWidget(self.time_bar)
        self.track_frame_scroll_area.setWidget(self.track_frame)
        self.track_button_frame_scroll_area.setWidget(self.track_button_frame)

        self.track_button_frame.link_to_height(self.track_frame)
        self.time_bar.link_to_width(self.track_frame)

        self.track_frame_scroll_area \
            .connect_horizontal_scrollbar(self.horizontal_scrollbar)
        self.track_frame_scroll_area \
            .connect_vertical_scrollbar(self.vertical_scrollbar)
        self.track_button_frame_scroll_area \
            .connect_vertical_scrollbar(self.vertical_scrollbar)
        self.time_bar_scroll_area \
            .connect_horizontal_scrollbar(self.horizontal_scrollbar)

        self.track_button_frame_scroll_area.set_adjusting_to_width(True)
        self.time_bar_scroll_area.set_adjusting_to_height(True)

        self.__show_debug_info_on_gui()

    def __show_debug_info_on_gui(self):
        """
        Setup the component somehow so that something can be seen which
        makes it possible to say if something works properly or not.
        """
        self.setStyleSheet('background-color: blue')

