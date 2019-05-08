from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import QByteArray, QDataStream, QMimeData, QIODevice, Qt, QSize
from PyQt5.QtGui import QDrag

from controller import TimelineController


class FileListView(QListWidget):
    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.setDragEnabled(True)

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

        mime_data = QMimeData()
        mime_data.setData('ubicut/file', item_data)

        # set first frame as pixmap
        pixmap = TimelineController.get_pixmap_from_file(path)

        # create and execute drag
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio))

        drag.exec_(Qt.MoveAction)
