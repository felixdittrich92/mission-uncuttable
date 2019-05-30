files = {
    "startview": "ui/start_view.ui",
    "filemanager": "ui/filemanager.ui",
    "preview_view": "ui/form.ui",
    "mainview": "ui/main_window.ui",
    "settingsview": "ui/settings_window.ui",
    "projectsettings_view": "ui/projectsettings_window.ui",
    "export_view": "ui/export.ui",
    "timeline_scrollarea_view": "ui/timeline_scroll_area.ui",
    "timeline_view": "ui/timeline_view.ui",
    "decision_widget": "ui/new_project_decision.ui",
    "select_project_widget": "ui/select_project.ui",
    "qss_dark": "stylesheets/dark.qss",
    "qss_light": "stylesheets/light.qss"
}
images = {
    "play_button": "images/buttons/play.png",
    "pause_button": "images/buttons/pause.png",
    "first_frame_button": "images/buttons/fast_backwards.png",
    "last_frame_button": "images/buttons/fast_forward.png",
    "back_button": "images/buttons/step_back.png",
    "forward_button": "images/buttons/step_forward.png",
    "maximize_button": "images/buttons/maximize.png",
    "media_symbols": "images/filemanagerIcons",
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
    __app = None

    def __init__(self, app):
        Resources.__app = app
        if Resources.__instance is not None:
            raise Exception("Resources already initialized!")
        else:
            Resources.__instance = self
            Resources.__load_file_paths()

    def __load_file_paths():
        Resources.files = Category()
        for attribute, value in files.items():
            setattr(Resources.files, attribute, Resources.__app.get_resource(value))
        Resources.images = Category()
        for attribute, value in images.items():
            setattr(Resources.images, attribute, Resources.__app.get_resource(value))
        Resources.strings = Category()
        for attribute, value in strings.items():
            setattr(Resources.strings, attribute, Resources.__app.get_resource(value))

class Category:
    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

