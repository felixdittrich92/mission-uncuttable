from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QSlider
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPolygonF, QDrag
from PyQt5.QtCore import Qt, QPoint, QPointF, QObject, pyqtSignal, QMimeData
import sys, math


class TimeNeedle(QWidget):

    pos_changed = pyqtSignal(int)

    def __init__(self, drawing_height, top=False):
        super(TimeNeedle, self).__init__()

        self.__drawing_height = drawing_height
        self.__top = top
        self.__color = QColor(100, 103, 100)
        self.__qp = QPainter()

        self.setGeometry(0, 0, 10, self.__drawing_height)
        self.setCursor(Qt.PointingHandCursor)
        self.pos_changed.connect(self.move_needle)

    def paintEvent(self, e):
        self.__qp.begin(self)
        self.draw_line(self.__qp)
        self.__qp.end()

    def draw_line(self, qp):
        __pen = QPen(self.__color, 2, Qt.SolidLine)
        __brush = QBrush(self.__color)

        qp.setPen(__pen)
        qp.setBrush(__brush)

        if self.__top:
            triangle = QPolygonF()
            n = 3
            r = 10
            s = 90
            w = 360 / n

            for i in range(n):
                t = w * i + s
                x = r * math.cos(math.radians(t))
                y = (r - 4) * math.sin(math.radians(t))
                triangle.append(QPointF(5 + x, 0 + y))

            qp.drawPolygon(triangle)

        starting_point = QPoint(5, 0)
        finishing_point = QPoint(5, self.__drawing_height)
        qp.drawLine(starting_point, finishing_point)

    def set_drawing_height(self, new_height):
        self.__drawing_height = new_height
        self.setFixedHeight(new_height)
        self.repaint()

    def mouseMoveEvent(self, evt):
        delta = QPointF(evt.localPos().x() - 5, evt.localPos().y())

        self.pos_changed.emit(delta.x())
        print(self.parentWidget())


    def move_needle(self, x):
        self.move(self.x() + x, 0)

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
