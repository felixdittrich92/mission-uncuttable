import os

from .history import History


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

    def get_history(self):
        return self.__history

    def get_project_name(self):
        name = ""
        if self.path is not None:
            name = os.path.splitext(os.path.basename(self.path))[0]

        return name
