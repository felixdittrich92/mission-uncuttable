from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtWidgets import QGraphicsRectItem


class TimeableView(QGraphicsRectItem):
    def __init__(self, name, width, height, x_pos):
        super(TimeableView, self).__init__()

        self.name = name
        self.width = width
        self.height = height
        self.x_pos = x_pos

        self.setRect(self.boundingRect())
        self.setPos(self.x_pos, 0)

        self.setFlag(QGraphicsRectItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsRectItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)

        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None

        self.handle_left = 1
        self.handle_right = 2

        self.handles = {}
        self.update_handles_pos()

    def boundingRect(self):
        return QtCore.QRectF(QtCore.QRectF(0, 0, self.width, self.height))

    def paint(self, painter, option, widget):
        self.brush = QtGui.QBrush(QtGui.QColor(214, 104, 83))
        painter.setBrush(self.brush)
        painter.drawRect(self.rect())
        painter.drawText(QtCore.QPointF(0, 10), self.name)

    # rightclick menu
    def contextMenuEvent(self, event):
        event.accept()
        self._show_context_menu(self, event.screenPos())

    def _show_context_menu(self, button, pos):
        menu = QtWidgets.QMenu()

        delete = QtWidgets.QAction('löschen')
        menu.addAction(delete)
        delete.triggered.connect(self.delete)

        menu.exec_(pos)

    def delete(self):
        self.scene().removeItem(self)

    def update_handles_pos(self):
        self.handles[self.handle_left] = QtCore.QRectF(
            self.rect().left(), self.rect().center().y() - self.height / 2, 4,
            self.height)

        self.handles[self.handle_right] = QtCore.QRectF(
            self.rect().right() - 4, self.rect().center().y() - self.height / 2, 4,
            self.height)

    def handle_at(self, point):
        for k, v, in self.handles.items():
            if v.contains(point):
                return k

        return None

    def resize(self, mouse_event):
        rect = self.rect()

        # self.prepareGeometryChange()

        if self.handle_selected == self.handle_left:
            diff = (self.mouse_press_rect.left() + mouse_event.pos().x()
                    - self.mouse_press_pos.x())

            if diff + self.scenePos().x() >= 0:
                rect.setLeft(diff)
                w = rect.size().width()
                if w <= 9:
                    return

                self.width = w
                self.setRect(self.boundingRect())
                self.x_pos = self.x_pos + diff
                self.setPos(self.x_pos, 0)

        elif self.handle_selected == self.handle_right:
            diff = (self.mouse_press_rect.right() + mouse_event.pos().x()
                    - self.mouse_press_pos.x())

            # if self.scene().itemAt(mouse_event.scenePos(), QtGui.QTransform()) is not None:
            #     return

            if diff <= self.scene().width():
                rect.setRight(diff)
                w = rect.size().width()
                if w <= 9:
                    return

                self.width = w
                self.setRect(self.boundingRect())
                self.setPos(self.x_pos, 0)

        self.update_handles_pos()

    def move_on_track(self, mouse_event):
        new_pos_x = mouse_event.scenePos().x() - self.mouse_press_pos.x()
        if new_pos_x >= 0 and new_pos_x + self.width <= self.scene().width():
            self.x_pos = new_pos_x
            self.setPos(self.x_pos, 0)

    def hoverMoveEvent(self, event):
        handle = self.handle_at(event.pos())
        if handle is None:
            cursor = QtCore.Qt.OpenHandCursor
        else:
            cursor = QtCore.Qt.SizeHorCursor

        self.setCursor(cursor)

        QGraphicsItem.hoverMoveEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        self.handle_selected = self.handle_at(event.pos())
        self.mouse_press_pos = event.pos()
        self.mouse_press_rect = self.rect()

        QGraphicsItem.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.handle_selected is not None:
            self.resize(event)
        else:
            self.setCursor(QtCore.Qt.ClosedHandCursor)

            self.move_on_track(event)

        QGraphicsItem.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.OpenHandCursor)
        QGraphicsItem.mouseReleaseEvent(self, event)

        self.handle_selected = None
        self.mouse_press_pos = None
        self.mouse_press_rect = None
