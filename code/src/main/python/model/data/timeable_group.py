class TimeableGroup:
    """ Timeables that are grouped together will also be moved together """

    def __init__(self, ids):
        """
        @param ids: ids of the timeable views in the group
        """
        self.ids = ids

    def has_timeable(self, id):
        """
        Checks if the timeable with the given id is in this group

        @id: id of the timeable view
        @return: True if if timeable is in group, False otherwhise
        """
        return id in self.ids

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
