from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt


class ConnectableScrollArea(QScrollArea):
    """
    Extends the QScrollArea to a special ScrollArea which lets you take
    control by using external ScrollBars. It can be very useful if you
    want to control multiple ScrollAreas at once with only one
    ScrollBar.

    Although this sounds very useful and convenient there is a
    restriction in using the ConnectableScrollArea: One single ScrollBar
    can only control multiple actions if they all use the same value
    range. Otherwise unexpected behaviour can occur.

    Method overview:
    connect_horizontal_scrollbar()    -- Connect the horizontal
                                         scrolling actions to a scroll
                                         bar.
    connect_vertical_scrollbar()      -- Connect the vertical scrolling
                                         actions to a scroll bar.
    disconnect_horizontal_scrollbar() -- Remove the connection between
                                         the horizontal scrolling
                                         actions and a scroll bar.
    disconnect_vertical_scrollbar()   -- Remove the connection between
                                         the vertical scrolling actions
                                         and a scroll bar.

    If a ConnectableScrollArea gets connected to a ScrollBar three
    things happen:
     1. The range of the ScrollBar is set according to the size of the
        scroll area's widget (either horizontal or vertical, depending
        on the used method)
     2. The scroll area is synchronized with the ScrollBar so that
          * every time the value of the ScrollBar changes the ScrollArea
            moves its widget inside the viewport (according to the
            orientation which the ScrollBar has been connected to)
          * every time the size of the widget changes the range of the
            scrollbar is adapted, too
          * every time the ScrollArea gets scrolled by something else
            the value of the ScrollBar is adapted
     3. The scroll area's own ScrollBars with the corresponding
        orientation are shut off because in most cases it won't be
        needed anymore.
        The shut-off ScrollBars can be turned on again at every time
        simply by setting the scroll area's ScrollBarPolicies manually.
        The ConnectableScrollArea remembers how many ScrollBars are
        connected and shuts its own ScrollBars on again if all external
        ones have been disconnected. Respectively, this happens for
        horizontal and vertical direction independently.
    """

    def __init__(self, parent=None):
        """Create a ConnectableScrollArea without any connections."""
        super(ConnectableScrollArea, self).__init__(parent)

        self.__connections_horizontal = 0
        self.__connections_vertical = 0

    def connect_horizontal_scrollbar(self, foreign_scroll_bar):
        """
        Connect the horizontal scrolling actions to the
        foreign_scroll_bar.

        :param foreign_scroll_bar:  the scroll bar to connect the scroll
                                    area to
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

        :param foreign_scroll_bar:  the scroll bar to connect the scroll
                                    area to
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
        and the foreign_scroll_bar.

        :param foreign_scroll_bar:  the scroll bar to disconnect the
                                    scroll area from
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
        and the foreign_foreign_scroll_bar.

        :param foreign_scroll_bar:  the scroll bar to disconnect the
                                    scroll area from
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
