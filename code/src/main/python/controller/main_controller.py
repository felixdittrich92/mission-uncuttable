import os
import json

from PyQt5.QtWidgets import QWidget

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
        manual_cut_button.clicked.connect(self.__start_main_controller)

        auto_cut_button = self.__start_view.findChild(QWidget, "auto_cut_button")
        auto_cut_button.clicked.connect(self.__start_autocut_controller)

        load_project_button = self.__start_view.findChild(QWidget, "load_project_button")
        load_project_button.setText(str(Language.current.startview.load_project))
        load_project_button.clicked.connect(self.__load_project)

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

    def __start_main_controller(self):
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
                filemanager = video_editor_view.filemanager
                filemanager.create_project_filemanager(project_data["filemanager"])

            # set project path
            project = Project.get_instance()
            project.path = path

            # show videoeditor
            self.__start_view.close()
            self.__video_editor_controller = VideoEditorController(video_editor_view)
            self.__video_editor_controller.start()

        # TODO show error window if path does not exist
