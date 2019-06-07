from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QListWidgetItem, QListView, QListWidget
from PyQt5.QtCore import QObject, QSize
from PyQt5 import uic
from config import Resources

from view.mainview import FileListView

class FilemanagerView(QWidget):
    
    def __init__(self, parent=None):
        super(FilemanagerView, self).__init__(parent)
        """Loads the UI file"""
        uic.loadUi(Resources.files.filemanager, self)
        self.deleteButton = self.findChild(QObject, 'pushButton_1')
        self.pickButton = self.findChild(QObject, 'pushButton_2')
        self.listWidget = FileListView()
        self.listWidget.setObjectName("list_widget")
        old_list_widget = self.findChild(QObject, 'listWidget')
        self.layout().replaceWidget(old_list_widget, self.listWidget)
        old_list_widget.deleteLater()

        """Set properties of the Widget"""
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setIconSize(QSize(115, 115))

