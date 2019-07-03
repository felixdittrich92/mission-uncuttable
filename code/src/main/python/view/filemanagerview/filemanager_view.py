import os

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QListView
from PyQt5.QtCore import QObject, QSize
from config import Resources, Language
from ..view import View
from util.classmaker import classmaker
from view.mainview import FileListView

class FilemanagerView(classmaker(QWidget, View)):

    def __init__(self, parent=None):
        super(FilemanagerView, self).__init__(parent)
        """Loads the UI file"""
        uic.loadUi(Resources.files.filemanager, self)
        self.deleteButton = self.findChild(QObject, 'pushButton_1')
        self.deleteButton.setText(str(Language.current.filemanager.deleteButtonName))
        self.pickButton = self.findChild(QObject, 'pushButton_2')
        self.pickButton.setText(str(Language.current.filemanager.pushButtonName))
        self.listWidget = FileListView()
        self.listWidget.setObjectName("list_widget")
        old_list_widget = self.findChild(QObject, 'listWidget')
        self.layout().replaceWidget(old_list_widget, self.listWidget)
        old_list_widget.deleteLater()

        """Set properties of the Widget"""
        self.listWidget.setViewMode(QListView.IconMode)
        self.listWidget.setIconSize(QSize(115, 115))

    def set_delete_action(self, action):
        self.deleteButton.clicked.connect(action)

    def set_pick_action(self, action):
        self.pickButton.clicked.connect(action)

    def set_selected_action(self, action):
        self.listWidget.itemSelectionChanged.connect(action)

    def get_current_item(self):
        return self.listWidget.currentItem().statusTip()

    def remove_selected_item(self):
        self.listWidget.takeItem(self.listWidget.currentRow())

    def add_item(self, pixmap, file):
        icon = QIcon(pixmap.scaled(QSize(275, 200)))
        item = QListWidgetItem(os.path.basename(file)[:15], self.listWidget)
        item.setIcon(icon)
        item.setToolTip(file)
        item.setStatusTip(file)
    
    def refresh(self):
        self.update()
        print('refresh filemanager')