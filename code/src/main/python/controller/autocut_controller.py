import time

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from model.splitter import VideoSplitter
from model.splitter import Presentation
from model.data import BoardVideo
from model.data import VisualiserVideo
from controller import VideoEditorController
from view import VideoEditorView
from view import StartView
from random import *

from config import Settings

VISUALISER_ROI_SLICES = (slice(250, 600), slice(800, 1000))
BOARD_ROI_SLICES = (slice(140, 260), slice(150, 750))
RESOLUTION = 250
projekt_path = "/home/felix/Schreibtisch/"  #Pfad ändern wenn Projekt anlegen vorhanden
projekt_name = "Projekt"
fps = Settings.get_instance().get_dict_settings()["Invisible"]["frames_per_second"]


class AutocutController:
    """A class used as the Controller for the autocut window."""

    def __init__(self, view, main_controller):
        self.__autocut_view = view
        self.__autocut_view.video_button.clicked.connect(self.pick_video)
        self.__autocut_view.pdf_button.clicked.connect(self.pick_pdf)
        self.__autocut_view.ok_button.clicked.connect(self.ready)
        self.__autocut_view.cancel_button.clicked.connect(self.stop)
        self.__main_controller = main_controller
        self.textlabel = self.__autocut_view.text_label
        self.textlabel.setText("Please add a video and a pdf to continue or choice only a video")
        self.textlabel.setAlignment(Qt.AlignCenter)
        self.textlabel.setWordWrap(True)
        self.progressbar = self.__autocut_view.progress_bar
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(100)

    def start(self):
        """Calls '__show_view()' of AutocutController"""
        self.__autocut_view.show()

    def stop(self):
        """Closes the window."""
        self.__autocut_view.close()
        self.__main_controller.start()

    def pick_video(self):
        """Opens a file picker to select a video file."""
        supported_filetypes = Settings.get_instance().get_dict_settings()["Invisible"]["autocutvideo_import_formats"]
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
        supported_filetypes = Settings.get_instance().get_dict_settings()["Invisible"]["autocutpdf_import_formats"]
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
        self.__autocut_view.video_button.setEnabled(False)
        self.__autocut_view.pdf_button.clicked.setEnabled(False)
        self.__autocut_view.ok_button.clicked.setEnabled(False)
        try:
            if self.filename_pdf is not None:
                presentation = Presentation(self.filename_pdf)
                presentation.convert_pdf(projekt_path, projekt_name, RESOLUTION)
            else:
                pass 
        except:
            pass

        try:
            if self.filename_video is not None:
                video_splitter = VideoSplitter(projekt_path, projekt_name,self.filename_video) 
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
                time.sleep(2)
        except:  
            return
            
        self.progressbar.setValue(100)
        self.__autocut_view.close()
        video_editor_view = VideoEditorView()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()
