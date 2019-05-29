from .media_file import MediaFile
from itertools import count

import cv2
import openshot

class VisualiserVideo(MediaFile):
    """
    This class contains the video
    """

    def __init__(self, file_path): 
        self.file_path = file_path
        self.subvideos = list()


    def visualiser_area(self, clip_prefix):
        """
        a method that analyse the video frame per frame and save the Clips (Visualiser) in a list
        """
        video = cv2.VideoCapture(str(self.file_path))
        try:
            times = list()
            clip_numbers = count()

            for frame_number in count():
                is_ok, frame = video.read()

                if not is_ok:
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                roi = frame[275:405, 960:1000]
                average = cv2.mean(roi)

                if average[0] > 5:
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









