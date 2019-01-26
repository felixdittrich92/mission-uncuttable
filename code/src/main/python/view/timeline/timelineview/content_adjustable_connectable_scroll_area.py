from .connectable_scroll_area import ConnectableScrollArea
from PyQt5.QtCore import pyqtSlot


# Todo: Implement correct widget replacement behaviour
#   Currently the ContentAdjustableConnectableScrollArea can only be set
#   to adapt to a widget it already holds.
#   As soon as the widget gets replaced or removed the adapting is
#   undefined. This is because the signal connections are not updated
#   if the widget changes.
#   Desired behaviour would be:
#   * The adjustment modes don't change if the widget changes
#   * The adjustment actions don't stick with the old widget but instead
#     are linked to the new one if there is one
#   * if there is no widget anymore the adjustment mode should be
#     remembered and restored if a new widget comes into play
# Todo: Implement sizeHint setup after deactivation of adjustment
#   To adjust the size of the ContentAdjustableConnectableScrollArea the
#   sizeHints are set to the same value by QWidget.setFixedWidth or
#   QWidget.setFixedHeight. If the adjusting gets deactivated this
#   change isn't undone so that the size of the scroll area is still
#   fixed. There should be set some default sizeHint values instead.


class ContentAdjustableConnectableScrollArea(ConnectableScrollArea):
    """
    Extends the ConnectableScrollArea to one which can be set to
    automatically fit its contents.

    The ContentAdjustableConnectableScrollArea can adjust its size so
    that its viewport perfectly fits the widget of the scroll area.
    The adjusting behaviour can be turned on and off for both horizontal
    and vertical adjustment independently.

    The scrolling connections of the ConnectableScrollArea still can be
    used. For more information see the documentation of
    view.timeline.timelineview.connectable_scroll_area \
        .ConnectableScrollArea

    Method overview:
    set_adjusting_to_width      -- Turn the width adjustment on or off.
    set_set_adjusting_to_height -- Turn the height adjustment on or off.


    Note that this scroll area should only hold a widget which is
    size-connectable (like e.g.
    view.timeline.timelineview.size_connectable_frame). This is because
    the scroll area has to synchronize itself with the size of its
    widget.
    """

    def __init__(self, parent=None):
        """
        Creates a ContentAdjustableConnectableScrollArea which behaves
        just like a normal scrollArea right after creation.
        Special behaviour can be defined after creation.

        :param parent: the parent widget
        """
        super(ContentAdjustableConnectableScrollArea, self).__init__(parent)
        self.__adjusting_to_width = False
        self.__adjusting_to_height = False

    def set_adjusting_to_width(self, b):
        """
        Turn the width adjustment on or off.

        :param b:   boolean value; True means adjustment on, False means
                    adjustment off
        """
        if b and not self.__adjusting_to_width:
            self.widget().width_changed.connect(self.__adjust_to_width)
            self.__adjust_to_width(self.widget().width())
            self.__adjusting_to_width = True
        elif not b and self.__adjusting_to_width:
            self.widget().width_changed.disconnect(self.__adjust_to_width)
            self.__adjusting_to_width = False

    def set_adjusting_to_height(self, b):
        """
        Turn the height adjustment on or off.

        :param b:   boolean value; True means adjustment on, False means
                    adjustment off
        """
        if b and not self.__adjusting_to_height:
            self.widget().height_changed.connect(self.__adjust_to_height)
            self.__adjust_to_height(self.widget().height())
            self.__adjusting_to_height = True
        elif not b and self.__adjusting_to_height:
            self.widget().height_changed.disconnect(self.__adjust_to_height)
            self.__adjusting_to_height = False

    @pyqtSlot(int)
    def __adjust_to_width(self, width):
        """
        Calculate the needed width of the scroll area for the given
        widget width and set it to the scroll area.

        :param width: The widget width the scroll area should adjust to
        """
        widget_border_width = self.width() - self.viewport().width()
        self.setFixedWidth(width + widget_border_width)

    @pyqtSlot(int)
    def __adjust_to_height(self, height):
        """
        Calculate the needed height of the scroll area for the given
        widget height and set it to the scroll area.

        :param height:  The widget height the scroll area should adjust
                        to
        """
        widget_border_height = self.height() - self.viewport().height()
        self.setFixedHeight(height + widget_border_height)
