from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt


class ConnectableScrollArea(QScrollArea):
    """
    Extends the QScrollArea to a special ScrollArea which can be
    controlled by external ScrollBars.

    Possible usages
    ===============
    The C{ConnectableScrollArea} can be very useful if you
    want to control multiple scroll areas at once with only one
    scroll bar.

    Warning: One single scroll bar
    can only control multiple actions if they all use the same value
    range. Otherwise unexpected behaviour can occur.

    Method overview
    ===============
    C{connect_horizontal_scrollbar()} S{->} Connect the horizontal
    scrolling actions to a scroll bar.
    C{connect_vertical_scrollbar()} S{->} Connect the vertical scrolling
    actions to a scroll bar.
    C{disconnect_horizontal_scrollbar()} S{->} Remove the connection
    between the horizontal scrolling actions and a scroll bar.
    C{disconnect_vertical_scrollbar()} S{->} Remove the connection between
    the vertical scrolling actions and a scroll bar.

    Detailed description of the connection process
    ==============================================
    If a C{ConnectableScrollArea} gets connected to a scroll bar three
    things happen:
     1. The range of the scroll bar gets set to the size of the
        scroll area's widget (either width or height, depending on the used
        method)
     2. The scroll area gets synchronized with the scroll bar so that
          - every time the value of the scroll bar changes the scroll area
            moves its widget inside the viewport (according to the
            direction which the scroll bar has been connected to)
          - every time the size of the widget changes the range of the
            scrollbar gets adapted accordingly
          - every time the scroll area is scrolled by something else
            the value of the scroll bar gets adapted accordingly
     3. The scroll area's C{ScrollBarPolicy} for the corresponding
        orientation gets set to C{ScrollBarAlwaysOff} because in most
        cases the own scroll bar won't be needed anymore.
        The shut-off scroll bar can be turned on again every time
        simply by setting the scroll area's C{ScrollBarPolicy} manually.
        The C{ConnectableScrollArea} remembers how many scroll bars are
        connected and shuts its own scroll bars on again if all external
        ones have been disconnected. Respectively, this happens for
        horizontal and vertical scrolling direction independently.
    """

    def __init__(self, parent=None):
        """Create a ConnectableScrollArea without any connection."""
        super(ConnectableScrollArea, self).__init__(parent)

        self.__connections_horizontal = 0
        self.__connections_vertical = 0

    def connect_horizontal_scrollbar(self, foreign_scroll_bar):
        """
        Connect the horizontal scrolling actions to the foreign scroll
        bar.

        @param foreign_scroll_bar: The scroll bar to connect the scroll
                                   area to.
        @return:                   Nothing.
        """
        own_scroll_bar = self.horizontalScrollBar()
        foreign_scroll_bar.setRange(
            own_scroll_bar.minimum(),
            own_scroll_bar.maximum()
        )
        foreign_scroll_bar.valueChanged. \
            connect(own_scroll_bar.setValue)
        own_scroll_bar.valueChanged. \
            connect(foreign_scroll_bar.setValue)
        own_scroll_bar.rangeChanged. \
            connect(foreign_scroll_bar.setRange)
        if self.__connections_horizontal == 0:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__connections_horizontal += 1

    def connect_vertical_scrollbar(self, foreign_scroll_bar):
        """
        Connect the vertical scrolling actions to the foreign scroll
        bar.

        @param foreign_scroll_bar: The scroll bar to connect the scroll
                                   area to.
        @return:                   Nothing.
        """
        own_scroll_bar = self.verticalScrollBar()
        foreign_scroll_bar.setRange(
            own_scroll_bar.minimum(),
            own_scroll_bar.maximum()
        )
        foreign_scroll_bar.valueChanged. \
            connect(own_scroll_bar.setValue)
        own_scroll_bar.valueChanged. \
            connect(foreign_scroll_bar.setValue)
        own_scroll_bar.rangeChanged. \
            connect(foreign_scroll_bar.setRange)
        if self.__connections_vertical == 0:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__connections_vertical += 1

    def disconnect_horizontal_scrollbar(self, foreign_scroll_bar):
        """
        Remove the connection between the horizontal scrolling actions
        and the foreign scroll bar.

        @param foreign_scroll_bar: The scroll bar to disconnect the
                                   scroll area from.
        @return:                   Nothing.
        """
        own_scroll_bar = self.horizontalScrollBar()
        foreign_scroll_bar.valueChanged. \
            disconnect(own_scroll_bar.setValue)
        own_scroll_bar.valueChanged. \
            disconnect(foreign_scroll_bar.setValue)
        own_scroll_bar.rangeChanged. \
            disconnect(foreign_scroll_bar.setRange)
        if self.__connections_horizontal == 1:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.__connections_horizontal -= 1

    def disconnect_vertical_scrollbar(self, foreign_scroll_bar):
        """
        Remove the connection between the vertical scrolling actions
        and the foreign scroll bar.

        @param foreign_scroll_bar: The scroll bar to disconnect the
                                   scroll area from.
        @return:                   Nothing.
        """
        own_scroll_bar = self.verticalScrollBar()
        foreign_scroll_bar.valueChanged. \
            disconnect(own_scroll_bar.setValue)
        own_scroll_bar.valueChanged. \
            disconnect(foreign_scroll_bar.setValue)
        own_scroll_bar.rangeChanged. \
            disconnect(foreign_scroll_bar.setRange)
        if self.__connections_vertical == 1:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.__connections_vertical -= 1
