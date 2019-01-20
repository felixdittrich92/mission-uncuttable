from .size_connectable_frame import SizeConnectableFrame

class TimeBar(SizeConnectableFrame):
    """
    Can it be so hard to describe a time bar? In my head it is so
    simple, but I can't find words for the image in my mind :(

    The TimeBar is simply a drawing consisting of a horizontal line
    going over the full width of the widget. On this line there are
    equally spaced small vertical lines. Every fifth one is a little
    longer than the others and every tenth one is even longer than
    these. The vertical lines shall give a visual association of time
    points with Timeables in the Timeline.
    Important time points are written to the corresponding position of
    the TimeBar.

    The TimeBar is drawn according to the zoom factor of the
    TimelineView so that at every time the TimeBar fits the needs to be
    as useful as possible for the user.
    """

    def __init__(self, parent=None):
        super(TimeBar, self).__init__(parent)

        # setting the size
        self.setFixedHeight(40)
        self.setFixedWidth(2000)

        # debug look (everything works just as good ad before if you
        # remove this code):
        from PyQt5.QtWidgets import QHBoxLayout, QPushButton
        self.setLayout(QHBoxLayout())
        for i in range(30):
            self.layout().addWidget(QPushButton(str(i)))
        self.setStyleSheet("background-color: orange")
