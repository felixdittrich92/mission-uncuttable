from PyQt5.QtWidgets import QFileDialog
from model.data import VideoSplitter
from model.data import Presentation
from model.data import BoardVideo
from model.data import VisualiserVideo

from config import Settings


class AutocutController:
    """A class used as the Controller for the autocut window."""
    def __init__(self, view):
        self.__autocut_view = view
        self.__autocut_view.video_button.clicked.connect(self.pick_video)
        self.__autocut_view.pdf_button.clicked.connect(self.pick_pdf)
        self.__autocut_view.ok_button.clicked.connect(self.ready)

    def start(self):
        """Calls '__show_view()' of AutocutController"""
        self.__autocut_view.show()

    def stop(self):
        """Closes the window."""
        self.__autocut_view.close()

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

    def ready(self):
        if self.filename_pdf is not None:
            presentation = Presentation(self.filename_pdf)
            presentation.convert_pdf("/home/felix/Schreibtisch/", "Projekt", 250)
        else:
            pass
        
        if self.filename_video is not None:
            video_splitter = VideoSplitter("/home/felix/Schreibtisch/", "Projekt",self.filename_video)
            video_splitter.audio_from_video()
            video_splitter.small_video()
            board_video = video_splitter.large_video()
            board_video.visualiser_area()
            boardvideo.board_area()
   
        else:
            #QDialog einfügen 
            return

