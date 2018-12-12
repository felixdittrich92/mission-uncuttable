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
        self.new_project_button.clicked.connect(self.switch_frame)
        self.back_button.clicked.connect(self.switch_frame)

    def show(self):
        self.showNormal()

    def switch_frame(self):
        self.start_frame.setHidden(not self.start_frame.isHidden())
        self.new_project_frame.setHidden(not self.new_project_frame.isHidden())
