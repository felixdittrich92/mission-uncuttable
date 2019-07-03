from PyQt5.QtWidgets import QListWidget, QListView
from PyQt5.QtCore import QByteArray, QDataStream, QMimeData, QIODevice, Qt, QSize
from PyQt5.QtGui import QDrag

from util.timeline_utils import get_pixmap_from_file, get_width_from_file, get_file_type


class FileListView(QListWidget):
    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.setDragEnabled(True)
        self.setWordWrap(True)
        self.setResizeMode(QListView.Adjust)

    def mouseMoveEvent(self, event):
        """ Starts the drag to the timeline """
        # do nothing if there is no item at the event position
        item = self.itemAt(event.pos())
        
        if item is None:
            return

        # write the path to the dragevent
        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)
        path = item.statusTip()
        QDataStream.writeString(data_stream, str.encode(path))

        # get width of timeable that would be created
        width = get_width_from_file(path)

        # do nothing if width is 0 because something went wrong
        if width == 0:
            return

        QDataStream.writeInt(data_stream, width)

        mime_data = QMimeData()
        mime_data.setData('ubicut/file', item_data)

        # set first frame as pixmap
        pixmap = get_pixmap_from_file(path, 1)

        # create and execute drag
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        if pixmap is not None:
            drag.setPixmap(pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio))

        drag.exec_(Qt.MoveAction)
