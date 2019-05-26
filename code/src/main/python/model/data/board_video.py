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
        self.background = None
        self.accumulate_weight = 0.5
        self.subvideos = list()

    def calculate_accumulated_average(self, frame):
        """
        a method that manage the background for the frame difference
        """
        if self.background is None:
            self.background = frame.copy().astype('float')
        else:
            cv2.accumulateWeighted(
                frame, self.background, self.accumulate_weight
            )

    def segment(self, frame, threshold=50):
        """
        a method that found a movement

        @return: if no movement None else the thresholded frame and the contours
        """

        diff = cv2.absdiff(self.background.astype('uint8'), frame)
        _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        contours, _hierarchy = cv2.findContours(
            thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if len(contours) == 0:
            return None
        else:
            return (thresholded, max(contours, key=cv2.contourArea))

    def area(self, roi_slices, clip_prefix):
        """
        a method that analyse the video frame per frame and save the Clips(visualiser/board) in a list
        """
        video = cv2.VideoCapture(str(self.file_path))
        try:
            background_subtractor = cv2.createBackgroundSubtractorMOG2()
            times = list()
            clip_numbers = count()
            for frame_number in count():
                is_ok, frame = video.read()
                if not is_ok:
                    break

                roi = frame[roi_slices]
                gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (9, 9), 0)
                foreground_mask = background_subtractor.apply(roi)

                if frame_number == 0:
                    self.calculate_accumulated_average(gray)
                else:
                    if self.segment(gray): #if not self.segment(gray):
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
                            #print(self.subvideos)
        finally:
            video.release()
            cv2.destroyAllWindows()
