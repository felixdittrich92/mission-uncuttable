import os

from .history import History
from projectconfig.projectsettings import Projectsettings


# Todo: Link the project and its settings together.
#  Normally you would expect that a Project knows its own settings. For
#  example, if you want to know the framerate of a project, wouldn't
#  your first thought be to look it up in the project itself? It would
#  be uncomfortable to have some dictionary lying around which you can
#  find the settings in for each project, instead.
class Project:
    __instance = None

    @staticmethod
    def get_instance():
        """
        Static access method.

        If no instance exists yet, one will be created.

        @return: the instance of this class, if it exists
        """
        if Project.__instance is None:
            Project()
        return Project.__instance

    def __init__(self):
        if Project.__instance is not None:
            raise Exception("This class is a singleton!")

        Project.__instance = self

        self.path = None
        self.changed = False
        self.__history = History()
        # This field is only here for convenience and quick progress.
        #  Actually the project settings have to be linked to this class
        #  and then this field can be removed.
        self.__framerate = 30

    def get_history(self):
        return self.__history

    def get_project_name(self):
        name = ""
        if self.path is not None:
            name = os.path.splitext(os.path.basename(self.path))[0]

        return name

    def get_framerate(self):
        return self.__framerate
