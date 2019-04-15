import math
from PyQt5.QtCore import QLine, Qt, QPointF, QPoint
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import QWidget


class TimeNeedle(QWidget):

    def __init__(self):
        super().__init__()
        self.init_needle()

    def init_needle(self):
        pass

    def paint_event(self):
        qp = QPainter()
        qp.begin(self)
        self.draw_widget(qp)
        qp.end()

    def draw_widget(self, qp):
        pen = QPen(QColor(214, 103, 83), 2, Qt.SolidLine)
        brush = QBrush(QColor(214, 103, 83))
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

        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawPolygon(triangle)

        starting_point = QPoint(5, 0)
        finishing_point = QPoint(5, 200)
        qp.drawLine(starting_point, finishing_point)

