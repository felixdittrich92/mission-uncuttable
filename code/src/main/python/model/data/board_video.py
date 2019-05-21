from .media_file import MediaFile
import openshot

class BoardVideo(MediaFile):
    """
    This class contains the video
    """

    def __init__(self, file_path): 
        self.__file_path = file_path
        self.background = None
        self.accumulated_weight = 0.5
        self.visualiser_time = []
        self.blackboard_time = []
        self.subvideos = []

        self.roi_visualiser_top = 250
        self.roi_visualiser_bottom = 600
        self.roi_visualiser_right = 800 
        self.roi_visualiser_left = 1000

        self.roi_board_top = 260 
        self.roi_board_bottom = 140
        self.roi_board_right = 150
        self.roi_board_left = 750

    def get(self):
        return self.__file_path
    
    def calc_accum_avg(self, frame, accumulated_weight):

        global background

        if background is None:
            background = frame.copy().astype("float")
            return None
        
        cv2.accumulateWeighted(frame, background, self.accumulated_weight)

    def segment(self, frame, threshold=50):

        global background

        diff = cv2.absdiff(background.astype("uint8"),frame)

        _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return None
        
        else:
            move_segment = max(contours, key = cv2.contourArea)

            return (thresholded, move_segment)

    def visualiser_area(self): 
        video = cv2.VideoCapture("/home/felix/Schreibtisch/OpenCVPython/large_video.mp4")
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        num_frames = 0

        fgbg = cv2.createBackgroundSubtractorMOG2()

        while True:
            ret,frame = video.read()

            if frame is None:
                return

            roi_visualiser = frame[self.roi_visualiser_top:self.roi_visualiser_bottom,self.roi_visualiser_right:self.roi_visualiser_left]
            fgmask = fgbg.apply(roi_visualiser)
            gray = cv2.cvtColor(roi_visualiser, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (9,9), 0)
            #gray = cv2.Canny(gray, 300, 550, 3)
            if num_frames < 1:
                self.calc_accum_avg(gray, self.accumulated_weight)

            else:
                visualiser = self.segment(gray)
                if visualiser is not None:  
                    thresholded, move_segment = visualiser
                    milli = video.get(cv2.CAP_PROP_POS_MSEC)
                    time = milli/1000
                    self.visualiser_time.append(time)
                elif visualiser is None:
                    if not visualiser_time:
                        pass
                    else:
                        number = 0
                        start = self.visualiser_time[0]
                        end = self.visualiser_time[-1]
                        clip = openshot.Clip(number)
                        clip.Start(start)
                        clip.End(end)
                        self.subvideos.append(clip)
                        self.visualiser_time.clear()
                        number += 1

            num_frames += 1

        video.release()
        cv2.destroyAllWindows()

    def board_area(self):
        video = cv2.VideoCapture("/home/felix/Schreibtisch/OpenCVPython/large_video.mp4")
        length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        #print(length)
        num_frames = 0

        fgbg = cv2.createBackgroundSubtractorMOG2()

        while True:
            ret,frame = video.read()

            if frame is None:
                return

            roi_board = frame[self.roi_board_top:self.roi_board_bottom,self.roi_board_right:self.roi_board_left]
            fgmask = fgbg.apply(roi_board)
            gray = cv2.cvtColor(roi_board, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (9,9), 0)

            if num_frames < 1:
                self.calc_accum_avg(gray, self.accumulated_weight)

            else:
                board = self.segment(gray)
                if board is not None:  
                    thresholded, move_segment = board
                    milli = video.get(cv2.CAP_PROP_POS_MSEC)
                    time = milli/1000
                    self.board_time.append(time)
                elif board is None:
                    if not board_time:
                        pass
                    else:
                        number = 0
                        start = self.board_time[0]
                        end = self.board_time[-1]
                        clip = openshot.Clip("a" + number)
                        clip.Start(start)
                        clip.End(end)
                        self.subvideos.append(clip)
                        self.board_time.clear()
                        number += 1

            num_frames += 1

        video.release()
        cv2.destroyAllWindows()

