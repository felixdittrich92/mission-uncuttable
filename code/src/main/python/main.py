from fbs_runtime.application_context import ApplicationContext
from controller import MainController
from view import StartView
from config import Resources
import os

import sys


class AppContext(ApplicationContext):

    def run(self):
        """Starts the application using 'MainController' with the 'StartView'."""

        #start = Presentation()
        #start.convert(r"C:\Users\felix\Desktop", "kickoff18.pdf")
        Resources(self)
        start_view = StartView()
        __main_controller = MainController(start_view)
        __main_controller.start()
        return self.app.exec_()


if __name__ == '__main__':
    app = AppContext()
    exit_code = app.run()
    sys.exit(exit_code)
