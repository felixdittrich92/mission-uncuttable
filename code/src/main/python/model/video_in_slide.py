import numpy
import cv2
from slide import Slide
from video import Video


class VideoInSlide:
    def __init__(self):
        pass

    def video_place(self, Slide):
        file = Slide

        image = cv2.imread(file, 0)
        """#gibt die pixel / xyz - koordinaten des gesamten Bildes aus"""
        print(image.shape)
        if image is None:
            print("Unable to open " + file)
            exit(-1)
        elif image.shape == [x, y, z]:
            pass

        else:
            cv2.imshow("An example image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
