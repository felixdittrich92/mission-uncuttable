import json
import os
import sys


class Settings:
    def __init__(self):
        file = os.path.join(sys.path[0], 'config/config.json')
        with open(file, 'r') as read_file:
            self.data = json.load(read_file)

    def get_settings(self):
        return self.data

    def get_setting(self, setting):
        pass
