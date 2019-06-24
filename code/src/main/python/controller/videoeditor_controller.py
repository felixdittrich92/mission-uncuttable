import json
import sys

from PyQt5.QtWidgets import QFileDialog

from shortcuts import ShortcutLoader
from .settings_controller import SettingsController
from .projectsettings_controller import ProjectSettingsController
from .timeline_controller import TimelineController
from model.project import Project
from view.settingsview import SettingsView, ProjectSettingsView
from view.exportview import ExportView
from view.filemanagerview import FilemanagerView
from .filemanager_controller import FilemanagerController
from projectconfig import Projectsettings
from config import Settings


class VideoEditorController:
    """
    A class used as the Controller for the video-editor window.

    Manages starting and stopping of the video-editor window.
    """
    def __init__(self, view):
        self.__video_editor_view = view
        self.__video_editor_view.save_project.connect(self.__start_save)
        self.__timeline_controller = TimelineController.get_instance()
        self.__filemanager_view = FilemanagerView()
        self.__filemanager_controller = FilemanagerController(self.__filemanager_view)

        self.__video_editor_view.set_filemanager_view(self.__filemanager_view)
        self.__video_editor_view.action_settings.triggered.connect(
            self.__start_settings_controller)
        self.__settings_controller = SettingsController(None)
        self.__video_editor_view.action_projectsettings.triggered.connect(
            self.__start_projectsettings_controller)
        self.__projectsettings_controller = ProjectSettingsController(None)
        self.__video_editor_view.actionExport.triggered.connect(
            self.__start_export_controller)
        self.__video_editor_view.actionUndo.triggered.connect(
            self.__start_undo)
        self.__video_editor_view.actionRedo.triggered.connect(
            self.__start_redo)
        self.__video_editor_view.actionSpeichern.triggered.connect(
            self.__start_save)
        self.__video_editor_view.actionSpeichern_als.triggered.connect(
            self.__start_save_as)
        self.__video_editor_view.actionOeffnen.triggered.connect(
            self.__start_open)

        self.__history = Project.get_instance().get_history()
        ShortcutLoader(self.__video_editor_view)

    def __show_view(self):
        """Calls show() of 'VideoEditorView'."""
        self.__video_editor_view.show()

    def start(self):
        """Calls '__show_view()' of VideoEditorController"""
        self.__show_view()

    def stop(self):
        """Closes the video-editor Window."""
        self.__video_editor_view.close()
        sys.exit(0)

    def __start_settings_controller(self):
        """Opens the settings window"""
        if self.__settings_controller.checkIfClosed():
            self.settings_view = SettingsView()
            self.__settings_controller = SettingsController(self.settings_view)
            self.__settings_controller.start()
        else:
            self.__settings_controller.focus()

    def __start_projectsettings_controller(self):
        """Opens the projectsettings window"""
        if self.__projectsettings_controller.checkIfClosed():
            self.projectsettings_view = ProjectSettingsView()
            self.__projectsettings_controller = ProjectSettingsController(self.projectsettings_view)
            self.__projectsettings_controller.start()
        else:
            self.__projectsettings_controller.focus()

    def __start_export_controller(self):
        """shows the export view"""
        export_view = ExportView()
        export_view.start()

    def __start_undo(self):
        """ Undo last action """
        try:
            self.__history.undo_last_operation()
        except:
            pass

    def __start_redo(self):
        """ Redo last action """
        try:
            self.__history.redo_last_operation()
        except:
            pass

    def __start_save(self):
        """ Save the Project """
        project = Project.get_instance()
        if project.path is None:
            self.__start_save_as()
            return

        self.__write_project_data(project.path)

    def __start_save_as(self):
        """ Lets the user select a file and saves the project in that file """
        # select file
        file_dialog = QFileDialog(self.__video_editor_view)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter('uc files (*.uc)')
        file_dialog.setDefaultSuffix('uc')
        if file_dialog.exec_() == QFileDialog.Accepted:
            filename = file_dialog.selectedFiles()[0]
        else:
            return

        self.__write_project_data(filename)

        project = Project.get_instance()
        project.path = filename

        Projectsettings.add_project(filename)

    def new_project(self, path):
        """
        Initially saves the project to the project file.

        :param path: String - Path to the projects file.
        """
        self.__write_project_data(path)
        project = Project.get_instance()
        project.path = path

        Projectsettings.add_project(path)

    def get_filemanager_controller(self):
        return self.__filemanager_controller

    def __write_project_data(self, filename):
        """ Saves project data into a file """
        # get timeline data
        timeline_data = self.__timeline_controller.get_project_timeline()

        # get filemanager data
        filemanager_data = self.__filemanager_controller.get_project_filemanager()

        project_data = {
            "timeline": timeline_data,
            "filemanager": filemanager_data,
            "projectsettings": Projectsettings.get_instance().get_dict_projectsettings()
        }

        # write data
        with open(filename, 'w') as f:
            json.dump(project_data, f, ensure_ascii=False)

        Project.get_instance().changed = False

    def __start_open(self):
        """ Open a project """
        filetypes = Settings.get_instance().get_dict_settings()[
            "Invisible"]["project_formats"]
        path, _ = QFileDialog.getOpenFileName(self.__video_editor_view,
                                              'Open Project', '', filetypes)

        # do nothing if cancel was clicked
        if path == "":
            return

        with open(path, 'r') as f:
            project_data = json.load(f)

        # set up timeline
        self.__timeline_controller.clear_timeline()

        if "timeline" in project_data:
            self.__timeline_controller.create_project_timeline(project_data["timeline"])
        else:
            self.__timeline_controller.create_default_tracks()

        # set up filemanager
        self.__filemanager_controller.clear()

        if "filemanager" in project_data:
            filemanager_data = project_data["filemanager"]
            self.__filemanager_controller.create_project_filemanager(filemanager_data)

        # set project path
        project = Project.get_instance()
        project.path = path
