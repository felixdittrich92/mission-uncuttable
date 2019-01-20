from PyQt5 import QtWidgets
from PyQt5 import QtCore

from view.timeline.timeableview import TimeableView


class TrackView(QtWidgets.QGraphicsView):
    def __init__(self, width, height):
        super(TrackView, self).__init__()

        self.width = width
        self.height = height
        self.scene = QtWidgets.QGraphicsScene()

        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self):
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(self.height)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.scene.setSceneRect(0, 0, self.width, self.height)
        self.setScene(self.scene)

        rect = TimeableView("name", 300, self.height, 0)
        self.scene.addItem(rect)
        rect2 = TimeableView("name", 100, self.height, 400)
        self.scene.addItem(rect2)
