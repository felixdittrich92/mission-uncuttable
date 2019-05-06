from video_splitter import VideoSplitter
from media_file import MediaFile

class Video(MediaFile):
    """
    This class contains the single file of the video
    """

    def __init__(self, file_path): 
        super().__init__(self.path)
        self.__file_path = file_path

    def get(self):
        return self.__file_path