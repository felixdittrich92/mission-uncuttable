from PyQt5.QtWidgets import QFrame, QScrollBar
from PyQt5.QtCore import QObject, QPoint
from PyQt5 import uic

import os

from .time_needle import TimeNeedle
from config import Resources
from .track_button_frame import TrackButtonFrame
from .time_bar import TimeBar
from .track_frame import TrackFrame
from .connectable_scroll_area import ConnectableScrollArea
from .content_adjustable_connectable_scroll_area import \
    ContentAdjustableConnectableScrollArea

# Todo: Think of (and write, if found) a better doc. The current one is
#  not completely on the point yet.
# Todo: Write getters


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
        __track_frame -- The frame which all TrackViews are placed in

        __track_button_frame -- The frame which all TrackButtons are
        placed in

        __time_bar -- The time bar

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
        uic.loadUi(Resources.get_instance().files.timeline_scrollarea_view, self)
        self.setObjectName("scroll_area")
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.__horizontal_scroll_bar = None
        self.__vertical_scroll_bar = None
        self.__find_scroll_bars()

        self.__init_scroll_areas()

        self.__track_frame = TrackFrame()
        self.__track_frame.setObjectName("track_frame")
        self.__track_button_frame = TrackButtonFrame()
        self.__track_button_frame.setObjectName("track_button_frame")
        self.__time_bar = TimeBar()
        self.__time_bar.setObjectName("time_bar")

        self.__time_bar_scroll_area.setWidget(self.__time_bar)
        self.__time_bar_scroll_area.setObjectName("time_bar_scroll_area")
        self.__track_scroll_area.setWidget(self.__track_frame)
        self.__track_scroll_area.setObjectName("track_scroll_area")
        self.__track_button_scroll_area.setWidget(self.__track_button_frame)
        self.__track_button_scroll_area.setObjectName("track_button_scroll_area")
        self.__setup_dependencies()

        self.__show_debug_info_on_gui()

        self.__needle_top = TimeNeedle(self.__time_bar.height(), True)
        self.__needle_top.setParent(self.__time_bar)
        self.__needle_top.setObjectName("needle_top")
        self.__needle_top.move_needle(5)

        self.__needle_bottom = TimeNeedle(self.__track_frame.height())
        self.__needle_bottom.setParent(self.__track_frame)
        self.__needle_bottom.setObjectName("needle_bottom")
        self.__needle_bottom.move_needle(5)

        self.__needle_top.pos_changed.connect(self.__needle_bottom.move_needle)
        self.__needle_bottom.pos_changed.connect(self.__needle_top.move_needle)
        self.__track_frame.height_changed.connect(self.__needle_bottom.set_drawing_height)

        self.__needle_bottom.set_drawing_height(300)
        self.__needle_bottom.repaint()

    def __setup_dependencies(self):
        self.__track_button_frame.link_to_height(self.__track_frame)
        self.__time_bar.link_to_width(self.__track_frame)
        self.__track_scroll_area \
            .connect_horizontal_scrollbar(self.__horizontal_scroll_bar)
        self.__track_scroll_area \
            .connect_vertical_scrollbar(self.__vertical_scroll_bar)
        self.__track_button_scroll_area \
            .connect_vertical_scrollbar(self.__vertical_scroll_bar)
        self.__time_bar_scroll_area \
            .connect_horizontal_scrollbar(self.__horizontal_scroll_bar)
        self.__track_button_scroll_area.set_adjusting_to_width(True)
        self.__time_bar_scroll_area.set_adjusting_to_height(True)

    def __init_scroll_areas(self):
        track_scroll_area_placeholder = self.findChild(
            QObject, 'track_scroll_area_placeholder'
        )
        track_button_scroll_area_placeholder = self.findChild(
            QObject, 'track_button_scroll_area_placeholder'
        )
        time_bar_scroll_area_placeholder = self.findChild(
            QObject, 'time_bar_scroll_area_placeholder'
        )
        self.__time_bar_scroll_area \
            = ContentAdjustableConnectableScrollArea()
        self.__track_button_scroll_area \
            = ContentAdjustableConnectableScrollArea()
        self.__track_scroll_area \
            = ConnectableScrollArea()
        self.layout().replaceWidget(
            track_scroll_area_placeholder, self.__track_scroll_area)
        self.layout().replaceWidget(
            track_button_scroll_area_placeholder,
            self.__track_button_scroll_area
        )
        self.layout().replaceWidget(
            time_bar_scroll_area_placeholder, self.__time_bar_scroll_area
        )
        track_scroll_area_placeholder.deleteLater()
        track_button_scroll_area_placeholder.deleteLater()
        time_bar_scroll_area_placeholder.deleteLater()

    def __find_scroll_bars(self):
        self.__horizontal_scroll_bar = self.findChild(
            QScrollBar, 'horizontal_scroll_bar'
        )
        self.__vertical_scroll_bar = self.findChild(
            QScrollBar, 'vertical_scroll_bar'
        )

    def __show_debug_info_on_gui(self):
        """
        Setup the component somehow so that something can be seen which
        makes it possible to say if something works properly or not.
        """
