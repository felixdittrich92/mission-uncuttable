from PyQt5.QtGui import QPen, QColor, QPainter
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint

from .size_linkable_frame import SizeLinkableFrame

LINE_WIDTH = 1
COLOR = "#F5F5F5"


class TimeBar(SizeLinkableFrame):
    """
    Extends SizeLinkableFrame to a frame showing a time bar.

    Not very implemented yet. So you have nothing to expect except for
    a few buttons making scrolling movement in the GUI visible. And it's
    orange!
    """

    def __init__(self, parent=None):
        """
        Create a TimeBar with a simple debug look.

        :param paren -> Nonet: the parent component
        """
        super(TimeBar, self).__init__(parent)

        # setting the size
        self.setFixedHeight(25)
        self.setFixedWidth(2000)

        self.__color = QColor(COLOR)
        self.__qp = QPainter()

    def mousePressEvent(self, event):
        pos = event.pos()
        needle = self.findChild(QWidget, "needle_top")
        needle.pos_changed.emit(pos.x() - needle.pos().x())
        needle.update_player(pos.x())

    def paintEvent(self, e):
        self.__qp.begin(self)

        __pen = QPen(self.__color, LINE_WIDTH, Qt.SolidLine)

        self.__qp.setPen(__pen)

        x = 5
        counter = 0
        width = self.width()
        while width > 0:

            self.draw_line(x, counter % 2 == 0)
            counter += 1
            x += 10
            width -= 10

        self.__qp.end()

    def draw_line(self, x, long_line):
        if long_line:
            starting_point = QPoint(x, int((self.height() / 3)))
        else:
            starting_point = QPoint(x, int((self.height() / 3 * 2)))

        finishing_point = QPoint(x, self.height())
        self.__qp.drawLine(starting_point, finishing_point)