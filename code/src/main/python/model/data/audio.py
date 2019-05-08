#from .video_splitter import VideoSplitter

class Audio():
    """
    This class contains the audiotrack of the video
    """

    def __init__(self, file_path): 
        self.__file_path = file_path

    def get(self):
        return self.__file_path