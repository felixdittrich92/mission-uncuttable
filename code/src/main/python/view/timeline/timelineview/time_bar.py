from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt

from .size_linkable_frame import SizeLinkableFrame


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

        # debug look (everything works just as good ad before if you
        # remove this code):
        from PyQt5.QtWidgets import QHBoxLayout, QPushButton
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        for i in range(30):
            button = QPushButton(str(i))
            button.setAttribute(Qt.WA_TransparentForMouseEvents)
            self.layout().addWidget(button)

    def mousePressEvent(self, event):
        pos = event.pos()
        needle = self.findChild(QWidget, "needle_top")
        needle.pos_changed.emit(pos.x() - needle.pos().x())
        needle.update_player(pos.x())