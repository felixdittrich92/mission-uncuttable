from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal


class SizeConnectableFrame(QFrame):
    """

    """

    height_changed = pyqtSignal(int)
    width_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(SizeConnectableFrame, self).__init__(parent)

    def resizeEvent(self, event):
        old_size = event.oldSize()
        new_size = event.size()
        if old_size.width() != new_size.width():
            self.width_changed.emit(new_size.width())
        if old_size.height() != new_size.height():
            self.height_changed.emit(new_size.height())
        super().resizeEvent(event)

    def connect_to_width(self, size_connectable_widget):
        size_connectable_widget.width_changed.connect(self.setFixedWidth)

    def connect_to_height(self, size_connectable_widget):
        size_connectable_widget.height_changed.connect(self.setFixedHeight)