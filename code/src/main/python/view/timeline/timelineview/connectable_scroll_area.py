from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal


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
    C{connect_scrollbar()} S{->} Connect scrolling actions to a scroll
    bar.
    C{disconnect_scrollbar()} S{->} Remove the connection between
    scrolling actions and a scroll bar.

    Detailed description of the connection process
    ==============================================
    If a C{ConnectableScrollArea} gets connected to a scroll bar two
    things happen:
     1. The range of the scroll bar gets set to the range of the scroll
        area's scroll bar. Normally this is the size of the scroll
        area's widget (either width or height, depending on the used
        method)
     2. The scroll area gets synchronized with the scroll bar so that
          - every time the value of the scroll bar changes the scroll
            area moves its widget inside the viewport (according to the
            direction which the scroll bar has been connected to)
          - every time the size of the widget changes the range of the
            scroll bar gets adapted accordingly
          - every time the scroll area is scrolled by something else
            the value of the scroll bar gets adapted accordingly

    For cases in which the scroll area's own original scrollbar isn't
    needed after connecting an external one it can be disabled over the
    C{setHorizontalScrollBarPolicy} and C{setVerticalScrollBarPolicy}
    methods.
    """

    viewport_width_changed = pyqtSignal(int)
    viewport_height_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        """Create a ConnectableScrollArea without any connection."""
        super(ConnectableScrollArea, self).__init__(parent)

        # store own scrollbars in a dict for parametric access in methods
        self.__own_scroll_bars = {
            Qt.Horizontal: self.horizontalScrollBar(),
            Qt.Vertical: self.verticalScrollBar()
        }
        self.__connected_scroll_bars = {
            Qt.Horizontal: set(),
            Qt.Vertical:   set()
        }

    def connect_scrollbar(self, scroll_bar, orientation):
        """
        Connect the scrolling actions in the given orientation to the
        foreign scroll bar.

        @param scroll_bar:  The scroll bar to connect the scroll area
                            to.
        @param orientation: The orientation of the movement which the
                            C{foreign_scroll_bar} should control.
        @type orientation:  Qt.Orientation
        @return:            Nothing.
        """
        if type(orientation) is not Qt.Orientation:
            raise TypeError(
                "value '"
                + str(orientation)
                + "' of parameter orientation is not of type 'Qt.Orientation'"
            )
        elif scroll_bar in self.__connected_scroll_bars[orientation]:
            raise ConnectionAlreadyExistingError()
        else:
            self.__connected_scroll_bars[orientation].add(scroll_bar)
            scroll_bar.setRange(
                self.__own_scroll_bars[orientation].minimum(),
                self.__own_scroll_bars[orientation].maximum()
            )
            scroll_bar.valueChanged\
                .connect(self.__own_scroll_bars[orientation].setValue)
            self.__own_scroll_bars[orientation].valueChanged\
                .connect(scroll_bar.setValue)
            self.__own_scroll_bars[orientation].rangeChanged\
                .connect(scroll_bar.setRange)
            if orientation == Qt.Horizontal:
                self.viewport_width_changed\
                    .connect(scroll_bar.setPageStep)
            elif orientation == Qt.Vertical:
                self.viewport_height_changed \
                    .connect(scroll_bar.setPageStep)

    def disconnect_scrollbar(self, scroll_bar, orientation=None):
        """
        Disconnect the scrolling actions in the specified orientation
        from the foreign scrollbar.

        If the orientation is C{None} the connection will be removed for
        both horizontal and vertical orientation.

        @param scroll_bar:  The scrollbar to disconnect
        @param orientation: The orientation which the connection should
                            be removed for. C{None} means both
                            horizontal and vertical.
        @type orientation:  Qt.Orientation
        @return:            Nothing
        """
        if orientation is None:
            orientations = {Qt.Horizontal, Qt.Vertical}
        elif type(orientation) is not Qt.Orientation:
            raise TypeError(
                "value '"
                + str(orientation)
                + "' of parameter orientation is not of type 'NoneType'"
                  " or 'Qt.Orientation'"
            )
        else:
            orientations = {orientation}
        for o in orientations:
            if scroll_bar not in self.__connected_scroll_bars[o]:
                if orientation is not None:
                    raise NotConnectedError(self, scroll_bar, o)
            else:
                scroll_bar.valueChanged\
                    .disconnect(self.__own_scroll_bars[o].setValue)
                self.__own_scroll_bars[o].valueChanged\
                    .disconnect(scroll_bar.setValue)
                self.__own_scroll_bars[o].rangeChanged\
                    .disconnect(scroll_bar.setRange)
                self.__connected_scroll_bars[o].remove(scroll_bar)
            if o == Qt.Horizontal:
                self.viewport_width_changed\
                    .disconnect(scroll_bar.setPageStep)
            elif o == Qt.Vertical:
                self.viewport_height_changed \
                    .disconnect(scroll_bar.setPageStep)

    # noinspection PyPep8Naming
    def resizeEvent(self, event):
        """
        Extend resizeEvent() to emit Qt signals if a ResizeEvent occurs.

        Emit the following signals according to the ResizeEvent:
        self.viewport_height_changed, self.viewport_width_changed
        """
        old_size = event.oldSize()
        new_size = event.size()
        if old_size.width() != new_size.width():
            self.viewport_width_changed.emit(
                self.__own_scroll_bars[Qt.Horizontal].pageStep()
            )
        if old_size.height() != new_size.height():
            self.viewport_height_changed.emit(
                self.__own_scroll_bars[Qt.Vertical].pageStep()
            )
        super().resizeEvent(event)


class NotConnectedError(ValueError):
    def __init__(self, scroll_area, scroll_bar, orientation=None):
        string = str(scroll_bar) + ' is not connected to ' + str(scroll_area)
        if orientation is not None:
            string += ' with orientation '
            if orientation == Qt.Horizontal:
                string += 'Qt.Horizontal'
            elif orientation == Qt.Vertical:
                string += 'Qt.Vertical'
            else:
                raise TypeError(
                    'orientation is not None or of type Qt.Orientation'
                )
        else:
            string += ' with any orientation.'
        super(NotConnectedError, self).__init__(string)


class ConnectionAlreadyExistingError(ValueError):
    def __init__(self):
        super(ConnectionAlreadyExistingError, self).__init__()