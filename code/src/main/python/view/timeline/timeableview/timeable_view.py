from PyQt5.QtCore import (QPoint, QRectF, QByteArray, QDataStream, QIODevice,
                          QMimeData, Qt, QSize)
from PyQt5.QtGui import QBrush, QColor, QDrag
from PyQt5.QtWidgets import QMenu, QAction, QApplication
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem

from controller import TimelineController


TIMEABLE_MIN_WIDTH = 8
RESIZE_AREA_WIDTH = 3


class TimeableView(QGraphicsRectItem):
    """
    A View for a single Timeable representing a Video- or Audioclip. A Timeable
    is always located on a TrackView.

    The TimeableView can be resized and moved on the Track and it can also be dragged
    to another Track.
    """

    def __init__(self, name, width, height, x_pos, res_left, res_right, model, parent=None):
        """
        Creates a new TimeableView at the specified position on a TrackView.

        @param name: the name that is displayed in the top left corner of the timeable
        @param width: timeable width, can be changed while resizing
        @param height: timeable height, should be the same as track height
        @param x_pos: position on the track
        """
        super(TimeableView, self).__init__(parent)

        self.model = model

        QApplication.processEvents()
        self.set_pixmap()

        self.name = name
        self.prepareGeometryChange()
        self.width = width
        self.height = height
        self.x_pos = x_pos

        self.resizable_left = res_left
        self.resizable_right = res_right
        self.name_visible = False

        self.setRect(self.boundingRect())
        self.setPos(self.x_pos, 0)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)  # necessary for moving
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None

        self.handle_left = 1
        self.handle_right = 2
        self.handle_middle = 3

        self.handles = {}
        self.update_handles_pos()

    def boundingRect(self):
        """overwritten Qt Function that defines the outer bounds of the item as a rectangle."""
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

    def set_pixmap(self):
        """ Sets the pixmap to the first frame """
        frame = self.model.get_first_frame()
        px = TimelineController.get_pixmap_from_file(self.model.file_name, frame)
        if px is not None:
            self.pixmap = px.scaled(QSize(100, self.height), Qt.IgnoreAspectRatio)
        else:
            self.pixmap = None

    def contextMenuEvent(self, event):
        """shows a menu on rightclick"""
        event.accept()

        menu = QMenu()

        delete = QAction('löschen')
        menu.addAction(delete)
        delete.triggered.connect(self.delete)

        cut = QAction('schneiden')
        menu.addAction(cut)
        cut.triggered.connect(lambda: self.cut(event.pos().x()))

        menu.exec_(event.screenPos() + QPoint(0, 5))

    def delete(self):
        """ removes the timeable from the track and deletes the model from the timeline """
        self.model.delete()

        self.scene().removeItem(self)

    def cut(self, pos):
        """
        cuts the timeable in two parts

        @param pos: x position on the timeable where it's cut
        """
        if pos < TIMEABLE_MIN_WIDTH and self.width >= 2 * TIMEABLE_MIN_WIDTH:
            return

        new_model = self.model.cut(pos)
        new_model.set_layer(self.model.clip.Layer())

        # create the second timeable
        new_timeable = TimeableView(self.name, self.width - pos, self.height,
                                    pos + self.x_pos, 0, self.resizable_right, new_model)
        self.resizable_right = 0

        # the bounding rect is dependent on the width so we have to call prepareGeometryChange
        # otherwhise the program can randomly crash
        self.prepareGeometryChange()
        # own width gets reduced to the point where the rightclick was made
        self.width = pos
        # adjust own timeable
        self.setRect(self.boundingRect())
        self.setPos(self.x_pos, 0)

        # add the new timeable to the scene
        self.scene().addItem(new_timeable)

        self.update_handles_pos()

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
            self.rect().left() + RESIZE_AREA_WIDTH, 0, self.width - (2 * RESIZE_AREA_WIDTH),
            self.height)

    def handle_at(self, point):
        """
        returns the handle at the given point

        @param point: point in the Timeable from where the handle is returned
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k

        return None

    def resize(self, mouse_event):
        """
        called from mouseMoveEvent() when left or right handle is selected

        either resizes to the mouse position or does nothing if resizing is not possible
        (when theres another timeable or the beginning or end of track is reached)

        @param mouse_event: the event parameter from the mouseMoveEvent function
        """
        if self.handle_selected == self.handle_left:
            diff = mouse_event.pos().x() - self.mouse_press_pos.x()

            w = self.width - diff
            if w <= TIMEABLE_MIN_WIDTH or diff + self.scenePos().x() < 0 \
               or diff < self.resizable_left:
                return

            new_x_pos = self.x_pos + diff
            r = QRectF(new_x_pos, 0, w, self.height)
            colliding = self.scene().items(r)
            if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
                return

            self.prepareGeometryChange()
            self.width = w
            self.setRect(self.boundingRect())
            self.x_pos = self.x_pos + diff
            self.setPos(self.x_pos, 0)
            self.resizable_left -= diff

            # update clip data
            self.model.trim_start(diff)

        elif self.handle_selected == self.handle_right:
            diff = (self.mouse_press_rect.right() + mouse_event.pos().x()
                    - self.mouse_press_pos.x() - self.width)

            w = self.width + diff

            if w > self.scene().width() or w <= TIMEABLE_MIN_WIDTH \
               or diff > self.resizable_right:
                return

            r = QRectF(self.x_pos, 0, w, self.height)
            colliding = self.scene().items(r)
            if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
                return

            self.prepareGeometryChange()
            self.width = w
            self.setRect(self.boundingRect())
            self.resizable_right -= diff

            # update clip data
            self.model.trim_end(diff)

        self.model.move(self.x_pos)

        self.update_handles_pos()

    def move_on_track(self, pos):
        """
        called from mouseMoveEvent() when middle handle is selected

        either moves the Timeable to the mouse position or does nothing if moving is not
        possible (when theres another timeable or the beginning or end of the track
        is reached)

        @param mouse_event: the event parameter from the mouseMoveEvent function
        """
        # check if theres another Timeable at the given position
        r = QRectF(pos, 0, self.width, self.height)
        colliding = self.scene().items(r)
        if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
            return

        # move only if the new position is still inside the track
        if pos >= 0 and pos + self.width <= self.scene().width():
            self.x_pos = pos
            self.setPos(self.x_pos, 0)

            # set clip position on the timeline in seconds
            self.model.move(self.x_pos)

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
        QDataStream.writeString(data_stream, str.encode(self.name))
        QDataStream.writeInt(data_stream, self.width)
        QDataStream.writeInt(data_stream, int(self.mouse_press_pos.x()))
        QDataStream.writeInt(data_stream, self.resizable_left)
        QDataStream.writeInt(data_stream, self.resizable_right)
        QDataStream.writeString(data_stream, str.encode(self.model.file_name))
        QDataStream.writeString(data_stream, str.encode(self.model.clip.Id()))

        mimeData = QMimeData()
        mimeData.setData('ubicut/timeable', item_data)

        # set first frame as pixmap
        # frame = self.model.get_first_frame()
        frame = 1
        pixmap = TimelineController.get_pixmap_from_file(self.model.file_name, frame)

        # start drag
        drag = QDrag(self.scene())
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio))

        # delete the timeable if the the item was succesfully dropped
        if (drag.exec_(Qt.MoveAction) == Qt.MoveAction):
            self.delete()
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
        if handle == self.handle_middle:
            cursor = Qt.OpenHandCursor
        else:
            cursor = Qt.SizeHorCursor

        self.setCursor(cursor)

        QGraphicsItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        """called when mouse leaves the timeable, sets cursor back to normal arrow cursor"""
        self.setCursor(Qt.ArrowCursor)

        QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        """
        called when mouse is pressed on a timeable, sets the selected handle,
        sets the position where the mouse was pressed (important for moving and resizing)
        """
        self.handle_selected = self.handle_at(event.pos())
        self.mouse_press_pos = event.pos()
        self.mouse_press_rect = self.rect()

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
                pos = event.scenePos().x() - self.mouse_press_pos.x()
                self.move_on_track(pos)

        else:
            self.resize(event)

        QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        """called when mouse button is released, resets selected handle and mouse press pos"""
        self.setCursor(Qt.OpenHandCursor)

        QApplication.processEvents()
        self.set_pixmap()

        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None

        QGraphicsItem.mouseReleaseEvent(self, event)
