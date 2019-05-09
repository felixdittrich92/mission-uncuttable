files = {
    "startview": "ui/start_view.ui",
    "filemanager": "ui/filemanager.ui",
    "preview_view": "ui/form.ui",
    "mainview": "ui/main_window.ui",
    "settingsview": "ui/settings_window.ui",
    "projectsettings_view": "ui/projectsettings_window.ui",
    "export_view": "ui/export.ui",
    "timeline_scrollarea_view": "ui/timeline_scroll_area.ui",
    "timeline_view": "ui/timeline_view.ui"
}
images = {
    "play_button": "images/buttons/002-play-button.svg",
    "pause_button": "images/buttons/001-pause.svg",
    "first_frame_button": "images/buttons/006-back.svg",
    "last_frame_button": "images/buttons/007-next-1.svg",
    "back_button": "images/buttons/013-previous.svg",
    "media_symbols": "images/filemanagerIcons",
    "forward_button": "images/buttons/004-next.svg",
    "max_button": "images/buttons/maximize.svg"
}
strings = {
    "de": "strings/de/strings.xml",
    "en": "strings/en/strings.xml"
}


class Resources:
    """
    This class loads the paths of included files.
    This is necessary because the project has different paths after freezing and installing.
    """
    __instance = None

    def __init__(self, app):
        self.app = app
        if Resources.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Resources.__instance = self
            self.load_file_paths()

    @staticmethod
    def get_instance():
        if Resources.__instance is None:
            raise Exception("Resources not initialized!")
        else:
            return Resources.__instance

    def load_file_paths(self):
        self.files = Category()
        for attribute, value in files.items():
            setattr(self.files, attribute, self.app.get_resource(value))
        self.images = Category()
        for attribute, value in images.items():
            setattr(self.images, attribute, self.app.get_resource(value))

class Category:
    pass

