from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QDataStream, Qt, QIODevice, QRectF

from view.timeline.timeableview import TimeableView
from model.project import TimeableModel, TimelineModel


class TrackView(QGraphicsView):
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

        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self):
        """ sets up the trackview """
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setScene(QGraphicsScene())

        self.setStyleSheet('background-color: black')

        self.resize()

    def resize(self):
        """ sets the size of the trackview to self.width and self.height """
        self.setMinimumSize(self.width, self.height)
        self.scene().setSceneRect(0, 0, self.width, self.height)

    def set_width(self, new_width):
        """
        Changes the width of the trackview.

        @param new_width: the new width of the track
        """
        self.width = new_width
        self.resize()

    def add_timeable(self, name, width, x_pos, model, res_left=0, res_right=0):
        """
        Adds a TimeableView to the Track.
        """
        timeable = TimeableView(name, width, self.height, x_pos, res_left, res_right, model)
        timeable.model.set_layer(self.num)
        self.scene().addItem(timeable)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('ubicut/timeable'):
            event.accept()
        elif event.mimeData().hasFormat('ubicut/file'):
            event.accept()
            # TODO create pixmap
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if event.mimeData().hasFormat('ubicut/timeable') \
           or event.mimeData().hasFormat('ubicut/file'):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat('ubicut/timeable') \
           or event.mimeData().hasFormat('ubicut/file'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('ubicut/timeable'):
            # get the data from the dropped item
            item_data = event.mimeData().data('ubicut/timeable')
            stream = QDataStream(item_data, QIODevice.ReadOnly)
            name = QDataStream.readString(stream).decode()
            width = QDataStream.readInt(stream)
            res_left = QDataStream.readInt(stream)
            res_right = QDataStream.readInt(stream)
            file_name = QDataStream.readString(stream).decode()
            clip_id = QDataStream.readString(stream).decode()

            # check if theres already another timeable at the drop position
            start_pos = event.pos().x() - width / 2
            if start_pos < 0:
                return

            rect = QRectF(start_pos, 0, width, self.height)
            colliding = self.scene().items(rect)
            if not colliding:
                # add new timeable
                model = TimeableModel(file_name)
                timeline = TimelineModel.get_instance()
                old_clip = timeline.get_clip_by_id(clip_id)

                model.set_start(old_clip.Start(), is_sec=True)
                model.set_end(old_clip.End(), is_sec=True)
                model.move(start_pos)

                # delete old clip from the timeline
                timeline.change("delete", ["clips", {"id": clip_id}], {})

                self.add_timeable(name, width, start_pos, model,
                                  res_left=res_left, res_right=res_right)

                event.acceptProposedAction()

        # for files that het dragged from the filemanager
        elif event.mimeData().hasFormat('ubicut/file'):
            item_data = event.mimeData().data('ubicut/file')
            stream = QDataStream(item_data, QIODevice.ReadOnly)
            path = QDataStream.readString(stream).decode()
            print(path)

            # TODO create timeable

        else:
            event.ignore()
