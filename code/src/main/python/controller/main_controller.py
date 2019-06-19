import os
import json

from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog

from config import Settings
from controller import VideoEditorController, AutocutController, TimelineController
from view import VideoEditorView
from model.project import Project
from view import AutocutView
from config import Language


class MainController:
    """A class used as the Controller, that manages the windows of the program."""
    def __init__(self, view):
        self.__start_view = view
        manual_cut_button = self.__start_view.findChild(QWidget, "manual_cut_button")
        manual_cut_button.clicked.connect(lambda: self.__new_project("SimpleCut"))

        auto_cut_button = self.__start_view.findChild(QWidget, "auto_cut_button")
        auto_cut_button.clicked.connect(lambda: self.__new_project("AutoCut"))

        load_project_button = self.__start_view.findChild(QWidget, "load_project_button")
        load_project_button.setText(str(Language.current.startview.load_project))
        load_project_button.clicked.connect(self.__load_project)

        new_project_button = self.__start_view.findChild(QWidget, "new_project_button")
        back_button = self.__start_view.findChild(QWidget, "back_button")

        new_project_button.clicked.connect(self.__start_view.switch_frame)
        back_button.clicked.connect(self.__start_view.switch_frame)

        pick_folder_button = self.__start_view.findChild(QWidget, "pick_folder_button")
        pick_folder_button.clicked.connect(self.__pick_folder)

        settings = Settings.get_instance().get_settings()

        self.folder_line_edit = self.__start_view.findChild(QWidget, "folder_line_edit")
        self.folder_line_edit.setText(settings.general.projects_path.current)

        self.name_line_edit = self.__start_view.findChild(QWidget, "name_line_edit")

    def start(self):
        """Calls show() of StartView"""
        self.__start_view.show()

    def stop(self):
        """Closes the start window and tries to close the video-editor window."""
        self.__start_view.close()
        try:
            self.__video_editor_controller.stop()
        except NameError:
            pass

    def __start_videoeditor_controller(self):
        """Closes the start window and starts the video-editor window."""

        self.__start_view.close()
        video_editor_view = VideoEditorView()
        timeline_controller = TimelineController.get_instance()
        timeline_controller.create_default_tracks()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()

    def __start_autocut_controller(self):
        self.__start_view.close()
        autocut_view = AutocutView()
        self.__autocut_controller = AutocutController(autocut_view, self)
        self.__autocut_controller.start()

    def __load_project(self):
        """ Closes the start window and loads the selected project """
        # get path from listwidget
        project_list = self.__start_view.select_project_widget.projects_list_view
        path = project_list.currentItem().text()

        # check if file exists
        if os.path.isfile(path):
            video_editor_view = VideoEditorView()
            self.__video_editor_controller = VideoEditorController(video_editor_view)

            with open(path, 'r') as f:
                project_data = json.load(f)

            # set up timeline
            timeline_controller = TimelineController.get_instance()
            if "timeline" in project_data:

                timeline_controller.create_project_timeline(project_data["timeline"])
            else:
                timeline_controller.create_default_tracks()

            # set up filemanager
            if "filemanager" in project_data:
                filemanager = self.__video_editor_controller.get_filemanager_controller()
                filemanager.create_project_filemanager(project_data["filemanager"])

            # set project path
            project = Project.get_instance()
            project.path = path

            # show videoeditor
            self.__start_view.close()
            self.__video_editor_controller.start()

        # TODO show error window if path does not exist

    def __new_project(self, type):
        path = self.folder_line_edit.text()
        name = self.name_line_edit.text()
        path = os.path.join(path, name)
        if path == "" or name == "":
            title = str(Language.current.errors.incomplete.msgboxtitle)
            icon = QMessageBox.Critical
            text = str(Language.current.errors.incomplete.msgboxtext)
            info = str(Language.current.errors.incomplete.msgboxinfotext)
            self.__show_message_box(title, icon, text, info)
            return
        else:
            if os.path.isdir(path):
                title = str(Language.current.errors.projectexists.msgboxtitle)
                icon = QMessageBox.Critical
                text = str(Language.current.errors.projectexists.msgboxtext)
                info = str(Language.current.errors.projectexists.msgboxinfotext)
                self.__show_message_box(title, icon, text, info)
                return
            else:
                try:
                    os.mkdir(path)
                except OSError:

                    pass

                if os.path.isdir(path) and type == "SimpleCut":
                    self.__start_videoeditor_controller()
                elif os.path.isdir(path) and type == "AutoCut":
                    self.__start_autocut_controller()
                else:
                    title = str(Language.current.errors.writeerror.msgboxtitle)
                    icon = QMessageBox.Critical
                    text = str(Language.current.errors.writeerror.msgboxtext)
                    info = str(Language.current.errors.writeerror.msgboxinfotext)
                    self.__show_message_box(title, icon, text, info)

    def __pick_folder(self):
        file = str(QFileDialog.getExistingDirectory(self.__start_view, "Select Directory"))
        self.folder_line_edit.setText(file)

    def __show_message_box(self, title, icon, text, info):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setIcon(icon)
        message_box.setText(text)
        message_box.setInformativeText(info)
        message_box.exec_()