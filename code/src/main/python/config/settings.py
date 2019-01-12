import json
import os
import sys


class Settings():
    """
    A Class, using the singleton pattern, that loads the settings file

    By default the config.json is loaded. When a 'userconfig.json' exists, the
    settings saved in 'userconfig.json' override those, the 'config.json'
    contains.
    """
    __instance = None

    @staticmethod
    def get_instance():
        """
        Static access method.

        If no instance exists yet, one will be created.

        @return: the instance of this class, if it exists
        """
        if Settings.__instance is None:
            Settings()
        return Settings.__instance

    def __init__(self):
        """ Virtually private constructor. """

        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self

            config = os.path.join(sys.path[0], 'config/config.json')

            with open(config, 'r') as read_file:
                self.parsed_data = json.load(read_file)



    def get_settings(self):
        return self.parsed_data

    def get_setting(self, wanted_setting):
        if wanted_setting in self.parsed_data:
            return self.parsed_data[wanted_setting]
