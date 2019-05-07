class MediaFile:
    """
    This class is the upper class of audio, video and slide
    """

    def __init__(self, path):
        self.path = path

    def get(self):
        return self.path


