from fbs_runtime.application_context import ApplicationContext
from controller import MainController
from view import StartView
from model import *

import sys


class AppContext(ApplicationContext):

    def run(self):
        """Starts the application using 'MainController' with the 'StartView'."""

        start = Presentation()                                      
        start.convert(r"C:\Users\felix\Desktop", "kickoff18.pdf")
            
        start_view = StartView()
        __main_controller = MainController(start_view)
        __main_controller.start()
        return self.app.exec_()


if __name__ == '__main__':
    app = AppContext()
    exit_code = app.run()
    sys.exit(exit_code)
