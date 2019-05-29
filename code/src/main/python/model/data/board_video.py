from .media_file import MediaFile
from itertools import count

import cv2
import openshot

class BoardVideo(MediaFile):
    """
    This class contains the video and analyse the areas for autocut
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.subvideos = list()


    def board_area(self, clip_prefix):
        """
        a method that analyse the video frame per frame and save the Clips (Board) in a list
        """
        video = cv2.VideoCapture(str(self.file_path))
        try:
            times = list()
            clip_numbers = count()

            for frame_number in count():
                is_ok, frame = video.read()

                if not is_ok:
                    break

                average = cv2.mean(frame)
                sum = average[0] + average[1] + average[2]
                percentage_green = (100 * average[1]) / sum

                if percentage_green > 40:
                    times.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                else:
                    if times:
                        clip = openshot.Clip(
                                '{}{}'.format(clip_prefix, next(clip_numbers))
                            )
                        clip.Start(times[0])
                        clip.End(times[-1])
                        self.subvideos.append(clip)
                        times.clear()

        finally:
            video.release()
            cv2.destroyAllWindows()


