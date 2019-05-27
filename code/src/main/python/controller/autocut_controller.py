from PyQt5.QtWidgets import QFileDialog, QMessageBox
from model.splitter import VideoSplitter
from model.splitter import Presentation
from model.data import BoardVideo
from model.data import VisualiserVideo
from controller import VideoEditorController
from view import VideoEditorView
from view import StartView

from config import Settings

VISUALISER_ROI_SLICES = (slice(250, 600), slice(800, 1000))
BOARD_ROI_SLICES = (slice(140, 260), slice(150, 750))
RESOLUTION = 250
projekt_path = "/home/felix/Schreibtisch/"  #Pfad ändern wenn Projekt anlegen vorhanden
projekt_name = "Projekt"


class AutocutController:
    """A class used as the Controller for the autocut window."""

    def __init__(self, view, main_controller):
        self.__autocut_view = view
        self.__autocut_view.video_button.clicked.connect(self.pick_video)
        self.__autocut_view.pdf_button.clicked.connect(self.pick_pdf)
        self.__autocut_view.ok_button.clicked.connect(self.ready)
        self.__autocut_view.cancel_button.clicked.connect(self.stop)
        self.__main_controller = main_controller

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
            self.__autocut_view.change_icon(self.__autocut_view.pdf_image_label)
        else:
            pass

    def ready(self):
        """autocut the input files and start the video editor view"""
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
                video_splitter.audio_from_video_cut()
                video_splitter.small_video_cut()
                visualiser_video = video_splitter.large_video_cut()
                visualiser_video.area(VISUALISER_ROI_SLICES, "small_video")
                board_video = video_splitter.large_video_cut()
                board_video.area(BOARD_ROI_SLICES, "large_video")
        except:  
            #QDialog einfügen 
            return
            
        # View einfügen bis Bearbeitung abgeschlossen ist Ladebalken oder ähnliches

        self.__autocut_view.close()
        video_editor_view = VideoEditorView()
        self.__video_editor_controller = VideoEditorController(video_editor_view)
        self.__video_editor_controller.start()
