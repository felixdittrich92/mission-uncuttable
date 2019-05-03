from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import QByteArray, QDataStream, QMimeData, QIODevice, Qt
from PyQt5.QtGui import QDrag


class FileListView(QListWidget):
    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.setDragEnabled(True)

    def mouseMoveEvent(self, event):
        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)

        item = self.itemAt(event.pos())
        if item is None:
            return

        path = item.statusTip()
        QDataStream.writeString(data_stream, str.encode(path))

        mime_data = QMimeData()
        mime_data.setData('ubicut/file', item_data)

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        drag.exec_(Qt.MoveAction)
