#from model.project import Operation
class TestOperation():
    """
    Operation that increments all elements of a list of type number
    """
    def __init__(self, testdata):
        self.testdata = testdata

    def do(self):
        for i in range(0, len(self.testdata)):
            self.testdata[i] += 1
    
    def undo(self):
        for i in range(0, len(self.testdata)):
            self.testdata[i] -= 1