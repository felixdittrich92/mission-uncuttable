from fbs_runtime.application_context import ApplicationContext
from controller import MainController
from view import StartView

from config import Resources
from config import Language
from config import Settings

import sys


class AppContext(ApplicationContext):

    def run(self):
        """Starts the application using 'MainController' with the 'StartView'."""
        # init resources
        Resources(self)
        # init language
        lang = Settings.get_instance().get_settings().General.language.current
        if lang == 0:
            Language('en')
        elif lang == 1:
            Language('de')
        else:
            Language()

        # start view and controller
        start_view = StartView()
        __main_controller = MainController(start_view)
        __main_controller.start()
        return self.app.exec_()


if __name__ == '__main__':
    app = AppContext()
    exit_code = app.run()
    sys.exit(exit_code)
