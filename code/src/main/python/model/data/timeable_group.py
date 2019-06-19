class TimeableGroup:
    """
    A TimeableGroup represents one or more Timeables that will be connected together.
    This means that all timeables in the group will be moved together.
    """

    def __init__(self, ids):
        """
        Creates a new timeable group

        @param ids: list with ids of the timeable views in the group
        """
        self.ids = ids

    def has_timeable(self, id):
        """
        Checks if the timeable with the given id is in this group

        @id: id of the timeable view
        @return: True if if timeable is in group, False otherwhise
        """
        return id in self.ids

    def add_timeable(self, id):
        """
        Adds a timeable to a timeable group.

        @param id: id of the timeable view that will be added
        @return: Nothing
        """
        if id in self.ids:
            return

        self.ids.append(id)

    def remove_timeable(self, id):
        """
        Removes the timeable with the given id from the group

        @param id: id of the timeable view that will be removed
        @return: Nothing
        """
        while id in self.ids:
            self.remove(id)

    def is_move_possible(self, pos):
        """ checks if all timeables in the group can be moved to pos """
        return False
