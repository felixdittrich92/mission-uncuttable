from PyQt5 import QtWidgets
from PyQt5 import QtCore

from view.timeline.timeableview import TimeableView


class TrackView(QtWidgets.QGraphicsView):
    """
    A View for a single Track, which can be added to the TrackFrame in the Timeline along
    with other TrackViews. The TrackView can hold Timeables.
    """

    def __init__(self, width, height, parent=None):
        """
        Creates TrackView with fixed width and height. The width and height should be
        the same for all TrackViews.

        @param width: track width
        @param height: track height
        """
        super(TrackView, self).__init__(parent)

        self.width = width
        self.height = height
        self.scene = QtWidgets.QGraphicsScene()

        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self):
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setMinimumWidth(self.width)
        self.setFixedHeight(self.height)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.setScene(self.scene)

        # self.setStyleSheet('background-color: black')

    def add_timeable(self, timeable):
        # TODO check for colliding items
        self.scene.addItem(timeable)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('ubicut/timeable'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('ubicut/timeable'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('ubicut/timeable'):
            # get the data from the dropped item
            item_data = event.mimeData().data('ubicut/timeable')
            stream = QtCore.QDataStream(item_data, QtCore.QIODevice.ReadOnly)
            name = QtCore.QDataStream.readString(stream).decode()
            width = QtCore.QDataStream.readInt(stream)
            res_left = QtCore.QDataStream.readInt(stream)
            res_right = QtCore.QDataStream.readInt(stream)

            # check if theres already another timeable at the drop position
            rect = QtCore.QRectF(event.pos().x() - width / 2, 0, width, self.height)
            colliding = self.scene.items(rect)
            if not colliding:
                # add new timeable
                t = TimeableView(name, width, self.height, event.pos().x() - width / 2)
                t.resizable_left = res_left
                t.resizable_rigth = res_right
                self.scene.addItem(t)

                event.acceptProposedAction()

        else:
            event.ignore()
