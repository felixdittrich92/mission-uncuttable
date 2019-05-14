"""
The controller module for communication between timelineview and
timelinemodel.
"""

import os
import uuid
import math

import cv2
import openshot
from PyQt5.QtGui import QImage, QPixmap

from config import Resources
from model.data import FileType

# from view.timeline.timelineview.timeline_view import TimelineView  # may not be needed

# Todo: Fill the interface methods which translate actions from the
#       Ubicut frontend (view) to the backend (model) with some
#       function.

# should be changable later
PIXELS_PER_SECOND = 16


class TimelineController:
    """
    The controller between the TimelineView and the TimelineModel.
    """

    __instance = None

    @staticmethod
    def get_instance():
        return TimelineController.__instance

    def __init__(self, timeline_view):
        TimelineController.__instance = self

        self.__timeline_view = timeline_view

    def create_timeable(self, track_id, name, width, x_pos, res_left, res_right, model):
        """
        Create a new object in the timeline model to represent a new
        timeable.

        @param data: The data needed to now what the timeable has to
                     contain and what track it has to be added to.
                     Important note: You may replace this parameter
                     with multiple ones if required while implementing
                     this method.
        @return:     Nothing.
        """
        track = self.__timeline_view.tracks[track_id]
        track.create_timeable(name, width, x_pos, 0, model,
                              res_left=res_left, res_right=res_right)

    def delete_timeable(self, id):
        """
        Delete the model's representation of a timeable.

        @param id: The timeable's unique ID.
        @return:   Nothing.
        """
        pass

    def rename_timeable(self, id, name):
        """
        Rename the model's representation of a timeable.

        @param id:   The timeable's unique ID.
        @param name: The new name of the timeable.
        @return:     Nothing.
        """
        pass

    def move_timeable(self, id, start):
        """
        Set a new start of the model 's representation of a timeable.

        @param id:    The timeable's unique ID.
        @param start: The new start time of the timeable.
        @return:      Nothing.
        """
        pass

    def split_timeable(self, id, time):
        """
        Split the model's representation of a timeable at a specified
        time relative to the start of the timeable.

        The split will happen after the time-th frame of the timeable.
        This means that the time-th frame will belong to the first but
        not the second one of the resulting timeables.

        @param id:   The timeable's unique ID.
        @param time: The time at which the timeable should be split.
        @return:     Nothing.
        """
        pass

    def remove_timeable_part(self, id, start, end):
        """
        Remove a part of the model's representation of a timeable
        between a start and an end time relative to the start of the
        timeable.

        The removed part includes the frames specified by start and end.

        @param id:    The timeable's unique ID.
        @param start: The number of the first frame removed.
        @param end:   The number of the last frame removed.
        @return:      Nothing.
        """
        pass

    def select_timeable(self, id, selected=True):
        """
        Set the selected-state of the model's representation of a
        timeable.

        @param id:       The timeable's unique ID.
        @param selected: The selected-state.
        @return:         Nothing.
        """
        pass

    @staticmethod
    def get_width_from_file(path):
        t = TimelineController.get_file_type(path)

        width = 0

        if t == FileType.VIDEO_FILE:
            v = cv2.VideoCapture(path)
            v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
            d = v.get(cv2.CAP_PROP_POS_MSEC)
            width = TimelineController.seconds_to_pos(d / 1000)

        elif t == FileType.AUDIO_FILE:
            c = openshot.Clip(path)
            d = c.Duration()
            width = TimelineController.seconds_to_pos(d)

        elif t == FileType.IMAGE_FILE:
            width = TimelineController.get_px_per_second()

        return width

    @staticmethod
    def get_pixmap_from_file(path, frame):
        t = TimelineController.get_file_type(path)

        if t == FileType.IMAGE_FILE:
            image = cv2.imread(path)
            if image is None:
                return None

        elif t == FileType.VIDEO_FILE:
            v = cv2.VideoCapture(path)
            v.set(cv2.CAP_PROP_POS_FRAMES, frame)

            success, image = v.read()
            if not success:
                return None

        elif t == FileType.AUDIO_FILE:
            path = Resources.get_instance().images.media_symbols
            path_to_file = os.path.join(path, "mp3logo.jpg")
            pixmap = QPixmap(path_to_file)

            return pixmap

        else:
            return None

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, channel = image.shape
        q_img = QImage(image.data, width, height, 3 * width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        return pixmap

    @staticmethod
    def get_file_type(path):
        """ Gets the file type from the extension of the file """
        _, ext = os.path.splitext(path)
        if ext in ['.jpg', '.png', '.jpeg']:
            return FileType.IMAGE_FILE
        elif ext in ['.mp4', '.mov']:
            return FileType.VIDEO_FILE
        elif ext in ['.mp3', '.wav']:
            return FileType.AUDIO_FILE

        return FileType.OTHER_FILE

    @staticmethod
    def get_px_per_second():
        # s = Settings.get_instance().get_dict_settings()
        # return int(s["Timeline"]["pixels_per_second"])

        return PIXELS_PER_SECOND

    @staticmethod
    def pos_to_seconds(pos):
        return pos / TimelineController.get_px_per_second()

    @staticmethod
    def seconds_to_pos(sec):
        return int(math.ceil(sec * TimelineController.get_px_per_second()))

    @staticmethod
    def generate_id():
        return str(uuid.uuid4())

    # for debugging
    @staticmethod
    def print_clip_info(clip):
        print('position: {}\nstart: {}\nend: {}\nduration: {}'.format(
            clip.Position(), clip.Start(), clip.End(), clip.Duration()))
