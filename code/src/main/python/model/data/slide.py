from .presentation import Presentation

class Slide():
    """
    This class contains a list of the converted PDF file
    """

    def __init__(self, file_path): 
        self.__file_path = file_path

    def get(self):
        return self.__file_path