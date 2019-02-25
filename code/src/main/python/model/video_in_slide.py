import cv2
from slide import Slide

class videoInSlide:
    def __init__(self):
        pass

    def show_video(self, Slide):
        file = Slide
        
        image = cv2.imread(file,0)
        if image is None:
            print("Unable to open " + file)
            exit(-1)
        else:
            cv2.imshow("An example image", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()