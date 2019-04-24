from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QSlider
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QPolygonF, QDrag
from PyQt5.QtCore import Qt, QPoint, QPointF, QObject, pyqtSignal, QMimeData
import sys, math


class TimeNeedle(QWidget):

    pos_changed = pyqtSignal(int)

    def __init__(self, drawing_height, top=False):
        super(TimeNeedle, self).__init__()

        self.drawing_height = drawing_height

        self.setGeometry(0, 0, 10, drawing_height)

        self.top = top
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp, )
        qp.end()

    def draw_line(self, qp):
        pen = QPen(QColor(100, 103, 100), 2, Qt.SolidLine)
        brush = QBrush(QColor(100, 103, 100))

        qp.setPen(pen)
        qp.setBrush(brush)

        if (self.top == True):
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
        finishing_point = QPoint(5, self.drawing_height)
        qp.drawLine(starting_point, finishing_point)

    def mouseMoveEvent(self, evt):
        delta = QPointF(evt.localPos().x() - 5, evt.localPos().y())

        self.move_needle(delta.x())

    def move_needle(self, x):
        self.move(self.x() + x, 0)

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
