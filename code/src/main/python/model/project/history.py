from .operation import Operation

class History:
    """
    Represents the history of a project and manages operations.
    """
    def __init__(self, operations = []):
        self.operations = operations
        self.__last_operation = len(operations) - 1
    
    def apply_history(self):
        pass

    def undo_last_operation(self):
        """
        Function that undos the last operation in the history.
        """
        if (self.__last_operation > -1):
            self.operations[self.__last_operation].undo()
            self.__last_operation -= 1
        else:
            raise Exception("No operation to undo in history. History is empty.")
        

    def redo_last_operation(self):
        """
        Function that redos the last undone operation in the history.
        """
        if (self.__last_operation + 1 < len(self.operations)):
            self.operations[self.__last_operation + 1].do()
            self.__last_operation += 1
        else:
            raise Exception("No operation to redo in history.")

    def do_operation(self, operation):
        """
        Executes a given operation and adds it to the history.
        @type   operation: Operation
        @param  operation: An operation that is executed.
        """
        # Add operation to history
        if(len(self.operations) > self.__last_operation + 1):
            # Other operation is overriden
            self.operations[self.__last_operation + 1] = operation
            # Remove undone operations
            self.operations = self.operations[0:(self.__last_operation + 2)]
        else:
            # Operation is added at the end
            self.operations.append(operation)
        self.__last_operation += 1
        # Execute operation
        operation.do()
        print(self.__last_operation)

    def get_num_operations(self):
        """
        Function that returns the Number of operations that can be undone
        """
        return self.__last_operation + 1

    def get_num_undone_operations(self):
        """
        Function that returns the number of operations that can be redone.
        @rtype Number
        @return Number of operations that can be redone.
        """
        return len(self.operations) - self.__last_operation
