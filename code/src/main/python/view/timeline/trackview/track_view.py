from PyQt5 import QtWidgets
from PyQt5 import QtCore

from view.timeline.timeableview import TimeableView
from model.project.timeable import TimeableModel
from model.project.timeline import TimelineModel


class TrackView(QtWidgets.QGraphicsView):
    """
    A View for a single Track, which can be added to the TrackFrame in the Timeline along
    with other TrackViews. The TrackView can hold Timeables.
    """

    def __init__(self, width, height, num, parent=None):
        """
        Creates TrackView with fixed width and height. The width and height should be
        the same for all TrackViews.

        @param width: track width
        @param height: track height
        """
        super(TrackView, self).__init__(parent)

        self.width = width
        self.height = height
        self.num = num
        self.scene = QtWidgets.QGraphicsScene()

        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self):
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setMinimumSize(self.width, self.height)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.setScene(self.scene)

        self.setStyleSheet('background-color: black')

    def add_timeable(self, timeable):
        timeable.model.clip.Layer(self.num)
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
            file_name = QtCore.QDataStream.readString(stream).decode()
            clip_id = QtCore.QDataStream.readString(stream).decode()

            # check if theres already another timeable at the drop position
            rect = QtCore.QRectF(event.pos().x() - width / 2, 0, width, self.height)
            colliding = self.scene.items(rect)
            if not colliding:
                # add new timeable
                model = TimeableModel(file_name)
                timeline = TimelineModel.get_instance()
                old_clip = timeline.get_clip_by_id(clip_id)

                model.set_start(old_clip.Start(), is_sec=True)
                model.set_end(old_clip.End(), is_sec=True)
                model.move(event.pos().x() - width / 2)

                # delete old clip from the timeline
                timeline.change("delete", ["clips", {"id": clip_id}], {})

                t = TimeableView(name, width, self.height, event.pos().x() - width / 2, model)
                t.resizable_left = res_left
                t.resizable_rigth = res_right

                self.add_timeable(t)

                event.acceptProposedAction()

        else:
            event.ignore()
