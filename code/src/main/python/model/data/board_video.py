from .media_file import MediaFile
from itertools import count

import cv2
# import openshot


class BoardVideo(MediaFile):
    """
    This class contains the video and analyse the areas for autocut
    """

    def __init__(self, file_path):
        self.file_path = str(file_path)
        self.background = None
        self.accumulate_weight = 0.5
        self.subvideos = list()

    def board_area(self, clip_prefix):
        """
        a method that analyse the video frame per frame and save the Clips (Board) in a list
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

                average = cv2.mean(frame)
                sum = average[0] + average[1] + average[2]
                percentage_green = (100 * average[1]) / sum

                if percentage_green > 40:
                    times.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                elif times:
                    self.subvideos.append((times[0], times[-1]))
                    times.clear()
        finally:
            video.release()
            cv2.destroyAllWindows()
