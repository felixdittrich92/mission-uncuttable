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
        self.folder_line_edit.setText(settings.Invisible.projects_path)

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

    def __start_videoeditor_controller(self, filepath):
        """
        Closes the start window and starts the video-editor window.

        :param filepath: String: Path to the project file
        """

        self.__start_view.close()
        video_editor_view = VideoEditorView()
        timeline_controller = TimelineController.get_instance()
        timeline_controller.create_default_tracks()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()
        self.__video_editor_controller.new_project(filepath)
        self.__video_editor_controller.set_title_saved()

    def __start_autocut_controller(self, path, project_name, filename):
        """
        Closes the start window and starts the autocut window.
        :param path: String - Path to the folder where the project folder will be created in.
        :param project_name: String - Name of the project
        :param filename: String - Name of project file *.uc
        """
        self.__start_view.close()
        autocut_view = AutocutView()
        self.__autocut_controller = AutocutController(autocut_view, self, path, project_name, filename)
        self.__autocut_controller.start()

    def __load_project(self):
        """ Closes the start window and loads the selected project """
        # get path from listwidget
        project_list = self.__start_view.select_project_widget.projects_list_view
        # return if no project is selected
        if project_list.currentItem() is None:
            return

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

            if "groups" in project_data:
                timeline_controller.create_project_groups(project_data["groups"])

            # set project path
            project = Project.get_instance()
            project.path = path
            project.changed = False

            # show videoeditor
            self.__start_view.close()
            self.__video_editor_controller.start()

    def __new_project(self, type):
        """
        Creates the project folder and starts the necessary controler.

        :param type: String - Type of the new Project ["AutoCut", "SimpleCut"]
        """
        path = os.path.expanduser(self.folder_line_edit.text())
        name = self.name_line_edit.text()
        projectpath = os.path.join(path, name)
        if projectpath == "" or name == "":
            title = str(Language.current.errors.incomplete.msgboxtitle)
            icon = QMessageBox.Critical
            text = str(Language.current.errors.incomplete.msgboxtext)
            info = str(Language.current.errors.incomplete.msgboxinfotext)
            self.__show_message_box(title, icon, text, info)
            return
        else:
            if os.path.isdir(projectpath):
                title = str(Language.current.errors.projectexists.msgboxtitle)
                icon = QMessageBox.Critical
                text = str(Language.current.errors.projectexists.msgboxtext)
                info = str(Language.current.errors.projectexists.msgboxinfotext)
                self.__show_message_box(title, icon, text, info)
                return
            else:
                try:
                    os.mkdir(projectpath)
                    filename = name + ".uc"

                except OSError:
                    pass

                if os.path.isdir(projectpath) and type == "SimpleCut":
                    self.__start_videoeditor_controller(os.path.join(projectpath, filename))

                elif os.path.isdir(projectpath) and type == "AutoCut":
                    os.mkdir(os.path.join(projectpath, "files"))
                    self.__start_autocut_controller(path, name, filename)
                else:
                    title = str(Language.current.errors.writeerror.msgboxtitle)
                    icon = QMessageBox.Critical
                    text = str(Language.current.errors.writeerror.msgboxtext)
                    info = str(Language.current.errors.writeerror.msgboxinfotext)
                    self.__show_message_box(title, icon, text, info)

    def __pick_folder(self):
        """ Opens folder picker"""
        file = str(QFileDialog.getExistingDirectory(self.__start_view, "Select Directory"))
        self.folder_line_edit.setText(file)

    def __show_message_box(self, title, icon, text, info):
        """
        Creates and shows a QMessageBox.

        :param title: String - Title of the message box
        :param icon: Icon of the message box, e.g. QMessageBox.Critical
        :param text: String - Text of the message box
        :param info: String - More text for the message box to provide further information
        """
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setIcon(icon)
        message_box.setText(text)
        message_box.setInformativeText(info)
        message_box.exec_()
