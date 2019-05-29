from .media_file import MediaFile
from itertools import count

import cv2
# import openshot


class VisualiserVideo(MediaFile):
    """
    This class contains the video
    """

    def __init__(self, file_path):
        self.file_path = str(file_path)
        self.subvideos = list()

    def visualiser_area(self, clip_prefix):
        """
        a method that analyse the video frame per frame and save the Clips (Visualiser) in a list
        """
        video = cv2.VideoCapture(self.file_path)
        try:
            times = list()

            for frame_number in count():
                is_ok, frame = video.read()

                if not is_ok:
                    if times:
                        self.subvideos.append((times[0], times[-1]))
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                roi = frame[275:405, 960:1000]
                average = cv2.mean(roi)

                if average[0] > 5:
                    times.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                elif times:
                    self.subvideos.append((times[0], times[-1]))
                    times.clear()

        finally:
            video.release()
            cv2.destroyAllWindows()
