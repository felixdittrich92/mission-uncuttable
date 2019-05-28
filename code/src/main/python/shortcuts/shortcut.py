from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

from model.project import Project
from view.exportview import ExportView


class Shortcut:
    """A class for simplifying the creation of a shortcut using PyQt5 QShortcuts."""
    def __init__(self, window, key_sequence, operation):
        """
        Creates a new QShortcut

        @type  window: QMainWindow
        @param window: The window, the shortcut gets assigned to.
        @type  key_sequence: string
        @param key_sequence: The key sequence to activate the shortcut
        @type  operation: string
        @param operation: Operation that should be executed when the shortcut
                            keys are pressed
        """
        shortcut = QShortcut(QKeySequence(key_sequence), window)
        shortcut.activated.connect(lambda: self.__execute(operation))

        self.__history = Project.get_instance().get_history()

    def __execute(self, operation):
        """
        This function executes the operations.

        @param operation: Name of the operation as String
        """
        if operation == "undo":
            try:
                self.__history.undo_last_operation()
            except:
                pass
        elif operation == "redo":
            try:
                self.__history.redo_last_operation()
            except:
                pass
        elif operation == "export":
            export_view = ExportView()
            export_view.start()
