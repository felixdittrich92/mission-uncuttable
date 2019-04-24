import openshot
import openshot.QtImageReader
import openshot.FFmpegWriter
AUDIO_LAYOUT = openshot.LAYOUT_STEREO

class TimelineModel:
    def __init__(self, width, height, framerate, sample_rate, channels):
        timeline = openshot.Timeline(width, height, openshot.Fraction(framerate), sample_rate, channels)
    
    def add_clip(self, path):
        timeline.AddClip(gen_clip(path))
    
    def gen_clip(self, path):
        if path.endswith('.png', '.jpg', '.jpeg', '.svg'):
            return openshot.QtImageReader(path)

        '''
        elif path.endswith('.flac', '.mp3', '.wav', '.ogg'):
            return 0 
        '''

        elif path.endswith('.mp4', '.avi', '.mov', '.flv', '.wmv'):
            return openshot.FFmpegWriter(path)

    
