from .video_splitter import VideoSplitter

class Video():
    """
    This class contains the single file of the video
    """

    def __init__(self, file_path): 
        self.__file_path = file_path

    def get(self):
        return self.__file_path