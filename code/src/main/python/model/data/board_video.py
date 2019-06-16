from .media_file import MediaFile
from itertools import count

import cv2
# import openshot


class BoardVideo(MediaFile):
    """
    This class contains the board video and a method to analyse the video
    """

    def __init__(self, file_path):
        self.__file_path = str(file_path)
        self.subvideos = list()

    def get(self):
        return self.__file_path

    def check_board_area(self, progress):
        """
        a method that analyse the video frame per frame and save the Clips (Board) in a list
        """
        video = cv2.VideoCapture(self.__file_path)
        maxframes = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        try:
            times = list()
            for frame_number in count():
                if frame_number % 30 == 0:
                    progress(frame_number/maxframes*100)
                is_ok, frame = video.read()
                #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                if not is_ok:
                    if times:
                        self.subvideos.append((times[0], times[-1]))

                    break

                average = cv2.mean(frame)
                summe = average[0] + average[1] + average[2]
                percentage_red = (100 * average[0]) / summe
                #percentage_green = (100 * average[1]) / summe
                #percentage_blue = (100 * average[2]) / summe

                if percentage_red > 31:
                #if average[0] > 168:
                    times.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                elif times:
                    self.subvideos.append((times[0], times[-1]))
                    times.clear()
        finally:
            video.release()



            