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

        :param parent: the parent component
        """
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

