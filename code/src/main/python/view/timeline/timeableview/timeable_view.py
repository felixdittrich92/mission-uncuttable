from PyQt5.QtCore import (QPoint, QRectF, QByteArray, QDataStream, QIODevice,
                          QMimeData, Qt, QSize)
from PyQt5.QtGui import QBrush, QColor, QDrag
from PyQt5.QtWidgets import QMenu, QAction, QApplication, QGraphicsItem, QGraphicsRectItem

from controller import TimelineController
from model.data import FileType
from util.timeline_utils import get_pixmap_from_file


TIMEABLE_MIN_WIDTH = 8
RESIZE_AREA_WIDTH = 3


class TimeableView(QGraphicsRectItem):
    """
    A View for a single Timeable representing a Video- or Audioclip. A Timeable
    is always located on a TrackView.

    The TimeableView can be resized and moved on the Track and it can also be dragged
    to another Track.
    """

    def __init__(self, name, width, height, x_pos, res_left, res_right,
                 model, view_id, track_id, parent=None):
        """
        Creates a new TimeableView at the specified position on a TrackView.

        @param name: the name that is displayed in the top left corner of the timeable
        @param width: timeable width, can be changed while resizing
        @param height: timeable height, should be the same as track height
        @param x_pos: position on the track
        """
        super(TimeableView, self).__init__(parent)

        self.model = model
        self.model.add_to_timeline()

        self.name = name
        self.view_id = view_id
        self.track_id = track_id
        self.width = width
        self.height = height
        self.x_pos = x_pos

        self.__controller = TimelineController.get_instance()

        self.set_pixmap()

        self.resizable_left = res_left
        self.resizable_right = res_right
        self.name_visible = False

        self.setRect(self.boundingRect())
        self.setPos(self.x_pos, 0)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        self.mouse_press_pos = 0
        self.mouse_press_start_pos = 0
        self.handle_selected = None
        self.mouse_press_rect = None
        self.infos_on_click = dict()

        self.handle_left = 1
        self.handle_right = 2
        self.handle_middle = 3

        self.handles = dict()
        self.update_handles_pos()

    def boundingRect(self):
        """
        Overwritten Qt Function that defines the outer bounds
        of the item as a rectangle.
        """
        return QRectF(QRectF(0, 0, self.width, self.height))

    def paint(self, painter, option, widget):
        """overwritten Qt function that paints the item."""
        self.brush = QBrush(QColor(214, 104, 83))
        painter.setBrush(self.brush)
        painter.drawRect(self.rect())

        # show thumbnail if there is enough space
        if self.width > 101 and self.pixmap is not None:
            painter.drawPixmap(QPoint(1, 0), self.pixmap)

        # only draw name if it fits on the timeable
        # if it doesn't fit a tooltip will be shown (see hoverMoveEvent)
        if painter.fontMetrics().width(self.name) <= self.width:
            painter.setPen(QColor(245, 245, 245))
            painter.drawText(QPoint(8, 20), self.name)

            self.name_visible = True
        else:
            self.name_visible = False

    def get_info_dict(self):
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "resizable_right": self.resizable_right,
            "resizable_left": self.resizable_left,
            "x_pos": self.x_pos,
            "view_id": self.view_id,
            "track_id": self.track_id
        }

    def set_pixmap(self):
        """ Sets the pixmap to the first frame """
        frame = self.model.get_first_frame()

        QApplication.processEvents()

        px = get_pixmap_from_file(self.model.file_name, frame)
        if px is not None:
            self.pixmap = px.scaled(
                QSize(100, self.height), Qt.IgnoreAspectRatio)
        else:
            self.pixmap = None

    def set_width(self, new_width):
        """ Sets the width of the timeable """
        # the bounding rect is dependent on the width
        # so we have to call prepareGeometryChange
        # otherwhise the program can randomly crash
        self.prepareGeometryChange()
        self.width = new_width
        self.setRect(self.boundingRect())

    def contextMenuEvent(self, event):
        """shows a menu on rightclick"""
        event.accept()

        menu = QMenu()

        delete = QAction('löschen')
        menu.addAction(delete)
        delete.triggered.connect(lambda: self.delete(hist=True))

        cut = QAction('schneiden')
        menu.addAction(cut)
        cut.triggered.connect(lambda: self.cut(event.pos().x()))

        menu.exec_(event.screenPos() + QPoint(0, 5))

    def delete(self, hist=True):
        """ deletes the model from the timeline """
        self.__controller.delete_timeable(self.get_info_dict(),
                                          self.model.get_info_dict(), hist=hist)

    def remove_from_scene(self):
        """ Removes the timeableview from the track """
        self.scene().removeItem(self)

    def cut(self, pos):
        """
        cuts the timeable in two parts

        @param pos: x position on the timeable where it's cut
        """
        if pos < TIMEABLE_MIN_WIDTH and self.width >= 2 * TIMEABLE_MIN_WIDTH:
            return

        self.__controller.split_timeable(self.view_id, self.resizable_right,
                                         self.width, self.model.clip.End(), pos)

    def update_handles_pos(self):
        """
        Sets the position of all handles.

        It's important to call this function everytime the geometry of the Timeable
        is changed (when resizing)
        """
        # handle for resizing on the left side
        self.handles[self.handle_left] = QRectF(
            self.rect().left(), 0, RESIZE_AREA_WIDTH, self.height)

        # handle for resizing on the right side
        self.handles[self.handle_right] = QRectF(
            self.rect().right() - RESIZE_AREA_WIDTH, 0, RESIZE_AREA_WIDTH, self.height)

        # handle for moving
        self.handles[self.handle_middle] = QRectF(
            self.rect().left() + RESIZE_AREA_WIDTH, 0,
            self.width - (2 * RESIZE_AREA_WIDTH), self.height)

    def handle_at(self, point):
        """
        returns the handle at the given point

        @param point: point in the Timeable from where the handle is returned
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k

        return None

    def collides_with_other_timeable(self, rect):
        """ Returns trueif rect collides with any timeable, false otherwhise """
        colliding = self.scene().items(rect)
        return (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self]))

    def resize(self, pos):
        """
        called from mouseMoveEvent() when left or right handle is selected

        either resizes to the mouse position or does nothing if resizing is not possible
        (when theres another timeable or the beginning or end of track is reached)

        @param pos: the position of the mouse
        """
        is_image = self.model.file_type == FileType.IMAGE_FILE
        if self.handle_selected == self.handle_left:
            diff = pos - self.mouse_press_pos
            w = self.width - diff

            if (w <= TIMEABLE_MIN_WIDTH or diff + self.scenePos().x() < 0
                    or diff < self.resizable_left) and not is_image:
                return

            new_x_pos = self.x_pos + diff
            if self.collides_with_other_timeable(QRectF(new_x_pos, 0, w, self.height)):
                return

            self.resizable_left -= diff

            self.prepareGeometryChange()
            self.width = w
            self.x_pos = self.x_pos + diff
            self.setPos(self.x_pos, 0)

        elif self.handle_selected == self.handle_right:
            diff = (self.mouse_press_rect.right() + pos
                    - self.mouse_press_pos - self.width)
            w = self.width + diff

            if (w > self.scene().width() or w <= TIMEABLE_MIN_WIDTH
                    or diff > self.resizable_right) and not is_image:
                return

            if self.collides_with_other_timeable(QRectF(self.x_pos, 0, w, self.height)):
                return

            self.resizable_right -= diff

            self.prepareGeometryChange()
            self.width = w

        self.setRect(self.boundingRect())
        self.update_handles_pos()

    def move_on_track(self, pos):
        """
        called from mouseMoveEvent() when middle handle is selected

        either moves the Timeable to the mouse position or does nothing if moving is not
        possible (when theres another timeable or the beginning or end of the track
        is reached)

        @param pos: the new x_pos of the timeable
        """
        # check if theres another Timeable at the given position
        r = QRectF(pos, 0, self.width, self.height)
        colliding = self.scene().items(r)
        if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
            return

        # move only if the new position is still inside the track
        if pos >= 0 and pos + self.width <= self.scene().width():
            self.x_pos = 0 if pos < 5 else pos

            self.setPos(self.x_pos, 0)

        # model gets changed on mouseReleaseEvent

    def start_drag(self, mouse_event):
        """
        starts a drag event and sends necessary data via mime types

        called from mouseMoveEvent() when mouse leaves current track,
        deletes the current timeable if drop was succesfull
        """
        # hide timeable while dragging
        self.setVisible(False)

        # write timeable data
        item_data = QByteArray()
        data_stream = QDataStream(item_data, QIODevice.WriteOnly)
        QDataStream.writeString(data_stream, str.encode(self.view_id))

        mimeData = QMimeData()
        mimeData.setData('ubicut/timeable', item_data)

        # set first frame as pixmap
        frame = self.model.get_first_frame()
        pixmap = get_pixmap_from_file(self.model.file_name, frame)

        # start drag
        drag = QDrag(self.scene())
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio))

        # delete the timeable if the the item was succesfully dropped
        if (drag.exec_(Qt.MoveAction) == Qt.MoveAction):
            self.delete(hist=False)
        else:
            self.setVisible(True)

    def hoverMoveEvent(self, event):
        """
        called when mouse hovers over Timeable,
        sets the cursor according to the position of the mouse and shows timeable name
        """
        if not self.name_visible:
            self.setToolTip("<font color=\"#ffffff\">" + self.name + "</font>")

        # get handle at current position
        handle = self.handle_at(event.pos())

        # set the cursor according to the handle
        cursor = Qt.OpenHandCursor if handle == self.handle_middle else Qt.SizeHorCursor
        self.setCursor(cursor)

        QGraphicsItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        """
        Called when mouse leaves the timeable.
        Sets cursor back to normal arrow cursor
        """
        self.setCursor(Qt.ArrowCursor)

        QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        """
        called when mouse is pressed on a timeable, sets the selected handle,
        sets the position where the mouse was pressed
        (important for moving and resizing)
        """
        self.handle_selected = self.handle_at(event.pos())
        self.mouse_press_pos = int(event.pos().x())
        self.mouse_press_start_pos = self.x_pos
        self.mouse_press_rect = self.rect()
        self.infos_on_click = self.get_info_dict()

        QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        """
        called when mouse is pressed and moved, calls the move, drag or resize function
        according to selected handle
        """
        if self.handle_selected == self.handle_middle:
            self.setCursor(Qt.ClosedHandCursor)

            # start drag event only when cursor leaves current track
            if event.pos().y() < 0 or event.pos().y() > self.height:
                self.start_drag(event)
            else:
                pos = event.scenePos().x() - self.mouse_press_pos
                self.move_on_track(pos)

        else:
            self.resize(event.pos().x())

        QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        """
        Called when mouse button is released.
        Resets selected handle and mouse press pos
        """
        self.setCursor(Qt.OpenHandCursor)

        self.set_pixmap()

        # update clip position if changed
        if self.x_pos != self.mouse_press_start_pos:
            self.__controller.move_timeable(self.view_id, self.mouse_press_start_pos,
                                            self.x_pos)

        # trim start or end if resize happened
        if (self.resizable_right != self.infos_on_click["resizable_right"]
                or self.resizable_left != self.infos_on_click["resizable_left"]):
            self.__controller.resize_timeable(self.infos_on_click, self.get_info_dict())

        self.mouse_press_pos = 0
        self.handle_selected = None
        self.mouse_press_rect = None

        QGraphicsItem.mouseReleaseEvent(self, event)
