import os

import cv2
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QDataStream, Qt, QIODevice, QRectF

from view.timeline.timeableview import TimeableView
from model.project import TimeableModel, TimelineModel
from util.timeline_utils import seconds_to_pos


# TODO move some stuff to timeline controller


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

        self.item_dropped = False
        self.current_timeable = None

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
        """ Adds a TimeableView to the Track. """
        timeable = TimeableView(name, width, self.height, x_pos, res_left, res_right, model)
        timeable.model.set_layer(self.num)
        self.scene().addItem(timeable)
        self.current_timeable = timeable

    def add_from_filemanager(self, drag_event):
        """ Adds a timeable when item from filemanager is dragged into the track """
        # get the path from the dropped item
        item_data = drag_event.mimeData().data('ubicut/file')
        stream = QDataStream(item_data, QIODevice.ReadOnly)
        path = QDataStream.readString(stream).decode()

        x_pos = drag_event.pos().x()
        # c = openshot.Clip(path)
        # width = seconds_to_pos(c.Duration())

        v = cv2.VideoCapture(path)
        v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        d = v.get(cv2.CAP_PROP_POS_MSEC)
        width = seconds_to_pos(d / 1000)

        # check if theres already another timeable at the drop position
        rect = QRectF(x_pos, 0, width, self.height)
        colliding = self.scene().items(rect)
        # add the timeable when there are no colliding items
        if not colliding:
            model = TimeableModel(path)
            model.move(x_pos)
            name = os.path.basename(path)
            self.add_timeable(name, width, x_pos, model)
            self.item_dropped = True

    def add_from_track(self, drag_event):
        """ Adds a timeable when a drag was started from a timeable on a track """
        # get the data from the dropped item
        item_data = drag_event.mimeData().data('ubicut/timeable')
        stream = QDataStream(item_data, QIODevice.ReadOnly)
        name = QDataStream.readString(stream).decode()
        width = QDataStream.readInt(stream)

        start_pos = drag_event.pos().x()

        # check if theres already another timeable at the drop position
        rect = QRectF(start_pos, 0, width, self.height)
        colliding = [item for item in self.scene().items(rect) if item.isVisible]

        # add the timeable when there are no colliding items
        if not colliding:
            res_left = QDataStream.readInt(stream)
            res_right = QDataStream.readInt(stream)
            file_name = QDataStream.readString(stream).decode()
            clip_id = QDataStream.readString(stream).decode()

            # create new timeable
            model = TimeableModel(file_name)
            timeline = TimelineModel.get_instance()
            old_clip = timeline.get_clip_by_id(clip_id)

            model.set_start(old_clip.Start(), is_sec=True)
            model.set_end(old_clip.End(), is_sec=True)
            model.move(start_pos)

            self.add_timeable(name, width, start_pos, model,
                              res_left=res_left, res_right=res_right)
            self.item_dropped = True

    def dragEnterEvent(self, event):
        """ Gets called when something is dragged into the track """
        if event.mimeData().hasFormat('ubicut/timeable'):
            self.add_from_track(event)
            event.accept()

        elif event.mimeData().hasFormat('ubicut/file'):
            self.add_from_filemanager(event)
            event.accept()

        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """ Gets called when something is dragged out of the track """
        if self.current_timeable is not None:
            self.current_timeable.delete()
            self.item_dropped = False
            self.current_timeable = None
            event.ignore()

        event.accept()

    def dragMoveEvent(self, event):
        """ Gets called when there is an active drag and the mouse gets moved """
        if event.mimeData().hasFormat('ubicut/timeable'):
            if self.item_dropped:
                self.current_timeable.move_on_track(event.pos().x())
                event.accept()
                return

            event.accept()
            self.add_from_track(event)

        elif event.mimeData().hasFormat('ubicut/file'):
            if self.item_dropped:
                self.current_timeable.move_on_track(event.pos().x())
                event.accept()
                return

            event.accept()
            self.add_from_filemanager(event)

        else:
            event.ignore()

    def dropEvent(self, event):
        """ Gets called when there is an active drag and the mouse gets released """
        if event.mimeData().hasFormat('ubicut/timeable'):
            if self.current_timeable is not None:
                event.acceptProposedAction()
                self.current_timeable = None

            self.item_dropped = False

        # for files that het dragged from the filemanager
        elif event.mimeData().hasFormat('ubicut/file'):
            self.item_dropped = False
            self.current_timeable = None

            if self.item_dropped:
                event.acceptProposedAction()

        else:
            event.ignore()
