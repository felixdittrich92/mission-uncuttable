import os

import openshot
from PyQt5.QtCore import (QPoint, QRectF, QByteArray, QDataStream, QIODevice,
                          QMimeData, Qt, QSize, pyqtSignal)
from PyQt5.QtGui import QBrush, QColor, QDrag, QTransform, QPixmap
from PyQt5.QtWidgets import (QMenu, QAction, QApplication, QGraphicsItem,
                             QGraphicsRectItem, QWidget)

from controller import TimelineController
from model.data import FileType
from config import Language, Resources, Settings
from util.timeline_utils import get_pixmap_from_file
from .timeable_settings_view import TimeableSettingsView

TIMEABLE_MIN_WIDTH = 8
RESIZE_AREA_WIDTH = 3
TIMEABLE_COLOR = "#AE6759"
TIMEABLE_BORDER_COLOR = "#2F2F2F"

HANDLE_LEFT = 1
HANDLE_RIGHT = 2
HANDLE_MIDDLE = 3


class TimeableView(QGraphicsRectItem):
    """
    A View for a single Timeable representing a Video- or Audioclip. A Timeable
    is always located on a TrackView.

    The TimeableView can be resized and moved on the Track and it can also be dragged
    to another Track.
    """

    update_previewplayer = pyqtSignal()

    def __init__(self, name, width, height, x_pos, res_left, res_right,
                 model, view_id, track_id, group_id=None, parent=None):
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
        self.width = width
        self.height = height
        self.x_pos = x_pos

        self.view_id = view_id
        self.track_id = track_id
        self.group_id = group_id

        self.__controller = TimelineController.get_instance()

        if self.__controller.is_overlay_track(self.track_id):
            self.model.corner(True)

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

        self.handles = dict()
        self.update_handles_pos()

    def boundingRect(self):
        """
        Overwritten Qt Function that defines the outer bounds
        of the item as a rectangle.
        """
        return QRectF(QRectF(0, 0, self.width, self.height - 3.0))

    def paint(self, painter, option, widget):
        """overwritten Qt function that paints the item."""
        brush = QBrush(QColor(TIMEABLE_COLOR))
        painter.setBrush(brush)
        painter.setPen(QColor(TIMEABLE_BORDER_COLOR))
        painter.drawRect(self.rect())

        # show thumbnail if there is enough space
        if self.width > 101 and self.pixmap is not None:
            painter.drawPixmap(QPoint(1, 1), self.pixmap)

        # only draw name if it fits on the timeable
        # if it doesn't fit a tooltip will be shown (see hoverMoveEvent)
        if painter.fontMetrics().width(self.name) + 100 <= self.width:
            painter.setPen(QColor(245, 245, 245))
            painter.drawText(QPoint(100, 20), self.name)

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
            "track_id": self.track_id,
            "group_id": self.group_id,
            "model": self.model.get_info_dict()
        }

    def set_pixmap(self):
        """ Sets the pixmap to the first frame """
        frame = self.model.get_first_frame()

        QApplication.processEvents()

        px = get_pixmap_from_file(self.model.file_name, frame)
        if px is not None:
            if self.model.is_video or (self.model.is_video is None):
                self.pixmap = px.scaled(QSize(100, self.height - 4.0), Qt.KeepAspectRatio,
                                        transformMode=1)
            else:
                px = QPixmap(os.path.join(Resources.images.media_symbols, "mp3.png"))
                self.pixmap = px.scaled(QSize(100, self.height - 4.0), Qt.KeepAspectRatio,
                                        transformMode=1)
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
        current_stylesheet = Settings.get_instance().get_settings().design.color_theme.current
        if current_stylesheet == 0:
            menu.setStyleSheet(open(Resources.files.qss_dark, "r").read())
        elif current_stylesheet == 1:
            menu.setStyleSheet(open(Resources.files.qss_light, "r").read())

        cut_timeneedle = QAction(str(Language.current.timeable.cut_timeneedle))
        menu.addAction(cut_timeneedle)
        cut_timeneedle.triggered.connect(self.cut_timeneedle)

        cut_here = QAction(str(Language.current.timeable.cut_here))
        menu.addAction(cut_here)
        cut_here.triggered.connect(lambda: self.cut_here(event.pos().x()))

        delete = QAction(str(Language.current.timeable.delete))
        menu.addAction(delete)
        delete.triggered.connect(lambda: self.delete(hist=True))

        settings = QAction(str(Language.current.timeable.settings))
        menu.addAction(settings)
        settings.triggered.connect(self.settings)

        if self.group_id is not None:
            remove_from_group = QAction(str(Language.current.timeable.group_remove))
            menu.addAction(remove_from_group)
            remove_from_group.triggered.connect(self.remove_from_group)

        menu.exec_(event.screenPos() + QPoint(0, 5))

    def settings(self):
        volume_dialog = TimeableSettingsView()
        current_clip_volume = self.model.clip.volume.GetValue(0)
        volume_dialog.set_data(current_clip_volume)
        volume_dialog.exec_()
        self.model.clip.volume = openshot.Keyframe(volume_dialog.current_volume_value)

    def delete(self, hist=True):
        """ deletes the model from the timeline """
        self.__controller.delete_timeable(self.get_info_dict(),
                                          self.model.get_info_dict(), hist=hist)

    def remove_from_group(self):
        if self.group_id is None:
            return

        self.__controller.remove_timeable_from_group(self.group_id, self.view_id)
        self.group_id = None

    def remove_from_scene(self):
        """ Removes the timeableview from the track """
        self.scene().removeItem(self)

    def cut_here(self, pos):
        """
        cuts the timeable in two parts

        @param pos: x position on the timeable where it's cut
        """
        if pos < TIMEABLE_MIN_WIDTH and self.width >= 2 * TIMEABLE_MIN_WIDTH:
            return

        self.__controller.split_timeable(self.view_id, self.resizable_right,
                                         self.width, self.model.clip.End(), pos)

    def cut_timeneedle(self):
        """
        Cuts the Timeable at the position of the Timeneedle, but only if the
        Timeneedle is on this Timeable.
        """
        # get the Timeneedle object
        needle = self.__controller.get_timelineview().track_frame_frame.findChild(
            QWidget, "needle_bottom")

        pos = needle.x()

        # do nothing if the Timeneedle is not on this Timeable
        if not self.scene().itemAt(QPoint(pos, 0), QTransform()) is self:
            return

        pos -= self.x_pos

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
        self.handles[HANDLE_LEFT] = QRectF(
            self.rect().left(), 0, RESIZE_AREA_WIDTH, self.height)

        # handle for resizing on the right side
        self.handles[HANDLE_RIGHT] = QRectF(
            self.rect().right() - RESIZE_AREA_WIDTH, 0, RESIZE_AREA_WIDTH, self.height)

        # handle for moving
        self.handles[HANDLE_MIDDLE] = QRectF(
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
        if self.handle_selected == HANDLE_LEFT:
            diff = pos - self.mouse_press_pos
            w = self.width - diff

            if ((w <= TIMEABLE_MIN_WIDTH or diff + self.scenePos().x() < 0)
                    or (diff < self.resizable_left and not is_image)):
                return

            new_x_pos = self.x_pos + diff
            if self.collides_with_other_timeable(QRectF(new_x_pos, 0, w, self.height)):
                return

            self.resizable_left -= diff

            self.prepareGeometryChange()
            self.width = w
            self.x_pos = self.x_pos + diff
            self.setPos(self.x_pos, 0)

        elif self.handle_selected == HANDLE_RIGHT:
            diff = (self.mouse_press_rect.right() + pos
                    - self.mouse_press_pos - self.width)
            w = self.width + diff

            if ((w > self.scene().width() or w <= TIMEABLE_MIN_WIDTH)
                    or (diff > self.resizable_right and not is_image)):
                return

            if self.collides_with_other_timeable(QRectF(self.x_pos, 0, w, self.height)):
                return

            self.resizable_right -= diff

            self.prepareGeometryChange()
            self.width = w

        self.setRect(self.boundingRect())
        self.update_handles_pos()

    def is_move_possible_diff(self, diff):
        """
        Checks if timeable can be moved by value in diff.

        @param diff: the difference between the x_pos before and after move.
        @return: True if move is possible, False otherwhise.
        """
        pos = self.x_pos + diff

        return self.is_move_possible_position(pos)

    def is_move_possible_position(self, pos):
        """
        Checks if move to pos is possible.

        @param pos: the position to which the timeable wants to be moved.
        @return: True if move is possible, False otherwhise.
        """
        # check if theres another Timeable at the given position
        r = QRectF(pos, 0, self.width, self.height)
        colliding = self.scene().items(r)
        if len(colliding) > 1:
            return False

        if (len(colliding) == 1 and colliding != [self]) \
            and not self.__controller.is_same_group(self.group_id,
                                                    colliding[0].group_id):
            return False

        # move only if the new position is still inside the track
        if pos < 0:
            return False

        # make track longer when new width is bigger than width
        if pos + self.width > self.scene().width():
            self.__controller.set_track_width(self.track_id, self.width + pos)

        return True

    def do_move(self, pos):
        """
        Changes the position of the timeables view.

        @param pos: the new x_pos.
        @return: Nothing.
        """
        # self.x_pos = 0 if pos < 5 else pos
        self.x_pos = pos
        self.setPos(self.x_pos, 0)

    def move_on_track(self, pos):
        """
        called from mouseMoveEvent() when middle handle is selected

        either moves the Timeable to the mouse position or does nothing if moving is not
        possible (when theres another timeable or the beginning or end of the track
        is reached)

        @param pos: the new x_pos of the timeable
        """
        if self.group_id is not None:
            diff = pos - self.x_pos
            self.__controller.try_group_move(self.group_id, diff)

        # make move if its possible
        elif self.is_move_possible_position(pos):
            self.do_move(pos)

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
        if self.model.is_video or (self.model.is_video is None):
            mimeData.setText("is_video")
        else:
            mimeData.setText("is_audio")

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
            self.setToolTip("<font color=\"#000000\">" + self.name + "</font>")

        # get handle at current position
        handle = self.handle_at(event.pos())

        # set the cursor according to the handle
        cursor = Qt.OpenHandCursor if handle == HANDLE_MIDDLE else Qt.SizeHorCursor
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
        if self.handle_selected == HANDLE_MIDDLE:
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
            if self.group_id is None:
                self.__controller.move_timeable(self.view_id, self.mouse_press_start_pos,
                                                self.x_pos)
            else:
                diff = self.x_pos - self.mouse_press_start_pos
                self.__controller.group_move_operation(self.group_id, diff)

        # trim start or end if resize happened
        if (self.resizable_right != self.infos_on_click["resizable_right"]
                or self.resizable_left != self.infos_on_click["resizable_left"]):
            self.__controller.resize_timeable(self.infos_on_click, self.get_info_dict())

        self.mouse_press_pos = 0
        self.handle_selected = None
        self.mouse_press_rect = None

        QGraphicsItem.mouseReleaseEvent(self, event)
