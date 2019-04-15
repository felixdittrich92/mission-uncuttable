from .operation import Operation

class History:
    def __init__(self, operations = []):
        if(len(operations) > 0):
            self.operations = operations
        else:
            self.operations = []
        
    def apply_history(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def do_operation(self, operations):
        pass    