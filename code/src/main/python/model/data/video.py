from .video_splitter import VideoSplitter

class Video():
    """
    This class contains the single file of the video
    """

    def __init__(self, new_large_video_path): 
        self.__new_large_video = new_large_video_path

    #def __init__(self, new_small_video_path): 
     #   self.__new_small_video = new_small_video_path

    def get(self):
        return self.__new_large_video