import os
import cv2
from pathlib import Path
from moviepy.editor import AudioFileClip
from model.data import VisualizerVideo, BoardVideo, Audio, SlideVideo


class VideoSplitter:
    """
    This class handles the video and audio splitting
    """

    def __init__(self, folder_path, folder_name, video_data):
        """
        Constructor of the class

        @param folder_path: the path to the project folder
        @param folder_name: the name of the project folder
        @param video_data: the path of the video file
        """

        self.folder_path = folder_path
        self.folder_name = folder_name
        self.video_data = video_data
        self.files = []
        self.audio_files = []
        self.frame = 0
        self.number_frames = 0

    def cut_video(self, update_progress):
        """
        a method which cut the modivideos from the "main" video

        @param update_progress: a function which handles the progressbar countprocess
        """
        self.frame = 0
        video = cv2.VideoCapture(self.video_data)
        self.number_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        folder = Path(self.folder_path, self.folder_name)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        board_filename = os.path.join(folder, 'board.mp4')
        slide_filename = os.path.join(folder, 'slides.mp4')
        visualizer_filename = os.path.join(folder, 'visualizer.mp4')
        board_out = cv2.VideoWriter(board_filename, fourcc, fps, (938, 530))
        slide_out = cv2.VideoWriter(slide_filename, fourcc, fps, (700, 530))
        visualizer_out = cv2.VideoWriter(visualizer_filename, fourcc, fps, (960, 530))
        if(video.isOpened() is False):
            print("Error opening video stream or file")
        while(video.isOpened()):
            ret, frame = video.read()
            if ret is True:
                board_out.write(frame[275:805, 17:955])
                slide_out.write(frame[275:805, 1080:1780])
                visualizer_out.write(frame[275:805, 960:1920])
                self.frame += 1
                if self.frame % 30 == 0:
                    update_progress((int)(self.frame/self.number_frames*100))
            else:
                break
        video.release()
        board_out.release()
        slide_out.release()
        visualizer_out.release()
        cv2.destroyAllWindows()
        self.files.append(board_filename)
        self.files.append(slide_filename)
        self.files.append(visualizer_filename)
        self.__board_video = BoardVideo(board_filename)
        self.__slide_video = SlideVideo(slide_filename)
        self.__visualizer_video = VisualizerVideo(visualizer_filename)

    def get_board_video(self):
        return self.__board_video

    def get_slide_video(self):
        return self.__slide_video

    def get_visualizer_video(self):
        return self.__visualizer_video

    def cut_audio_from_video(self):
        """
        a method to get the audio from a video and save it in the project folder
        and create a object of this

        @return: a audio object which contains the path
        """

        folder = Path(self.folder_path, self.folder_name)
        audio_from_video = 'audio.mp3'
        audio = AudioFileClip(self.video_data)
        audio.write_audiofile(os.path.join(folder, audio_from_video), verbose=False, logger=None)
        extracted_audio = Path(folder, audio_from_video)
        self.audio_files.append(extracted_audio)
        return Audio(extracted_audio)