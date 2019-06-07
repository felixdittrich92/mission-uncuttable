import os
import cv2

from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QListWidgetItem, QListView
from PyQt5.QtCore import QObject, QSize

from config import Resources
from config import Settings


class FilemanagerController:
    """
    a class used as the controller for the filemanager window.

    Manages from the resource class loaded files
    This class contains the functionality of the filemanager and loads for every supported
    file a preview picture and the show this with the filename in the ListWidget.
    Furthermore, the class contains all applications like adding and deleting files from the filemanager window.
    """

    def __init__(self, view):
        self.__filemanager_view = view

        """Set the functionality to the Widgets"""
        self.__filemanager_view.pickButton.clicked.connect(self.pickFileNames)
        self.__filemanager_view.deleteButton.clicked.connect(self.remove)
        self.__filemanager_view.listWidget.itemSelectionChanged.connect(self.selected)

        self.file_list = []

    def pickFileNames(self):
        print("hdgd")
        """
        This method saves the selected files in a list and add this to the filemanager window
        This method ensures that only supported files are displayed and can be used.
        """

        supported_filetypes = Settings.get_instance().get_dict_settings()["Invisible"]["filemanager_import_formats"]
        fileNames, _ = QFileDialog.getOpenFileNames(
            self.__filemanager_view,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )

        for file in fileNames:

            QApplication.processEvents()
            self.addFileNames(file)

    def addFileNames(self, file):
        """
        This method create a QListWidgetItem with a preview picture and the filename as text dependent from the file type.
        This method also looks to see if the item already exists.

        @param file: the current file from the fileNames list
        @return: Nothing
        """

        if file in self.file_list:
            print("The file exist")
            return

        if file.upper().endswith(('.JPG', '.PNG')):
            pixmap = QPixmap(file)
            QApplication.processEvents()
        elif file.upper().endswith(('.MP4')):
            video_input_path = file
            cap = cv2.VideoCapture(str(video_input_path))

            ret, frame = cap.read()
            if not ret:
                return
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                height, width, channel = frame.shape
                q_img = QImage(frame.data, width, height, 3 * width, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)

            cap.release()
            cv2.destroyAllWindows()
            QApplication.processEvents()

        elif file.upper().endswith(('.MP3', '*.WAV')):
            path = Resources.images.media_symbols
            filename = "mp3.png"
            path_to_file = os.path.join(path, filename)
            pixmap = QPixmap(path_to_file)
            QApplication.processEvents()

        else:
            print("The datatype is not supported")
            return

        QApplication.processEvents()
        icon = QIcon(pixmap.scaled(QSize(275,200)))
        item = QListWidgetItem(os.path.basename(file)[:15], self.listWidget)
        item.setIcon(icon)
        item.setToolTip(file)
        item.setStatusTip(file)
        self.file_list.append(file)

    def remove(self):
        """This method removes a single file in the filemanager window and in the list"""
        try:
            path = self.listWidget.currentItem().statusTip()
            self.file_list.remove(path)
            self.listWidget.takeItem(self.listWidget.currentRow())
        except:
            return

    def selected(self):
        """This method saves the selected files to a list"""
        try:
            selected_files = []
            path = self.listWidget.currentItem().statusTip()
            selected_files.append(path)
        except:
            return

    def get_project_filemanager(self):
        """ Returns a list with all the files in the filemanager. """
        return self.file_list

    def create_project_filemanager(self, files):
        """
        Recreates the filemanager from a config file.

        @param data: list of filenames
        """
        for f in files:
            self.addFileNames(f)
