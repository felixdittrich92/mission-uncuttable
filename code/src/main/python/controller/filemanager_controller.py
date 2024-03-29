import json
import os

import cv2

from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from config import Resources, Settings, Language
from model.folder import Folder
from model.project import Project
from autocut import Presentation

RESOLUTION = 250


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

        self.__filemanager_view.new_folder_button.clicked.connect(self.new_folder)
        self.__filemanager_view.back_button.clicked.connect(self.folder_up)
        self.__filemanager_view.listWidget.itemDoubleClicked.connect(self.handle_double_click)

        """Set the functionality to the Widgets"""
        self.__filemanager_view.set_pick_action(lambda: self.pickFileNames())
        self.__filemanager_view.set_delete_action(lambda: self.remove())
        self.__filemanager_view.set_selected_action(lambda: self.selected())

        self.file_list = []
        self.pictures = []
        self.folder_stack = []

        self.print_folder_stack()

        self.__filemanager_view.listWidget.itemSelectionChanged.connect(self.toggle_delete_button)
        self.__filemanager_view.listWidget.drop.connect(self.handle_drop)

    def print_folder_stack(self):
        breadcrumbs = self.__filemanager_view.breadcrumbs
        breadcrumbs.setText("home")

        for folder in self.folder_stack:
            breadcrumbs.setText(breadcrumbs.text() + " > " + folder.get_name())

    def get_current_file_list(self):
        """Returns either the content of the filemanager """
        if len(self.folder_stack) == 0:
            file_list = self.file_list
        else:
            file_list = self.folder_stack[-1].get_content()

        return file_list

    def pickFileNames(self):
        """
        This method saves the selected files in a list and add this to the filemanager window
        This method ensures that only supported files are displayed and can be used.
        """
        self.full_path = Project.get_instance().path
        self.directory_strings = self.full_path.split('/')
        self.project_name = self.directory_strings[-2]
        self.directory_strings.pop(-1)
        self.directory_strings.pop(-1)
        self.project_path = os.path.join('/' , *self.directory_strings) #* takes every element of the list as single argument

        supported_filetypes = Settings.get_instance().get_dict_settings()["Invisible"]["filemanager_import_formats"]
        fileNames, _ = QFileDialog.getOpenFileNames(
            self.__filemanager_view,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )

        if not fileNames:
            return

        for file in fileNames:
            QApplication.processEvents()
            self.addFileNames(file)

        project = Project.get_instance()
        if not project.changed:
            project.changed = True
            self.__filemanager_view.changed.emit()

    def addFileNames(self, file):
        """
        This method create a QListWidgetItem with a preview picture and the filename as text dependent from the file type.
        This method also looks to see if the item already exists.

        @param file: the current file from the fileNames list
        @return: Nothing
        """

        if file in self.get_current_file_list():
            print("The file exist")
            return

        if file is None:
            name, result = QInputDialog.getText(self.__filemanager_view, 'Input Dialog',
                                                str(Language.current.filemanager.new_folder))
            if result is True and name not in [
                    f.get_name() for f in self.file_list if isinstance(f, Folder)]:
                file = Folder(name)
            else:
                return

        elif file.upper().endswith(('.JPG', '.PNG', 'MP4', '.MP3', '.WAV')):
            pass

        elif file.upper().endswith(('.PDF')):
            filename = os.path.split(file)
            filename = filename[-1]
            filename = filename[:-4]
            folder = Folder(filename)

            presentation = Presentation(file)
            if not os.path.isdir(os.path.join(self.project_path, self.project_name, 'files')):
                try:
                    os.mkdir(os.path.join(self.project_path, self.project_name, 'files'))
                except OSError:
                    pass
            if not os.path.isdir(os.path.join(self.project_path, self.project_name, 'files', filename)):
                try:
                    os.mkdir(os.path.join(self.project_path, self.project_name, 'files', filename))
                except OSError:
                    pass

            self.pictures = presentation.convert_pdf(self.project_path,
                                                         os.path.join(self.project_name, "files", filename),
                                                         RESOLUTION)
            for pic in self.pictures:
                folder.add_to_content(pic)

            self.file_list.append(folder)
            self.update_file_list(self.get_current_file_list())
            return

        else:
            print("The datatype is not supported")
            return

        if len(self.folder_stack) == 0:
            self.file_list.append(file)
        else:
            self.folder_stack[-1].add_to_content(file) # list[-1] returns last element

        self.update_file_list(self.get_current_file_list())

    def remove(self):
        """
        This method removes a single file or directory in the filemanager from
        the list it is stored in.
        """
        item = self.__filemanager_view.listWidget.currentItem()
        file_list = self.get_current_file_list()

        is_folder = False
        for file in file_list:
            if isinstance(file, Folder):
                if file.get_name() == item.text():
                    is_folder = True
                    item = file
                    break

        if is_folder:
            file_list.remove(item)
        else:
            file_list.remove(item.statusTip())

        self.__filemanager_view.remove_selected_item()

        project = Project.get_instance()
        if not project.changed:
            project.changed = True
            self.__filemanager_view.changed.emit()

    def selected(self):
        """This method saves the selected files to a list"""
        try:
            selected_files = []
            path = self.__filemanager_view.get_current_item()
            selected_files.append(path)
        except:
            return

    def clear(self):
        """ Removes all entries from the filemanager """
        self.file_list = []
        self.update_file_list(self.get_current_file_list())
        self.__filemanager_view.listWidget.clear()

    def get_project_filemanager(self):
        """
        Returns the files of the filemanager in JSON format.

        :return: JSON-String
        """
        return json.dumps(self.file_list, default=self.serialize)

    def create_project_filemanager(self, files):
        """
        Recreates the filemanager from a config file.

        :param files: list of filenames
        """
        files = json.loads(files)
        for f in files:
            if str(f).startswith("{"):
                folder = Folder(f["_Folder__name"])
                self.fill_folder(folder, f["_Folder__content"])

                self.file_list.append(folder)
            else:
                self.file_list.append(f)

        self.update_file_list(self.file_list)

    def fill_folder(self, folder, files):
        for f in files:
            if str(f).startswith("{"):
                new_folder = Folder(f["_Folder__name"])
                self.fill_folder(new_folder, f["_Folder__content"])
                folder.add_to_content(new_folder)
            else:
                folder.add_to_content(f)

    def new_folder(self):
        """Starts the creation of a new folder."""

        self.addFileNames(None)

        project = Project.get_instance()
        if not project.changed:
            project.changed = True
            self.__filemanager_view.changed.emit()

    def handle_double_click(self, item):
        """
        Detects a doubleclick on a folder and opens the folder.

        :param item: Item of the FileList
        """

        file_list = self.get_current_file_list()

        for file in file_list:
            if isinstance(file, Folder):
                if file.get_name() == item.text():
                    self.update_file_list(file.get_content())
                    self.folder_stack.append(file)
                    self.print_folder_stack()

                    self.__filemanager_view.back_button.setEnabled(True)
                    break

    def folder_up(self):
        """Navigates one folder back."""

        if len(self.folder_stack) > 1:
            self.folder_stack.pop()
            self.update_file_list(self.folder_stack[-1].get_content())
        elif len(self.folder_stack) == 1:
            self.folder_stack.pop()
            self.update_file_list(self.file_list)
            self.__filemanager_view.back_button.setEnabled(False)

        self.print_folder_stack()

    def update_file_list(self, list):
        """
        Displays all items of a given list in the ListView.

        :param list: List to be displayed.
        """

        self.__filemanager_view.listWidget.clear()

        for item in list:
            if isinstance(item, Folder):
                image = Resources.images.folder_icon
                pixmap = QPixmap(image)
            elif item.upper().endswith(('.JPG', '.PNG')):
                pixmap = QPixmap(item)
            elif item is not None and item.upper().endswith('.MP4'):
                video_input_path = item
                cap = cv2.VideoCapture(str(video_input_path))

                ret, frame = cap.read()
                if not ret:
                    return
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    height, width, channel = frame.shape
                    q_img = QImage(frame.data, width, height, 3 * width,
                                   QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_img)

                cap.release()
                cv2.destroyAllWindows()
            elif item is not None and item.upper().endswith(('.MP3', '*.WAV')):
                path = Resources.images.media_symbols
                filename = "mp3.png"
                path_to_file = os.path.join(path, filename)
                pixmap = QPixmap(path_to_file)

            self.__filemanager_view.add_item(pixmap, item)

    def toggle_delete_button(self):
        """
        Toggles the enabled state of the delete button, whether an item is
        selected or not.
        """

        if len(self.__filemanager_view.listWidget.selectedItems()) == 0:
            self.__filemanager_view.delete_button.setEnabled(False)
        else:
            self.__filemanager_view.delete_button.setEnabled(True)

    def handle_drop(self, item, path):
        list_widget = self.__filemanager_view.listWidget

        # get the source item
        item_list = list_widget.findItems(os.path.basename(path), Qt.MatchExactly)
        if not item_list:
            return

        source_item = item_list[0]

        # find folder
        file_list = self.get_current_file_list()
        for file in file_list:
            if isinstance(file, Folder) and file.get_name() == item.text():
                # check if file already exists in folder
                if path in file.get_content():
                    return

                # remove old file
                file_list.remove(source_item.statusTip())
                list_widget.removeItemWidget(source_item)
                self.update_file_list(self.get_current_file_list())

                # add to foldeer
                file.add_to_content(path)

                project = Project.get_instance()
                if not project.changed:
                    project.changed = True
                    self.__filemanager_view.changed.emit()

                return

    def serialize(self, obj):
        """
        Serializes objects as a dictionary.

        :param obj: Object
        :return: Dictionary that contains all the values of obj.
        """
        return obj.__dict__
