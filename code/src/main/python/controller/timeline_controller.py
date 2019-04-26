from view.timeline.timelineview.timeline_view import TimelineView

class TimelineController:
    def __init__(self, timeline_view):
        self.__timeline_view = timeline_view

    def create_timeable(self, data=None):
        """
        Create a new object in the timeline model to represent a new
        timeable.

        @param data: The data needed to now what the timeable has to
                     contain.
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
        not the second of the resulting timeable's parts.

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
        @param start:
        @param end:
        @return:
        """
        pass

    def select_timeable(self, id, selected=True):
        """
        Set the selected state of the model's representation of a
        timeable.

        @param id:       The timeable's unique ID.
        @param selected:
        @return:
        """
        pass
