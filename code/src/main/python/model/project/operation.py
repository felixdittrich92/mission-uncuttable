
from abc import ABC, abstractmethod
class Operation(ABC):
    def __init__(self, name):
        self.___name = name()

    @abstractmethod
    def do(self):
        pass

    @abstractmethod
    def undo(self):
        pass
