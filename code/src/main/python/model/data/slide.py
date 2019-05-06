from .presentation import Presentation

class Slide():
    """
    This class contains a list of the converted PDF file
    """

    def __init__(self, files): 
        self.__files = files

    def get(self):
        return self.__files