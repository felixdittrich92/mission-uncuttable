from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem


class TimeableView(QGraphicsRectItem):
    """
    A View for a single Timeable representing a Video- or Audioclip. A Timeable
    is always located on a TrackView.

    The TimeableView can be resized and moved on the Track and it can also be dragged
    to another Track.
    """

    def __init__(self, name, width, height, x_pos):
        """
        Creates a new TimeableView at the specified position on a TrackView.

        @param name: the name that is displayed in the top left corner of the timeable
        @param width: timeable width, can be changed while resizing
        @param height: timeable heigth, should be the same as track heigth
        @param x_pos: position on the track
        """
        super(TimeableView, self).__init__()

        self.name = name
        self.width = width
        self.max_width = width
        self.height = height
        self.x_pos = x_pos

        self.setRect(self.boundingRect())
        self.setPos(self.x_pos, 0)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)  # necessary for moving
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
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
        """
        Overwritten Qt Function that defines the outer bounds of the item as a rectangle.
        """
        return QtCore.QRectF(QtCore.QRectF(0, 0, self.width, self.height))

    def paint(self, painter, option, widget):
        """
        Overwritten Qt function that paints the item.
        """
        self.brush = QtGui.QBrush(QtGui.QColor(214, 104, 83))
        painter.setBrush(self.brush)
        painter.drawRect(self.rect())
        # todo: don't draw text if width is too small
        painter.drawText(QtCore.QPointF(1, 15), self.name)

    def contextMenuEvent(self, event):
        """
        defines a rightclick event on the timeable
        """
        event.accept()
        self._show_context_menu(self, event.screenPos())

    def _show_context_menu(self, button, pos):
        """
        shows a context menu, called from contextMenuEvent
        """
        menu = QtWidgets.QMenu()

        delete = QtWidgets.QAction('löschen')
        menu.addAction(delete)
        delete.triggered.connect(self.delete)

        menu.exec_(pos)

    def delete(self):
        """
        removes the timeable from the track
        """
        self.scene().removeItem(self)

    def update_handles_pos(self):
        """
        Sets the position of all handles.

        It's important to call this function everytime the geometry of the Timeable
        is changed (when resizing)
        """
        # handle for resizing on the left side
        self.handles[self.handle_left] = QtCore.QRectF(
            self.rect().left(), 0, 4, self.height)

        # handle for resizing on the right side
        self.handles[self.handle_right] = QtCore.QRectF(
            self.rect().right() - 4, 0, 4, self.height)

        # handle for moving
        self.handles[self.handle_middle] = QtCore.QRectF(
            self.rect().left() + 4, 0, self.width - 8, self.height)

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
        rect = self.rect()

        if self.handle_selected == self.handle_left:
            diff = (self.mouse_press_rect.left() + mouse_event.pos().x()
                    - self.mouse_press_pos.x())

            if diff + self.scenePos().x() >= 0:
                rect.setLeft(diff)
                w = rect.size().width()
                if w <= 9 or w > self.max_width:
                    return

                new_x_pos = self.x_pos + diff
                r = QtCore.QRectF(new_x_pos, 0, w, self.height)
                colliding = self.scene().items(r)
                if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
                    return

                self.width = w
                self.setRect(self.boundingRect())
                self.x_pos = self.x_pos + diff
                self.setPos(self.x_pos, 0)
            else:
                return

        elif self.handle_selected == self.handle_right:
            diff = (self.mouse_press_rect.right() + mouse_event.pos().x()
                    - self.mouse_press_pos.x())

            if diff <= self.scene().width():
                rect.setRight(diff)
                w = rect.size().width()
                if w <= 9 or w > self.max_width:
                    return

                r = QtCore.QRectF(self.x_pos, 0, w, self.height)
                colliding = self.scene().items(r)
                if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
                    return

                self.width = w
                self.setRect(self.boundingRect())
                self.setPos(self.x_pos, 0)
            else:
                return

        self.update_handles_pos()

    def move_on_track(self, mouse_event):
        """
        called from mouseMoveEvent() when middle handle is selected

        either moves the Timeable to the mouse position or does nothing if moving is not
        possible (when theres another timeable or the beginning or end of the track
        is reached)

        @param mouse_event: the event parameter from the mouseMoveEvent function
        """
        new_pos_x = mouse_event.scenePos().x() - self.mouse_press_pos.x()

        # check if theres another Timeable at the given position
        r = QtCore.QRectF(new_pos_x, 0, self.width, self.height)
        colliding = self.scene().items(r)
        if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
            return

        # move only if the new position is still inside the track
        if new_pos_x >= 0 and new_pos_x + self.width <= self.scene().width():
            self.x_pos = new_pos_x
            self.setPos(self.x_pos, 0)

    def start_drag(self, mouse_event):
        # get qpixmap from the timeable
        r = self.boundingRect()
        pixmap = QtGui.QPixmap(r.width(), r.height())
        painter = QtGui.QPainter(pixmap)
        painter.drawRect(r)
        self.scene().render(painter, QtCore.QRectF(), self.sceneBoundingRect())
        painter.end()

        # write timeable data
        item_data = QtCore.QByteArray()
        data_stream = QtCore.QDataStream(item_data, QtCore.QIODevice.WriteOnly)
        QtCore.QDataStream.writeString(data_stream, str.encode(self.name))
        QtCore.QDataStream.writeInt(data_stream, self.width)

        mimeData = QtCore.QMimeData()
        mimeData.setData('ubicut/timeable', item_data)

        # start drag
        drag = QtGui.QDrag(self.scene())
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(self.width / 2, self.height / 2))

        drag.setPixmap(pixmap)

        # delete the timeable if the the item was succesfully dropped
        if (drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction):
            self.delete()

    def hoverMoveEvent(self, event):
        """
        called when mouse hovers over Timeable,
        sets the cursor according to the position of the mouse
        """
        # get handle at current position
        handle = self.handle_at(event.pos())

        # set the cursor according to the handle
        if handle == self.handle_middle:
            cursor = QtCore.Qt.OpenHandCursor
        else:
            cursor = QtCore.Qt.SizeHorCursor

        self.setCursor(cursor)

        QGraphicsItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        """
        called when mouse leaves the timeable, sets cursor back to normal arrow cursor
        """
        self.setCursor(QtCore.Qt.ArrowCursor)

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
            self.setCursor(QtCore.Qt.ClosedHandCursor)

            # start drag event only when cursor leaves current track
            if event.pos().y() < 0 or event.pos().y() > self.height:
                self.start_drag(event)
            else:
                self.move_on_track(event)

        else:
            self.resize(event)

        QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        """
        called when mouse button is released, resets selected handle and mouse press pos
        """
        self.setCursor(QtCore.Qt.OpenHandCursor)

        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None

        QGraphicsItem.mouseReleaseEvent(self, event)
