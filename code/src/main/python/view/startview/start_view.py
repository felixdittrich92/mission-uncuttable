from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
import os


class StartView(QMainWindow):
    """
    @TODO Doc
    """
    def __init__(self):
        super(StartView, self).__init__()
        path = os.path.abspath('src/main/python/view/startview')
        uic.loadUi(path + '/start_view.ui', self)

    def show(self):
        self.showNormal()
