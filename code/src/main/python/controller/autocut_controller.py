import os
import cv2

from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import Qt
from model.splitter import VideoSplitter
from model.splitter import Presentation
from controller import VideoEditorController, TimelineController
from view import VideoEditorView
from random import randint
from config import Settings

RESOLUTION = 250
projekt_path = os.path.join(os.path.expanduser("~"), "Schreibtisch")
projekt_name = "Projekt"


class AutocutController:
    """A class used as the Controller for the autocut window."""

    def __init__(self, view, main_controller):
        self.__autocut_view = view
        self.video_button = self.__autocut_view.video_button
        self.video_button.clicked.connect(self.pick_video)
        self.pdf_button = self.__autocut_view.pdf_button
        self.pdf_button.clicked.connect(self.pick_pdf)
        self.ok_button = self.__autocut_view.ok_button
        self.ok_button.clicked.connect(self.ready)
        self.cancel_button = self.__autocut_view.cancel_button
        self.cancel_button.clicked.connect(self.stop)
        self.__main_controller = main_controller
        self.textlabel = self.__autocut_view.text_label
        self.textlabel.setText("Please choose a video and optionally a pdf")
        self.textlabel.setAlignment(Qt.AlignCenter)
        self.textlabel.setWordWrap(True)
        self.progressbar = self.__autocut_view.progress_bar
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)

        self.filename_video = None
        self.filename_pdf = None

    def start(self):
        """Calls '__show_view()' of AutocutController"""
        self.__autocut_view.show()

    def stop(self):
        """Closes the window."""
        self.__autocut_view.close()
        self.__main_controller.start()

    def pick_video(self):
        """Opens a file picker to select a video file."""
        supported_filetypes = Settings.get_instance().get_dict_settings()[
            "Invisible"]["autocutvideo_import_formats"]
        self.filename_video, _ = QFileDialog.getOpenFileName(
            self.__autocut_view,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )
        if self.filename_video:
            self.textlabel.setText("Ready to continue")
            self.__autocut_view.change_icon(self.__autocut_view.video_image_label)

    def pick_pdf(self):
        """Opens a file picker to select a pdf."""
        supported_filetypes = Settings.get_instance().get_dict_settings()[
            "Invisible"]["autocutpdf_import_formats"]
        self.filename_pdf, _ = QFileDialog.getOpenFileName(
            self.__autocut_view,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )
        if self.filename_pdf:
            self.textlabel.setText("Please add a video file to continue")
            self.__autocut_view.change_icon(self.__autocut_view.pdf_image_label)
        else:
            pass

    def ready(self):
        """autocut the input files and start the video editor view"""
        self.progressbar.setValue(0)
        QApplication.processEvents()
        self.textlabel.setText("Working...")
        self.video_button.setEnabled(False)
        self.pdf_button.setEnabled(False)
        self.ok_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        QApplication.processEvents()
        try:
            if self.filename_pdf is not None:
                presentation = Presentation(self.filename_pdf)
                self.pictures = presentation.convert_pdf(projekt_path, projekt_name, RESOLUTION)
        except:
            pass

        try:
            if self.filename_video is not None:
                video = cv2.VideoCapture(self.filename_video)
                fps = video.get(cv2.CAP_PROP_FPS)

                video_splitter = VideoSplitter(projekt_path,
                                               projekt_name, self.filename_video)
                self.progressbar.setValue(randint(15, 26))
                QApplication.processEvents()
                audio = video_splitter.audio_from_video_cut()
                self.progressbar.setValue(randint(29, 34))
                QApplication.processEvents()
                foil_video = video_splitter.foil_video_cut(fps)
                self.progressbar.setValue(randint(37, 53))
                QApplication.processEvents()

                board_video = video_splitter.large_video_cut(fps)
                board_video.board_area()
                self.progressbar.setValue(randint(60, 70))
                QApplication.processEvents()
                visualiser_video = video_splitter.visualiser_video_cut(fps)
                visualiser_video.visualiser_area()

                self.progressbar.setValue(randint(80, 90))
                QApplication.processEvents()

        except:
            return

        self.progressbar.setValue(100)
        QApplication.processEvents()

        video_editor_view = VideoEditorView()
        timeline_controller = TimelineController.get_instance()
        timeline_controller.create_autocut_tracks()

        filemanager = video_editor_view.filemanager
        filemanager.addFileNames(self.filename_video)
        filemanager.addFileNames(board_video.get())
        filemanager.addFileNames(visualiser_video.get())
        filemanager.addFileNames(foil_video.get())
        filemanager.addFileNames(audio.get())
        for count in range(0, len(self.pictures)):
            filemanager.addFileNames(self.pictures[count])

        timeline_controller.create_autocut_timeables(board_video.get(), 2,
                                                     board_video.subvideos)
        timeline_controller.create_autocut_timeables(visualiser_video.get(), 1,
                                                     visualiser_video.subvideos)
        timeline_controller.add_clip(foil_video.get(), 0)

        self.__autocut_view.close()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()
