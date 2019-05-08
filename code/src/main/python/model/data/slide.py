from .media_file import MediaFile
import numpy as np
import cv2

class Slide(MediaFile):
    """
    This class contains a list of the converted PDF file
    """

    def __init__(self, file_path): 
        self.__file_path = file_path
        self.__is_free = False
        self.list_is_free = []

    def get(self):
        return self.__file_path

    def check_color(self):
        """
        a method which checks if the place for a video is free to show it 

        @return: True if region of interest is completly white or gray
        """
        input_file = self.__file_path
        picture = cv2.imread(str(input_file))
        height = picture.shape[0]
        width = picture.shape[1]
        # upper y point
        y1 = int((73.8 * height) / 100)
        # lower y point
        y2 = int((94.7 * height) / 100)
        # left x point
        x1 = int((79.3 * width) / 100)
        # right x point
        x2 = int(width)
        white = 255
        gray = 32
        img = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)
        roi = img[y1:y2, x1:x2]

        if np.all(roi == white) == True:
            self.list_is_free.append(True)
            return True
        elif np.all(roi == gray) == True:
            self.list_is_free.append(True)
            return True
        else:
            self.list_is_free.append(False)
            return False
