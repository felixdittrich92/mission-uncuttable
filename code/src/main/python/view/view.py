import abc
from util import Observable, Observer

class View(Observer, Observable):
    __metaclass__ = abc.ABCMeta
    def __init__(self, parent=None):
        if parent is not None:
            parent.attach(self)

    def update(self):
        self.refresh()
        self.__notify()

    def update_attribute(self, attribute, value):
        pass

    def add_view(self, view):
        self.attach(view)

    @abc.abstractmethod
    def refresh(self):
        """
        Abstract method for refreshing the view
        is called by update method
        """
        return

