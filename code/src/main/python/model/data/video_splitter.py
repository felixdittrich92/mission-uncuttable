from pdf2image import convert_from_path
import os
import numpy as np
import cv2
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
from moviepy.editor import *
from .visualiser_video import VisualiserVideo
from .board_video import BoardVideo
from .audio import Audio
import shutil

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

    def large_video(self):
        """
        a method to get the part of the speaker from the "main video" and save it in the project folder
        and create a object of this
        """

        video_file = self.video_data
        folder = Path(self.folder_path, self.folder_name)

        cap = cv2.VideoCapture(str(video_file))

        large_video_name = 'large_video.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(os.path.join(folder,str(large_video_name)), fourcc , 21, (938, 530))

        if(cap.isOpened() == False):
            print("Error opening video stream or file")

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frame = frame[275:805, 17:955]
                out.write(frame)

            else:
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        new_large_video_path = Path(folder, large_video_name)
        self.files.append(new_large_video_path)
        return BoardVideo(new_large_video_path)


    def small_video(self):
        """
        a method to get the part of the foil/visualiser from the "main video" and save it in the project folder
        and create a object of this
        """
        video_file = self.video_data
        folder = Path(self.folder_path, self.folder_name)

        cap = cv2.VideoCapture(str(video_file))

        small_video_name = 'small_video.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(os.path.join(folder,str(small_video_name)), fourcc , 21, (700, 530))

        if(cap.isOpened() == False):
            print("Error opening video stream or file")

        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                frame = frame[275:805, 1080:1780]
                out.write(frame)

            else:
                break
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        new_small_video_path = Path(folder, small_video_name)
        self.files.append(new_small_video_path)
        return VisualiserVideo(new_small_video_path)


    def audio_from_video(self):
        """
        a method to get the audio from a video and save it in the project folder
        and create a object of this
        """

        folder = Path(self.folder_path, self.folder_name)
        video = self.video_data

        audio_from_video = 'audio.mp3'
        video = VideoFileClip(str(video))
        audio = video.audio
        audio.write_audiofile(os.path.join(folder,str(audio_from_video)))
        extracted_audio = Path(folder, audio_from_video)
        self.audio_files.append(extracted_audio)
        return Audio(extracted_audio)

