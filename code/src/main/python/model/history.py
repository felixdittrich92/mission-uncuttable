from operation import Operation

class History:
    def __init__(self, Operation):
        self.operations = [Operation]
        
    def apply_history(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass

    def do_operation(self, operations):
        pass    