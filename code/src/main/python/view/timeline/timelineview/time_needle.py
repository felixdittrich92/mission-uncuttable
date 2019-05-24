from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPolygonF
from PyQt5.QtCore import Qt, QPoint, QPointF, pyqtSignal
import math

from view.preview.preview import PreviewView

NEEDLE_COLOR = "#D66853"
NEEDLE_WIDTH = 10
NEEDLE_LINE_WIDTH = 2


class TimeNeedle(QWidget):
    """
    A Class that manages the gui for the preview needle of the timeline.

    The needle consists of two elements, the top and the bottom part.
    The first part is draw with a triangle on top and the bottom part is just a
    single line.
    Both parts need to be separate objects. The timelines layout requires this.
    Because of that both objects need to be synced.
    """

    pos_changed = pyqtSignal(int)

    def __init__(self, drawing_height, top=False):
        """
        Initializes TimeNeedle.

        Sets the drawing height, whether its the top part or not, the color,
        the cursor, the default geometry and connects the object to the
        position changed signal.

        :param drawing_height: Integer: Height the needle part should adopt
        :param top: Boolean: Whether its the top part or not
        """
        super(TimeNeedle, self).__init__()

        self.__drawing_height = drawing_height
        self.__top = top
        self.__color = QColor(NEEDLE_COLOR)
        self.__qp = QPainter()

        self.setGeometry(0, 0, NEEDLE_WIDTH, self.__drawing_height)
        self.setCursor(Qt.PointingHandCursor)
        self.pos_changed.connect(self.move_needle)

        preview = PreviewView.get_instance()
        preview.frame_changed.connect(self.move)
    def paintEvent(self, e):
        self.__qp.begin(self)
        self.draw_needle(self.__qp)
        self.__qp.end()

    def draw_needle(self, qp):
        """
        Draws the Needle.

        Whether the top or the bottom part of the needle is going to be drawn,
        the function operates differently. The top part is drawn with a triangle,
        the bottom part is just a single line.

        :param qp: QPainter
        """
        __pen = QPen(self.__color, NEEDLE_LINE_WIDTH, Qt.SolidLine)
        __brush = QBrush(self.__color)

        qp.setPen(__pen)
        qp.setBrush(__brush)

        if self.__top:
            triangle = QPolygonF()
            n = 3
            r = self.width() - 2
            s = 90
            w = 360 / n

            for i in range(n):
                t = w * i + s
                x = r * math.cos(math.radians(t))
                y = (r - 3) * math.sin(math.radians(t))
                triangle.append(QPointF(self.width()/2 + x, 0 + y))

            qp.drawPolygon(triangle)

        starting_point = QPoint(int(self.width()/2), 0)
        finishing_point = QPoint(int(self.width()/2), self.__drawing_height)
        qp.drawLine(starting_point, finishing_point)

    def set_drawing_height(self, new_height):
        """
        Sets the height of the needle part and repaints it.

        :param new_height: Integer: The new height of the needle part
        """
        self.__drawing_height = new_height
        self.setFixedHeight(new_height)
        self.repaint()

    def mouseMoveEvent(self, evt):
        """
        Handles drag and drop.

        The position gets emitted to a signal, which the other needle part can
        receive.

        :param evt: EventHandler
        """
        delta = QPointF(evt.localPos().x() - self.width()/2, evt.localPos().y())
        # if (self.mapToParent(QPoint(0, 0)).x() < (self.width)):
        # print(self.mapToParent(QPoint(0, 0)).x())
        # print(self.mapTo(self.parent().parent().parent()), QPoint(0, 0))
        # timeline_scroll_area = self.parent().parent().parent().parent()
        # track_scroll_area = timeline_scroll_area.findChild(QWidget, "track_scroll_area")
        # horizontal_scroll_bar = timeline_scroll_area.findChild(QWidget, "horizontal_scroll_bar")
        # print(horizontal_scroll_bar)
        
        # if self.mapTo(track_scroll_area, QPoint(0, 0)).x() < 20:
        #     print("TRUE")
        #     old_value = horizontal_scroll_bar.value()
        #     horizontal_scroll_bar.setValue(old_value - 1)

        self.pos_changed.emit(delta.x())

    def move_needle(self, delta_x):
        """
        Moves the needle part to another location.

        Also detects collisions on boundaries.

        :param x: Integer: new x value
        """
        half_width = self.width()/2
        parent_width = self.parent().parent().parent().parent().findChild(QWidget, "track_frame").width()
        new_x = self.x() + delta_x

        if new_x >= half_width and new_x < parent_width - half_width:
            self.move(new_x, 0)

    def move_needle_absolute(self, x):
        self.move()

    def mousePressEvent(self, event):
        """
        Sets the cursor to a closed hand when mouse button is pressed.

        :param event: EventHandler
        """
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        """
        Sets the cursor to a pointing hand when mouse button is released.

        :param event: EventHandler
        """
        self.setCursor(Qt.PointingHandCursor)
