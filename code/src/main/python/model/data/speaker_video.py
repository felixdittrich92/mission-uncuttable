from .media_file import MediaFile

class SpeakerVideo(MediaFile):
    """
    This class contains the board video and a method to analyse the video
    """

    def __init__(self, file_path):
        self.__file_path = str(file_path)

    def get(self):
        return self.__file_path