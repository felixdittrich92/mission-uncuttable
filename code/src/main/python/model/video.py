#import numpy
#import cv2


class Video:
    def __init__(self):
        pass

    def show_video(self, path, filename):

        cap = cv2.VideoCapture(file=path + filename)
        if (cap.isOpened() is False):
            print("Error opening video stream or file")

        while(cap.isOpened()):
            frame = cap.read()
            if cap.read() is True:
                cv2.imshow('Frame', frame)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()

        cv2.destroyAllWindows()
