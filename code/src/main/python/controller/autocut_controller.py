import os

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from model.splitter import VideoSplitter
from model.splitter import Presentation
from controller import VideoEditorController
from view import VideoEditorView

from config import Settings

VISUALISER_ROI_SLICES = (slice(250, 600), slice(800, 1000))
BOARD_ROI_SLICES = (slice(140, 260), slice(150, 750))


class AutocutController:
    """A class used as the Controller for the autocut window."""

    def __init__(self, view, main_controller):
        self.__autocut_view = view
        self.__autocut_view.video_button.clicked.connect(self.pick_video)
        self.__autocut_view.pdf_button.clicked.connect(self.pick_pdf)
        self.__autocut_view.ok_button.clicked.connect(self.ready)
        self.__autocut_view.cancel_button.clicked.connect(self.stop)
        self.__main_controller = main_controller

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
        supported_filetypes = Settings.get_instance().get_dict_settings()["AutoCutVideo"]["import_formats"]
        self.filename_video, _ = QFileDialog.getOpenFileName(
            self.__autocut_view,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )
        if self.filename_video:
            self.__autocut_view.change_icon(self.__autocut_view.video_image_label)

    def pick_pdf(self):
        """Opens a file picker to select a pdf."""
        supported_filetypes = Settings.get_instance().get_dict_settings()["AutoCutPDF"]["import_formats"]
        self.filename_pdf, _ = QFileDialog.getOpenFileName(
            self.__autocut_view,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )
        if self.filename_pdf:
            self.__autocut_view.change_icon(self.__autocut_view.pdf_image_label)
        else:
            pass

    def ready(self):
        """autocut the input files and start the video editor view"""
        if self.filename_pdf is not None:
            presentation = Presentation(self.filename_pdf)
            presentation.convert_pdf(os.path.join(os.path.expanduser("~"),
                                                  "Schreibtisch"), "Projekt", 250)

        if self.filename_video is not None:
            video_splitter = VideoSplitter(
                os.path.join(os.path.expanduser("~"), "Schreibtisch"),
                "Projekt", self.filename_video)
            video_splitter.audio_from_video()
            video_splitter.small_video()
            visualiser_video = video_splitter.large_video()
            visualiser_video.area(VISUALISER_ROI_SLICES, "v_video")
            board_video = video_splitter.large_video()
            board_video.area(BOARD_ROI_SLICES, "b_video")

        else:
            #QDialog einfügen
            return

        # View einfügen bis Bearbeitung abgeschlossen ist Ladebalken oder ähnliches

        self.__autocut_view.close()
        video_editor_view = VideoEditorView()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()
