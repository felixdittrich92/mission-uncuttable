import json
import os
import platform

import config

from collections import namedtuple


class Settings:
    """
    A Class, using the singleton pattern, that loads the settings file

    By default the config.py is loaded. When a 'userconfig.json' exists, the
    settings saved in 'userconfig.json' override those, the 'config.py'
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
        """
        Virtually private constructor.

        Loads the settings file (config.py) for default settings and the users
        custom settings. If 'userconfig.json" contains values that are
        different from the values in 'config.py', this values will be
        overwritten.
        Then the JSON gets converted into an object, where the settings can
        be accessed via dot-notation.
        """

        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self
            home = os.path.expanduser('~')
            user_config = os.path.join(home, '.config', 'ubicut', 'userconfig.json')
            if os.path.exists(user_config):
                with open(user_config, 'r') as read_file:
                    self.user_config_data = json.load(read_file)
                    config.default_settings.update(self.user_config_data)
                    self.parsed_data = config.default_settings

            else:
                self.parsed_data = config.default_settings

            self.parsed_json = json.dumps(self.parsed_data, ensure_ascii=False)

            self.settings = json.loads(
                self.parsed_json,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values())
            )

    def get_settings(self):
        """
        Getter that returns all settings as an object.

        @return: object of settings
        """
        return self.settings

    @staticmethod
    def save_settings(new_settings):
        """
        Method that saves the custom user settings to a file.

        Depending on the platform, the program is running on, a directory,
        containing the json file is created.

        @type   new_settings: Dictionary
        @param  new_settings: Settings to be saved
        """
        home = os.path.expanduser('~')
        location = ""
        if platform.system() == 'Linux':
            location = os.path.join(home, '.config', 'ubicut')
        elif platform.system() == 'Windows':
            location = os.path.join(home, 'AppData', 'Roaming', 'ubicut')

        if not os.path.exists(location):
            os.makedirs(location)

        file = os.path.join(location, 'userconfig.json')

        with open(file, 'w') as outfile:        # writes json to file
            json.dump(new_settings, outfile, ensure_ascii=False)
