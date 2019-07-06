from PyQt5.QtCore import (QPoint, QRectF, QByteArray, QDataStream, QIODevice,
                          QMimeData, Qt, QSize, pyqtSignal)
from PyQt5.QtGui import QBrush, QColor, QDrag
from PyQt5.QtWidgets import QMenu, QDialog, QAction, QApplication, QGraphicsItem, QGraphicsRectItem

from controller import TimelineController
from view.timeline.util.timelineview_utils import *
from model.data import FileType
from config import Language
from util.timeline_utils import get_pixmap_from_file
from .timeable_settings_view import TimeableSettingsView
import openshot

TIMEABLE_MIN_WIDTH = 8
RESIZE_AREA_WIDTH = 3
TIMEABLE_COLOR = "#AE6759"

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

    # Todo: Add missing parameter documentation for
    #         - res_left
    #         - res_right
    #         - model
    #         - view_id
    #         - track_id
    def __init__(
            self,
            name,
            start,
            length,
            height,
            res_left,
            res_right,
            model,
            view_id,
            track_id,
            parent=None):
        """
        Create a new C{TimeableView} with the specified start and length
        and add it to the given C{TrackView} accordingly.

        @param name:   the name that is displayed in the top left corner of the timeable
        @param start:  The time point at which the first frame of the
                       timeable is positioned. This frame is the very
                       first one which is not trimmed by res_left.
        @type start:   int
        @param length: The length of the timeable in frames. It is
                       measured from the relative time point specified
                       by res_left to the time point specified by
                       res_right. The trimmed ends aren't taken into
                       this value.
        @type length:  int
        @param height: timeable height, should be the same as track height
        """
        super(TimeableView, self).__init__(parent)

        self.model = model
        self.model.add_to_timeline()

        self.name = name
        self.__start = start
        self.__length = length
        self.view_id = view_id
        self.track_id = track_id
        self.__width = length
        self.height = height
        self.__x_pos = start
        self.__zoom_factor = 1

        self.__controller = TimelineController.get_instance()

        if self.__controller.is_overlay_track(self.track_id):
            self.model.corner(True)

        self.set_pixmap()

        self.resizable_left = res_left
        self.resizable_right = res_right
        self.name_visible = False

        self.setRect(self.boundingRect())
        self.setPos(self.__x_pos, 0)

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
        return QRectF(QRectF(0, 0, self.__width, self.height))

    def paint(self, painter, option, widget):
        """overwritten Qt function that paints the item."""
        brush = QBrush(QColor(TIMEABLE_COLOR))
        painter.setBrush(brush)
        painter.drawRect(self.rect())

        # show thumbnail if there is enough space
        if self.__width > 101 and self.pixmap is not None:
            painter.drawPixmap(QPoint(1, 1), self.pixmap)

        # only draw name if it fits on the timeable
        # if it doesn't fit a tooltip will be shown (see hoverMoveEvent)
        if painter.fontMetrics().width(self.name) + 100 <= self.__width:
            painter.setPen(QColor(245, 245, 245))
            painter.drawText(QPoint(100, 20), self.name)

            self.name_visible = True
        else:
            self.name_visible = False

    def get_info_dict(self):
        return {
            "name": self.name,
            "start": self.__start,
            "length": self.__length,
            "width": self.__width,
            "height": self.height,
            "resizable_right": self.resizable_right,
            "resizable_left": self.resizable_left,
            "x_pos": self.__x_pos,
            "view_id": self.view_id,
            "track_id": self.track_id,
            "model": self.model.get_info_dict()
        }

    def set_pixmap(self):
        """ Sets the pixmap to the first frame """
        frame = self.model.get_first_frame()

        QApplication.processEvents()

        px = get_pixmap_from_file(self.model.file_name, frame)
        if px is not None:
            self.pixmap = px.scaled(QSize(100, self.height), Qt.KeepAspectRatio)
        else:
            self.pixmap = None

    def set_start(self, start):
        """ Set the start of the timeable.

        @param start:  The time point at which the first frame of the
                       timeable is positioned. This frame is the very
                       first one which is not trimmed by res_left.
        @type start:   int
        """
        self.__start = start
        self.__refresh_x_pos()

    def set_length(self, length):
        """ Set the length of the timeable without changing its start.

        @param length: The length of the timeable in frames. It is
                       measured from the relative time point specified
                       by res_left to the time point specified by
                       res_right. The trimmed ends aren't taken into
                       this value.
        @type length:  int
        """
        self.__length = length
        self.__refresh_width()

    def set_zoom_factor(self, zoom_factor):
        """ Set the zoom factor.

        @param zoom_factor: The new zoom factor in pixels per frame.
        @type zoom_factor:  float
        """
        self.__zoom_factor = zoom_factor
        self.__refresh_width()
        self.__refresh_x_pos()

    def __set_x_pos(self, x_pos):
        """ Set the x pos. """
        self.__x_pos = x_pos
        self.prepareGeometryChange()
        self.setPos(self.__x_pos, 0)
        # self.prepareGeometryChange()
        self.setRect(self.boundingRect())

    def __set_width(self, width):
        """ Sets the width of the timeable """
        # the bounding rect is dependent on the width
        # so we have to call prepareGeometryChange
        # otherwhise the program can randomly crash
        self.__width = width
        self.prepareGeometryChange()
        self.setRect(self.boundingRect())

    def get_x_pos(self):
        return self.__x_pos

    def get_end_pos(self):
        return self.__x_pos + self.__width

    def get_width(self):
        return self.__width

    def __refresh_width(self):
        """
        Refresh the width depending on the length and the zoom factor of
        the timeable.
        """
        self.__set_width(frames_to_pixels(self.__length, self.__zoom_factor))

    def __refresh_x_pos(self):
        """
        Refresh the x position of the timeable depending on the start
        and the zoom factor of the timeable.
        """
        self.__set_x_pos(frames_to_pixels(self.__start, self.__zoom_factor))

    def __refresh_geometry(self):
        """
        Refresh the geometry depending on the length, the start and the
        zoom factor of the timeable.
        """
        self.__refresh_width()
        self.__refresh_x_pos()

    def contextMenuEvent(self, event):
        """shows a menu on rightclick"""
        event.accept()

        menu = QMenu()

        delete = QAction(str(Language.current.timeable.delete))
        menu.addAction(delete)
        delete.triggered.connect(lambda: self.delete(hist=True))

        cut = QAction(str(Language.current.timeable.cut))
        menu.addAction(cut)
        cut.triggered.connect(lambda: self.cut(event.pos().x()))

        settings = QAction(str(Language.current.timeable.settings))
        menu.addAction(settings)
        settings.triggered.connect(lambda: self.settings())

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

    def remove_from_scene(self):
        """ Removes the timeableview from the track """
        self.scene().removeItem(self)

    def cut(self, pos):
        """
        cuts the timeable in two parts

        @param pos: x position on the timeable where it's cut
        """
        if pos < TIMEABLE_MIN_WIDTH and self.__width >= 2 * TIMEABLE_MIN_WIDTH:
            return

        self.__controller.split_timeable(self.view_id, self.resizable_right,
                                         self.__width, self.model.clip.End(), pos)

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
            self.__width - (2 * RESIZE_AREA_WIDTH), self.height)

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
            w = self.__width - diff

            if ((w <= TIMEABLE_MIN_WIDTH or diff + self.scenePos().x() < 0)
                    or (diff < self.resizable_left and not is_image)):
                return

            new_x_pos = self.__x_pos + diff
            if self.collides_with_other_timeable(QRectF(new_x_pos, 0, w, self.height)):
                return

            self.resizable_left -= diff

            self.prepareGeometryChange()
            self.__width = w
            self.__x_pos = self.__x_pos + diff
            self.setPos(self.__x_pos, 0)

        elif self.handle_selected == HANDLE_RIGHT:
            diff = (self.mouse_press_rect.right() + pos
                    - self.mouse_press_pos - self.__width)
            w = self.__width + diff

            if ((w > self.scene().width() or w <= TIMEABLE_MIN_WIDTH)
                    or (diff > self.resizable_right and not is_image)):
                return

            if self.collides_with_other_timeable(QRectF(self.__x_pos, 0, w, self.height)):
                return

            self.resizable_right -= diff

            self.prepareGeometryChange()
            self.__width = w

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
        r = QRectF(pos, 0, self.__width, self.height)
        colliding = self.scene().items(r)
        if (len(colliding) > 1 or (len(colliding) == 1 and colliding != [self])):
            return

        # move only if the new position is still inside the track
        if pos >= 0 and pos + self.__width <= self.scene().width():
            self.__x_pos = 0 if pos < 5 else pos

            self.setPos(self.__x_pos, 0)

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
        self.mouse_press_start_pos = self.__x_pos
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
        if self.__x_pos != self.mouse_press_start_pos:
            self.__controller.move_timeable(self.view_id, self.mouse_press_start_pos,
                                            self.__x_pos)

        # trim start or end if resize happened
        if (self.resizable_right != self.infos_on_click["resizable_right"]
                or self.resizable_left != self.infos_on_click["resizable_left"]):
            self.__controller.resize_timeable(self.infos_on_click, self.get_info_dict())

        self.mouse_press_pos = 0
        self.handle_selected = None
        self.mouse_press_rect = None

        QGraphicsItem.mouseReleaseEvent(self, event)
