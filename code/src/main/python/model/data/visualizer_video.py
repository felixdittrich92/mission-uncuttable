from .media_file import MediaFile
from itertools import count

import cv2


class VisualizerVideo(MediaFile):
    """
    This class contains the visualizer video
    """

    def __init__(self, file_path):
        self.__file_path = str(file_path)
        self.visualizer_subvideos = list()

    def get(self):
        return self.__file_path

    def check_visualiser_area(self, update_progress):
        """
        a method that analyse the video frame per frame and save the Clips (Visualiser) in a list

        @param update_progress: a function which handles the progressbar countprocess
        """
        video = cv2.VideoCapture(self.__file_path)
        maxframes = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        try:
            times = list()

            for frame_number in count():
                is_ok, frame = video.read()

                if frame_number % 30 == 0:
                    update_progress(frame_number/maxframes*100)
                if not is_ok:
                    if times:
                        self.visualizer_subvideos.append((times[0], times[-1]))
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

                roi = frame[0:40, 0:40]
                average = cv2.mean(roi)

                if average[0] > 15:
                    times.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                elif times:
                    self.visualizer_subvideos.append((times[0], times[-1]))
                    times.clear()

        finally:
            video.release()
            