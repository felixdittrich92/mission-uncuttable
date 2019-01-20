from .size_connectable_frame import SizeConnectableFrame


class TrackButtonFrame(SizeConnectableFrame):
    """
    Todo: doc
    """

    def __init__(self, parent=None):
        super(TrackButtonFrame, self).__init__(parent)

        # set size
        self.setFixedWidth(50)
        self.setFixedHeight(200)

        # debug look (everything works just as good ad before if you
        # remove this code):
        from PyQt5.QtWidgets import QVBoxLayout, QPushButton
        self.setLayout(QVBoxLayout())
        for i in range(4):
            self.layout().addWidget(QPushButton(str(i)))
        self.setStyleSheet('background-color: orange')