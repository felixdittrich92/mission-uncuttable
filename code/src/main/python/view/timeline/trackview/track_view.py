import os

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QDataStream, Qt, QIODevice, QRectF

from view.timeline.timeableview import TimeableView
from model.project import TimeableModel, TimelineModel


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
        @param num: the layer of the track, clips in tracks with higher numbers get rendered
                    above others
        """
        super(TrackView, self).__init__(parent)

        self.width = width
        self.height = height
        self.num = num

        # for drag and drop handling
        self.item_dropped = False
        self.current_timeable = None

        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self):
        """ sets up the trackview """
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)

        self.setMinimumWidth(self.width)
        self.setFixedHeight(self.height)

        self.setScene(QGraphicsScene())

        self.resize()

    def wheelEvent(self, event):
        """ Overrides wheelEvent from QGraphicsView to prevent scrolling in a track """
        pass

    def resize(self):
        """ sets the size of the trackview to self.width and self.height """
        self.setMinimumSize(self.width, self.height)
        self.scene().setSceneRect(0, 0, self.width, self.height)

        # TODO adjust sizes of other tracks via timeline controller

    def set_width(self, new_width):
        """
        Changes the width of the trackview.

        @param new_width: the new width of the track
        """
        self.width = new_width
        self.resize()

    def add_timeable(self, name, width, drag_pos, mouse_pos, model, res_left=0, res_right=0):
        """ Adds a TimeableView to the Track. """
        x_pos = drag_pos - mouse_pos
        if width + x_pos > self.width:
            self.set_width(width + x_pos)

        timeable = TimeableView(name, width, self.height, x_pos, res_left, res_right, model)
        timeable.mouse_press_pos = mouse_pos
        timeable.model.set_layer(self.num)
        self.scene().addItem(timeable)
        self.current_timeable = timeable

    def add_from_filemanager(self, drag_event):
        """ Adds a timeable when item from filemanager is dragged into the track """
        # get the path from the dropped item
        item_data = drag_event.mimeData().data('ubicut/file')
        stream = QDataStream(item_data, QIODevice.ReadOnly)
        path = QDataStream.readString(stream).decode()
        width = QDataStream.readInt(stream)

        x_pos = drag_event.pos().x()

        # check if theres already another timeable at the drop position
        rect = QRectF(x_pos, 0, width, self.height)
        colliding = self.scene().items(rect)
        # add the timeable when there are no colliding items
        if not colliding:
            model = TimeableModel(path)
            model.move(x_pos)
            model.set_end(width)

            name = os.path.basename(path)
            self.add_timeable(name, width, x_pos, 0, model)
            self.item_dropped = True

            return True

        return False

    def add_from_track(self, drag_event):
        """ Adds a timeable when a drag was started from a timeable on a track """
        # get the data thats needed to check for collisions
        item_data = drag_event.mimeData().data('ubicut/timeable')
        stream = QDataStream(item_data, QIODevice.ReadOnly)
        name = QDataStream.readString(stream).decode()
        width = QDataStream.readInt(stream)
        pos = QDataStream.readInt(stream)

        # get a list of items at the position where the timeable would be added
        start_pos = drag_event.pos().x()
        if start_pos < pos:
            return

        rect = QRectF(start_pos - pos, 0, width, self.height)
        colliding = [item for item in self.scene().items(rect) if item.isVisible]

        # only add the timeable if colliding is empty
        if not colliding:
            # read the rest of the data from the dragevent
            res_left = QDataStream.readInt(stream)
            res_right = QDataStream.readInt(stream)
            file_name = QDataStream.readString(stream).decode()
            clip_id = QDataStream.readString(stream).decode()

            # create new timeable
            model = TimeableModel(file_name)

            # find the old clip to get start and end of the clip
            timeline = TimelineModel.get_instance()
            old_clip = timeline.get_clip_by_id(clip_id)

            # adjust the new model
            model.set_start(old_clip.Start(), is_sec=True)
            model.set_end(old_clip.End(), is_sec=True)
            model.move(start_pos)

            # add the timeable to the track
            self.add_timeable(name, width, start_pos, pos, model,
                              res_left=res_left, res_right=res_right)

            # set item_dropped to True because the timeable was succesfully created
            self.item_dropped = True

            return True

        return False

    def move_dropped_timeable(self, event):
        pos = event.pos().x() - self.current_timeable.mouse_press_pos
        self.current_timeable.move_on_track(pos)

    def dragEnterEvent(self, event):
        """ Gets called when something is dragged into the track """
        if event.mimeData().hasFormat('ubicut/timeable'):
            # try to add a timeable
            self.add_from_track(event)

            event.accept()

        elif event.mimeData().hasFormat('ubicut/file'):
            # try to add a timeable
            self.add_from_filemanager(event)

            event.accept()

        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        """ Gets called when something is dragged out of the track """
        if self.current_timeable is not None:
            # delete dragged timeable if mouse leaves track
            self.current_timeable.delete()

            # clear data
            self.item_dropped = False
            self.current_timeable = None

            event.ignore()

        event.accept()

    def dragMoveEvent(self, event):
        """ Gets called when there is an active drag and the mouse gets moved """
        if event.mimeData().hasFormat('ubicut/timeable'):
            # move the timeable if it was created
            if self.item_dropped:
                self.move_dropped_timeable(event)
                event.accept()
                return

            # try to add the timeable if it wasn't added before
            self.add_from_track(event)
            event.accept()

        elif event.mimeData().hasFormat('ubicut/file'):
            # move the timeable if it was created
            if self.item_dropped:
                self.move_dropped_timeable(event)
                event.accept()
                return

            # try to add the timeable if it wasn't added before
            self.add_from_filemanager(event)
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        """ Gets called when there is an active drag and the mouse gets released """
        if event.mimeData().hasFormat('ubicut/timeable'):
            # accept MoveAction if timeable was succesfully created
            if self.current_timeable is not None:
                event.acceptProposedAction()
                self.current_timeable = None

            # set item_dropped to false for next drag
            self.item_dropped = False

        elif event.mimeData().hasFormat('ubicut/file'):
            # clear data for next drag
            self.item_dropped = False
            self.current_timeable = None

        else:
            event.ignore()
