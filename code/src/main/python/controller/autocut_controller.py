class AutocutController:
    """A class used as the Controller for the autocut window."""
    def __init__(self, view):
        self.autocut_view = view
        self.autocut_view.show()

    def pickVideoFile(self):
        supported_filetypes = Settings.get_instance().get_dict_settings()["AutoCutVideo"]["import_formats"]
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )
    
    def pickPdfFile(self):
        supported_filetypes = Settings.get_instance().get_dict_settings()["AutoCutPDF"]["import_formats"]
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            'QFileDialog.getOpenFileNames()',
            '',
            (
                supported_filetypes
            )
        )

