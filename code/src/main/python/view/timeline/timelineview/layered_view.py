from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal, QSize


class LayeredView(QFrame):

    size_changed = pyqtSignal(QSize)

    def __init__(self):
        super().__init__()

    def add_widget(self, widget, fullsize=False):
        widget.setParent(self)

        self.size_changed.connect(widget.setFixedSize)

    def resizeEvent(self, event):
        new_size = event.size()

        self.size_changed.emit(new_size)