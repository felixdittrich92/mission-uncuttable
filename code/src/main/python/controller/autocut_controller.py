import cv2

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from model.splitter import VideoSplitter
from model.splitter import Presentation
from controller import VideoEditorController, TimelineController
from view import VideoEditorView
from random import randint
from config import Settings

VISUALISER_ROI_SLICES = (slice(250, 600), slice(800, 1000))
BOARD_ROI_SLICES = (slice(140, 260), slice(150, 750))
RESOLUTION = 250
projekt_path = "/home/clemens/Schreibtisch/"  # Pfad ändern wenn Projekt anlegen vorhanden
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
        self.textlabel.setText("Working...")
        self.video_button.setEnabled(False)
        self.pdf_button.setEnabled(False)
        self.ok_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        try:
            if self.filename_pdf is not None:
                presentation = Presentation(self.filename_pdf)
                presentation.convert_pdf(projekt_path, projekt_name, RESOLUTION)
        except:
            pass

        try:
            if self.filename_video is not None:
                # get fps
                video = cv2.VideoCapture(self.filename_video)
                fps = video.get(cv2.CAP_PROP_FPS)

                video_splitter = VideoSplitter(projekt_path,
                                               projekt_name, self.filename_video)
                self.progressbar.setValue(randint(15, 32))
                video_splitter.audio_from_video_cut()
                video_splitter.small_video_cut(fps)
                self.progressbar.setValue(randint(37, 53))
                video = video_splitter.large_video_cut(fps)
                self.progressbar.setValue(randint(60, 70))
                video.area(VISUALISER_ROI_SLICES, "small_video")
                video2 = video_splitter.large_video_cut(fps)
                self.progressbar.setValue(randint(80, 90))
                video2.area(BOARD_ROI_SLICES, "large_video")
        except:
            return

        self.progressbar.setValue(100)

        video_editor_view = VideoEditorView()
        timeline_controller = TimelineController.get_instance()
        timeline_controller.create_autocut_tracks()
        filemanager = video_editor_view.filemanager
        filemanager.addFileNames(self.filename_video)

        for c in video.subvideos:
            timeline_controller.create_timeable_from_clip(c)

        for c in video2.subvideos:
            timeline_controller.create_timeable_from_clip(c)

        self.__autocut_view.close()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()
