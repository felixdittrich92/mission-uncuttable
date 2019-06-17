class TimeableGroup:
    """ Timeables that are grouped together will also be moved together """

    def __init__(self, ids):
        """
        @param ids: ids of the timeable views in the group
        """
        self.ids = ids

    def has_timeable(self, id):
        return id in self.ids

    def remove_timeable(self, id):
        """ Removes a timeable from the group """
        if id not in self.ids:
            return

    def is_move_possible(self, pos):
        """ checks if all timeables in the group can be moved to pos """
        return False
