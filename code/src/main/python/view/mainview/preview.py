from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
import os

class PreviewView(QWidget):
    def __init__(self):
        super(PreviewView, self).__init__()
        path = os.path.abspath('src/main/python/view/mainview')
        uic.loadUi(os.path.join(path, 'form.ui'), self)