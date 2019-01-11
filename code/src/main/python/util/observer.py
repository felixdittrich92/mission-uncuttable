import abc


class Observer(metaclass=abc.ABCMeta):
    """
    Define an updating interface for objects that should be notified of
    changes in a subject.
    """

    def __init__(self):
        self._subject = None
        self._observer_state = None

    @abc.abstractmethod
    def update(self, arg):
        """
        Method is called by observed instances
        """
        pass

    @abc.abstractmethod
    def update_attribute(self, attribute_name, attribute_value):
        """
        Method is called by observed instances to update single attribute
        """
        pass
