import cv2
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import QByteArray, QDataStream, QMimeData, QIODevice, Qt, QSize
from PyQt5.QtGui import QDrag

from controller import TimelineController
from util.timeline_utils import seconds_to_pos


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

        # get width of timeable that would be created
        v = cv2.VideoCapture(path)
        v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        d = v.get(cv2.CAP_PROP_POS_MSEC)
        width = seconds_to_pos(d / 1000)
        QDataStream.writeInt(data_stream, width)

        mime_data = QMimeData()
        mime_data.setData('ubicut/file', item_data)

        # set first frame as pixmap
        pixmap = TimelineController.get_pixmap_from_file(path)

        # create and execute drag
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio))

        drag.exec_(Qt.MoveAction)
