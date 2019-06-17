
class Settings:
    

    def __init__(self):
        self.settings = None
        self.dict = None

    def get_settings(self):
        """
        Getter that returns all settings as an object.

        @return: object of settings
        """
        return self.settings

    def get_dict_settings(self):
        """
        Getter that returns all settings as a dictionary.

        @return:  dictionary with all settings
        """
        return self.dict
