import os
import skvideo.io
import cv2

from pathlib import Path
from moviepy.audio.io.AudioFileClip import AudioFileClip
from model.data import VisualizerVideo, BoardVideo, Audio, SlideVideo, SpeakerVideo


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
        self.width = 0

    def cut_video(self, update_progress):
        """
        a method which cut the modivideos from the "main" video

        @param update_progress: a function which handles the progressbar countprocess
        """
        self.frame = 0
        reader = skvideo.io.FFmpegReader(self.video_data, {}, {})
        videometadata = skvideo.io.ffprobe(self.video_data)
        self.frame_rate = videometadata['video']['@avg_frame_rate']
        self.number_frames = int(videometadata['video']['@nb_frames'])
        folder = Path(self.folder_path, self.folder_name)

        board_filename = os.path.join(folder, 'board.mp4')
        slide_filename = os.path.join(folder, 'slides.mp4')
        visualizer_filename = os.path.join(folder, 'visualizer.mp4')

        board_out = skvideo.io.FFmpegWriter(board_filename, inputdict={
            "-r": self.frame_rate
        })

        slide_out = skvideo.io.FFmpegWriter(slide_filename, inputdict={
            "-r": self.frame_rate
        })

        visualizer_out = skvideo.io.FFmpegWriter(visualizer_filename, inputdict={
            "-r": self.frame_rate
        })

        # iterate through the frames
        for frame in reader.nextFrame():
            self.height, self.width = frame.shape[:2]
            if self.width == 1920:
                board_out.writeFrame(frame[330:750, 18:770])
                slide_out.writeFrame(frame[225:855, 917:1760])
                visualizer_out.writeFrame(frame[225:855, 775:1900])
                self.frame += 1
                if self.frame % 30 == 0:
                    update_progress((int)(self.frame/self.number_frames*100)) 
            else:
                board_out.writeFrame(frame[219:500, 12:514])
                slide_out.writeFrame(frame[149:570, 610:1172])
                visualizer_out.writeFrame(frame[149:570, 516:1266])

                self.frame += 1
                if self.frame % 30 == 0:
                    update_progress((int)(self.frame/self.number_frames*100))
        board_out.close()
        slide_out.close()
        visualizer_out.close()
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

    def get_speaker_video(self):
        return self.__speaker_video

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
    
    def cut_zoom_video(self, update_progress):
        """
        a method which track the speaker in the video and cut a video from this

        @param update_progress: a function which handles the progressbar countprocess
        """

        self.frame = 0
        folder = Path(self.folder_path, self.folder_name)
        speaker_filename = os.path.join(folder, 'speaker.mp4')
        video_data = self.files[0]

        reader = skvideo.io.FFmpegReader(video_data, {}, {})
        #fgbg = cv2.createBackgroundSubtractorMOG2()
        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5 , 1)

        videometadata = skvideo.io.ffprobe(video_data)
        self.frame_rate = videometadata['video']['@avg_frame_rate']
        self.number_frames = int(videometadata['video']['@nb_frames'])

        x, y, width, height = 220, 400, 300, 850
        #x, y, width, height = 350, 350, 180, 650
        track_window = (width,x,height,y)

        speaker_out = skvideo.io.FFmpegWriter(speaker_filename, inputdict={
            "-r": self.frame_rate
        })

        for frame in reader.nextFrame():
            gmask = fgbg.apply(frame)
            is_ok, track_window = cv2.meanShift(gmask, track_window, term_crit)
            x, y, width, height = track_window
            if self.width == 1920:
                y = 100
                speaker_out.writeFrame(frame[y:y+height, x+100:x+width])
                self.frame += 1
                if self.frame % 30 == 0:
                    update_progress((int)(self.frame/self.number_frames*100))
            else:   
                y = 250
                speaker_out.writeFrame(frame[y-100:y+height, x:x+width])
                self.frame += 1
                if self.frame % 30 == 0:
                    update_progress((int)(self.frame/self.number_frames*100))  
                
        speaker_out.close()
        self.files.append(speaker_filename)
        self.__speaker_video = SpeakerVideo(speaker_filename)
