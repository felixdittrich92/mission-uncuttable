# import os
# import sys

from PyQt5 import QtWidgets
from PyQt5 import uic


class TimeableView(QtWidgets.QWidget):
    def __init__(self, timeable_name, width, height):
        super(TimeableView, self).__init__()
        self.timeable_name = timeable_name
        self.width = width
        self.height = height

        self.setup_ui()

    def setup_ui(self):
        # path = os.path.abspath('src/main/python/view/timeableview/')
        # uic.loadUi(path + '/timeable_widget.ui', self)
        uic.loadUi('timeable_view.ui', self)
        self.findChild(QtWidgets.QLabel, 'name').setText(self.timeable_name)
        self.resize(self.width, self.height)

    # rightclick menu
    def contextMenuEvent(self, event):
        event.accept()
        self._show_context_menu(self, event.globalPos())

    def _show_context_menu(self, button, pos):
        menu = QtWidgets.QMenu()
        menu.addAction('umbennenen')
        menu.addAction('löschen')
        menu.exec_(pos)


# nur zum testen wie es aussieht
# eigentlich werden die timeables in eine spur eingefügt
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     t = TimeableView("Video 1", 300, 100)
#     t.show()
#     app.exec_()
