from PyQt5.QtWidgets import QFrame, QGridLayout, QScrollBar
from PyQt5.QtCore import Qt
from .track_button_frame import TrackButtonFrame
from .time_bar import TimeBar
from .track_frame import TrackFrame
from .connectable_scroll_area import ConnectableScrollArea
from .content_adjustable_connectable_scroll_area import \
    ContentAdjustableConnectableScrollArea


class TimelineScrollArea(QFrame):
    def __init__(self, parent=None):
        super(TimelineScrollArea, self).__init__(parent)

        self.content_frame = QFrame()
        self.horizontal_scrollbar = QScrollBar(Qt.Horizontal)
        self.vertical_scrollbar = QScrollBar(Qt.Vertical)
        self.track_frame = TrackFrame()
        self.track_button_frame = TrackButtonFrame()
        self.time_bar = TimeBar()

        self.time_bar_scroll_area \
            = ContentAdjustableConnectableScrollArea()
        self.track_button_frame_scroll_area \
            = ContentAdjustableConnectableScrollArea()
        self.track_frame_scroll_area \
            = ConnectableScrollArea()

        self.setLayout(QGridLayout())
        self.layout().addWidget(self.content_frame, 0, 0)
        self.layout().addWidget(self.vertical_scrollbar, 0, 1)
        self.layout().addWidget(self.horizontal_scrollbar, 1, 0)

        self.content_frame.setLayout(QGridLayout())
        self.content_frame.layout() \
            .addWidget(self.time_bar_scroll_area, 0, 1)
        self.content_frame.layout() \
            .addWidget(self.track_frame_scroll_area, 1, 1)
        self.content_frame.layout() \
            .addWidget(self.track_button_frame_scroll_area, 1, 0)

        self.time_bar_scroll_area.setWidget(self.time_bar)
        self.track_frame_scroll_area.setWidget(self.track_frame)
        self.track_button_frame_scroll_area.setWidget(self.track_button_frame)

        self.track_button_frame.connect_to_height(self.track_frame)
        self.time_bar.connect_to_width(self.track_frame)

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
        self.setStyleSheet('background-color: blue')

