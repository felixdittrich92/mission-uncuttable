from pdf2image import convert_from_path
import os
import numpy as np
import cv2
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
from moviepy.editor import *
from .video import Video
import shutil

class VideoSplitter:

    def __init__(self, folder_path, folder_name, video_path, video_name):
        self.folder_path = folder_path
        self.folder_name = folder_name
        self.video_path = video_path
        self.video_name = video_name

    def large_video(self):
        """
        a function to get the part of the speaker from the "main video" and save it in the project folder

        @param folder_path: path to the project folder
        @param folder_name: the name of the project folder
        @param video_path: the path to the video
        @param video_name: the name of the "main video"

        @return: a String to the new generated video
        """

        video_file = Path(self.video_path, self.video_name)
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
        #return new_large_video_path anstaat return video in Klasse video
        Video(new_large_video_path)


def small_video(self):
    """
    a function to get the part of the foil/visualiser from the "main video" and save it in the project folder

    @param folder_path: path to the project folder
    @param folder_name: the name of the project folder
    @param video_path: the path to the video
    @param video_name: the name of the "main video"

    @return: a String to the new generated video
    """
    video_file = Path(self.video_path, self.video_name)
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
    #return new_small_video_path
    Video(new_small_video_path) #mehrere Konstruktoren ???? 


#need tests
def audio_from_video(self):
    """
    a function to get the audio from a video and save it in the project folder

    @param folder_path: path to the project folder
    @param folder_name: the name of the project folder
    @param video_path: the path to the video
    @param video_name: the name of the "main video"

    @return: a String to the new generated audio
    """

    folder = Path(self.folder_path, self.folder_name)
    video = Path(self.video_path, self.video_name)

    audio_from_video = 'audio.mp3'
    video = VideoFileClip(str(video))
    audio = video.audio
    audio.write_audiofile(os.path.join(folder,str(audio_from_video)))
    extracted_audio = Path(folder, audio_from_video)
    #return extracted_audio # in klasse video
    Video(extracted_audio)
