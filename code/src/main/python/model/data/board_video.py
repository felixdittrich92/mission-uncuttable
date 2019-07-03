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
        self.board_subvideos = list()
        self.speaker_subvideos = list()

    def get(self):
        return self.__file_path

    def check_board_area(self, update_progress):
        """
        a method that analyse the video frame per frame and save the Cliptimes (Board, Speaker) in a list

        @param update_progress: a function which handles the progressbar countprocess
        """
        video = cv2.VideoCapture(self.__file_path)
        maxframes = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        try:
            times = list()
            times_speaker = list()
            for frame_number in count():
                if frame_number % 30 == 0:
                    update_progress(frame_number/maxframes*100)
                is_ok, frame = video.read()

                if not is_ok:
                    if times:
                        self.board_subvideos.append((times[0], times[-1]))
                    if times_speaker:
                        self.speaker_subvideos.append((times_speaker[0], times_speaker[-1]))
                    break

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                (thresh, frame) = cv2.threshold(frame, 60, 255, cv2.THRESH_BINARY)
                average = cv2.mean(frame)

                if average[0] < 250:
                    times_speaker.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                elif times_speaker:
                    self.speaker_subvideos.append((times_speaker[0], times_speaker[-1]))
                    times_speaker.clear()
                else:
                    pass

                if average[0] > 250:
                    times.append(video.get(cv2.CAP_PROP_POS_MSEC) / 1000)
                elif times:
                    self.board_subvideos.append((times[0], times[-1]))
                    times.clear()
                else:
                    pass

        finally:
            video.release()



            