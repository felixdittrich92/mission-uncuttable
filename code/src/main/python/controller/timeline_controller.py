"""
The controller module for communication between timelineview and
timelinemodel.
"""

import os

import cv2
from PyQt5.QtGui import QImage, QPixmap

# from view.timeline.timelineview.timeline_view import TimelineView  # may not be needed

# Todo: Fill the interface methods which translate actions from the
#       Ubicut frontend (view) to the backend (model) with some
#       function.


class TimelineController:
    """
    The controller between the TimelineView and the TimelineModel.
    """
    def __init__(self, timeline_view):
        self.__timeline_view = timeline_view

    def create_timeable(self, data=None):
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
        pass

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
    def get_pixmap_from_file(path, frame):
        _, ext = os.path.splitext(path)
        if ext in ['.jpg', '.png']:
            image = cv2.imread(path)
            if image is None:
                return image
        else:
            v = cv2.VideoCapture(path)
            v.set(cv2.CAP_PROP_POS_FRAMES, frame)

            success, image = v.read()
            if not success:
                return None

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        height, width, channel = image.shape
        q_img = QImage(image.data, width, height, 3 * width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        return pixmap
