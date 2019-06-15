class TimeableGroup:
    """ Timeables that are grouped together will also be moved together """

    def __init__(self, ids):
        """
        @param ids: ids of the timeables in the group
        """
        self.ids = ids

    def is_move_possible(self, pos):
        """ checks if all timeables in the group can be moved to pos """
        return False
