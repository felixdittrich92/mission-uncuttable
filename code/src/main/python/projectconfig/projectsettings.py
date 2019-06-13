import json
import os
import platform

import projectconfig
import config

from collections import namedtuple


class Projectsettings:
    """
    A Class, using the singleton pattern, that loads the projectsettings file

    By default the projectconfig.py is loaded. When a 'projectconfig.uc' exists, the
    settings saved in 'projectconfig.uc' override those, the 'projectconfig.py'
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
        if Projectsettings.__instance is None:
            Projectsettings()
        return Projectsettings.__instance

    def __init__(self):
        """
        Virtually private constructor.

        Loads the settings file (projectconfig.py) for default settings and saved projectsettings.
        If 'projectconfig.uc" contains values that are
        different from the values in 'projectconfig.py', this values will be
        overwritten.
        Then the JSON gets converted into an object, where the settings can
        be accessed via dot-notation.
        """

        if Projectsettings.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Projectsettings.__instance = self
            home = os.path.expanduser('~')
            project_config = os.path.join(home, '.config', 'ubicut', 'projectconfig.uc')
            if os.path.exists(project_config):
                with open(project_config, 'r') as read_file:
                    self.project_config_data = json.load(read_file)
                    projectconfig.default_settings.update(self.project_config_data)
                    self.parsed_data = projectconfig.default_settings

            else:
                self.parsed_data = projectconfig.default_settings

            self.parsed_json = json.dumps(self.parsed_data, ensure_ascii=False)

            self.dict = json.loads(self.parsed_json)

            self.settings = json.loads(
                self.parsed_json,
                object_hook=lambda d: namedtuple('X', d.keys())(*d.values())
            )

    def get_settings(self):
        """
        Getter that returns all settings as an object.

        @return: object of settings
        """
        return self.projectsettings

    def get_dict_projectsettings(self):
        """
        Getter that returns all settings as a dictionary.

        @return:  dictionary with all settings
        """
        return self.dict

    @staticmethod

    def get_config_dir():
        """ Returns the directory where the config will be saved """
        home = os.path.expanduser('~')
        config_location = ""
        if platform.system() == 'Linux':
            config_location = os.path.join(home, '.config', 'ubicut')
        elif platform.system() == 'Windows':
            config_location = os.path.join(home, 'AppData', 'Roaming', 'ubicut')

        return config_location

    @staticmethod
    def save_settings(new_projectsettings):
        """
        Method that saves the custom user settings to a file.

        Depending on the platform, the program is running on, a directory,
        containing the json file is created.

        @type   new_projectsettings: Dictionary
        @param  new_projectsettings: Settings to be saved
        """
        location = Projectsettings.get_config_dir()

        if not os.path.exists(location):
            os.makedirs(location)

        file = os.path.join(location, 'projectconfig.uc')

        with open(file, 'w') as outfile:        # writes json to file
            json.dump(new_projectsettings, outfile, ensure_ascii=False)

    @staticmethod
    def get_projects():
        """ Returns a list a known projects """
        location = Projectsettings.get_config_dir()
        project_file = os.path.join(location, 'projects')

        if not os.path.isfile(project_file):
            return []

        res = []
        with open(project_file, 'r') as f:
            for file in f.read().splitlines():
                if os.path.isfile(file):
                    res.append(file)

        return res

    @staticmethod
    def add_project(filename):
        """ Adds a project to the projects file """
        location = Projectsettings.get_config_dir()
        project_file = os.path.join(location, 'projects')
        if not os.path.isfile(project_file):
            with open(project_file, 'w') as f:
                f.write(filename + '\n')
        else:
            with open(project_file, 'a') as f:
                f.write(filename + '\n')
