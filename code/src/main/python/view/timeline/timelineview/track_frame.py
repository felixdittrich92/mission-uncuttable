from .size_connectable_frame import SizeConnectableFrame


class TrackFrame(SizeConnectableFrame):
    """
    Todo: doc
    """

    def __init__(self, parent=None):
        super(TrackFrame, self).__init__(parent)

        self.setFixedSize(5000, 3000)

        # debug look (everything works just as good ad before if you
        # remove this code):
        from PyQt5.QtWidgets import QGridLayout, QPushButton
        self.setLayout(QGridLayout())
        for i in range(30):
            for j in range(4):
                self.layout().addWidget(QPushButton(str(i)+","+str(j)), j, i)
        self.setStyleSheet("background-color: orange")