from presentation import Presentation
from media_file import MediaFile

class Slide(MediaFile):
    """
    This class contains a list of the converted PDF file
    """

    def __init__(self, file_path): 
        super().__init__(path)
        self.__file_path = file_path

    def get(self):
        return self.__file_path