from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt


class ConnectableScrollArea(QScrollArea):
    """
    A special ScrollArea which lets you take control by using external
    ScrollBars. It can be very useful if you want to control multiple
    ScrollAreas at once with only one ScrollBar.

    Although this sounds very useful and convenient there is a
    restriction in using the ConnectableScrollArea: One single ScrollBar
    can only control multiple actions if they all use the same value
    range. Otherwise unexpected behaviour can occur.

    ScrollBars can be connected by calling
    connect_horizontal_scrollbar() or connect_vertical_scrollbar and
    can be disconnected by calling disconnect_horizontal_scrollbar()
    or disconnect_vertical_scrollbar().

    If a ConnectableScrollArea is connected to a ScrollBar it does three
    things:
        1. It sets the range of the ScrollBar according to the size of
           its widget
        2. It synchronizes itself with the ScrollBar so that
            * every time the value of the ScrollBar changes the
              ScrollArea adapts its viewport (according to the direction
              which the ScrollBar has been connected to)
            * every time the size of the widget changes the range of the
              scrollbar changes, too
            * every time the ScrollArea gets scrolled by something else
              the value of the ScrollBar is adapted
        3. It shuts its own ScrollBar in the corresponding direction
           off because in most cases it won't be needed anymore

    The shut-off ScrollBars can be turned on again at every time simply
    by calling QAbstractScrollBar.setHorizontalScrollBarPolicy() or the
    corresponding function for the vertical ScrollBar depending on
    what's needed.

    The ConnectableScrollArea remembers how many ScrollBars are
    connected and shuts its own ScrollBars on again if all external
    ones have been disconnected. Respectively, this happens for
    horizontal and vertical direction independently.
    """

    def __init__(self, parent=None):
        super(ConnectableScrollArea, self).__init__(parent)

        self.__connections_horizontal = 0
        self.__connections_vertical = 0

    def connect_horizontal_scrollbar(self, foreign_scroll_bar):
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
