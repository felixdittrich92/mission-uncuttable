from PyQt5 import QtWidgets
from PyQt5 import QtCore


# extrem unvollständig
class TrackView(QtWidgets.Widget):
    def __init__(self):
        super(TrackView, self).__init__()
        self.timeables = []

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

    def dragEnterEvent(self, event):
        pass

    def dropEvent(self, event):
        pass
