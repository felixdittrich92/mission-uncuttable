import json
import os
import sys


class Settings:
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
        """
        Virtually private constructor.

        Loads the settings file for default settings and the users custom
        settings. If 'userconfig.json" contains values that are different from
        the values in 'config.json', this values will be overwritten.
        """

        if Settings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self

            config = os.path.join(sys.path[0], 'config/config.json')
            userconfig = os.path.join(sys.path[0], 'config/userconfig.json')

            with open(config, 'r') as read_file:
                self.default_data = json.load(read_file)

            if os.path.exists(userconfig):
                with open(userconfig, 'r') as read_file:
                    self.userconfig_data = json.load(read_file)
                    self.default_data.update(self.userconfig_data)
                    self.parsed_data = self.default_data
            else:
                self.parsed_data = self.default_data

    def get_settings(self):
        """
        Getter that returns all settings as a dictionary.

        @return: dictionary of settings
        """
        return self.parsed_data

    def get_setting(self, wanted_setting):
        """
        Method that returns a specific value for a setting. There are two
        levels of settings. Level-one-settings are those, that have a single
        value assigned to them. Level-two-settings are objects in JSON with
        their own list of settings.

        @param wanted_setting: The setting, the value should be returned.
        @return: the wanted settings value as a string
        """
        if "#" in wanted_setting:
            wanted_level_one, wanted_level_two = wanted_setting.split('#')
            level_two_settings = self.parsed_data[wanted_level_one]
            return level_two_settings[wanted_level_two]
        elif wanted_setting in self.parsed_data:
            return self.parsed_data[wanted_setting]
