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
        self.new_project_frame.hide()
        self.new_project_button.clicked.connect(self.switch_frame_to_new_project)
        self.back_button.clicked.connect(self.switch_frame_to_start)

    def show(self):
        self.showNormal()

    def switch_frame_to_new_project(self):
        self.start_frame.hide()
        self.new_project_frame.show()

    def switch_frame_to_start(self):
        self.start_frame.show()
        self.new_project_frame.hide()

