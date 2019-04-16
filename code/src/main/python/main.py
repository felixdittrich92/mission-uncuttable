from fbs_runtime.application_context import ApplicationContext
from controller import MainController
from view import StartView
<<<<<<< HEAD
=======
from config import Resources
import os
>>>>>>> 350a202b95370858fb67003ffb8e08515a66849c

import sys


class AppContext(ApplicationContext):

    def run(self):
        """Starts the application using 'MainController' with the 'StartView'."""
        Resources(self)
        start_view = StartView()
        __main_controller = MainController(start_view)
        __main_controller.start()
        return self.app.exec_()


if __name__ == '__main__':
    app = AppContext()
    exit_code = app.run()
    sys.exit(exit_code)
