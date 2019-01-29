from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal


# Todo: Implement methods for unlinking.


class SizeLinkableFrame(QFrame):
    """
    Extends QFrame to a Frame which the size of can be linked to the
    size of another size-linkable component.

    The size linkage causes the frame the linking method was called on
    to dynamically set its own size to the size of the component it got
    linked to. The linkage can be set up independently for width and
    height. It is only one-directional but can be made two-directional
    if it is set up from both sides so that each component adapts to the
    other one.

    Method overview:
        link_to_width() -- Link the frame's width to the width of another
        size-linkable component.

        link_to_height() -- Link the frame's height to the height of another
        size-linkable component.

    Important note: This class declares Qt signals. Because this is done
    in Python, their inheritance doesn't work perfectly. In particular,
    while single inheritance works well, it is impossible to use multi
    inheritance with this class.
    """

    height_changed = pyqtSignal(int)
    width_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        """Create a SizeLinkableFrame without any linkage."""
        super(SizeLinkableFrame, self).__init__(parent)

    # noinspection PyPep8Naming
    def resizeEvent(self, event):
        """
        Extend resizeEvent() to emit Qt signals if a ResizeEvent occurs.

        Emit the following signals according to the ResizeEvent:
        self.height_changed, self.width_changed
        """
        old_size = event.oldSize()
        new_size = event.size()
        if old_size.width() != new_size.width():
            self.width_changed.emit(new_size.width())
        if old_size.height() != new_size.height():
            self.height_changed.emit(new_size.height())
        super().resizeEvent(event)

    def link_to_width(self, size_linkable_widget):
        """
        Setup a linkage of the own width to the width of
        size_linkable_widget.

        Form the linkage by connecting the signal
        size_linkable_widget.width_changed to self.setFixedWidth.

        :param size_linkable_widget: The size-linkable widget which the
                                     frame should be linked to
        """
        size_linkable_widget.width_changed.connect(self.setFixedWidth)

    def link_to_height(self, size_linkable_widget):
        """
        Setup a linkage of the own height to the height of
        size_linkable_widget.

        Form the linkage by connecting the signal
        size_linkable_widget.height_changed to self.setFixedHeight.

        :param size_linkable_widget: The size-linkable widget which the
                                     frame should be linked to
        """
        size_linkable_widget.height_changed.connect(self.setFixedHeight)
