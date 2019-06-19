class TimeableGroup:
    """
    A TimeableGroup represents one or more Timeables that will be connected together.
    This means that all timeables in the group will be moved together.
    """

    def __init__(self, group_id, timeables):
        """
        Creates a new timeable group

        @param ids: list with ids of the timeable views in the group
        """
        self.group_id = group_id
        self.timeables = timeables

        for t in self.timeables:
            t.group_id = self.group_id

    def has_timeable(self, id):
        """
        Checks if the timeable with the given id is in this group

        @id: id of the timeable view
        @return: True if if timeable is in group, False otherwhise
        """
        return id in self.ids

    def add_timeable(self, timeable):
        """
        Adds a timeable to a timeable group.

        @param timeable: the timeable view that will be added
        @return: Nothing
        """
        if timeable in self.timeables:
            return

        self.timeables.append(timeable)
        timeable.group_id = self.group_id

    def remove_timeable(self, timeable):
        """
        Removes the timeable with the given id from the group

        @param timeable: the timeable view that will be removed
        @return: Nothing
        """
        while timeable in self.timeables:
            self.timeables.remove(timeable)

    def is_move_possible(self, diff):
        """
        Checks if the group can be moved by the value of diff

        @param diff: the difference between the old and new position of the timeables
        @return: True if move is possible, False otherwhise
        """
        return all(t.is_move_possible_diff(diff) for t in self.timeables)
