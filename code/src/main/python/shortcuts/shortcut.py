from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


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
        @param operation: String for sample output
        """
        shortcut = QShortcut(QKeySequence(key_sequence), window)
        shortcut.activated.connect(lambda: self.__execute(operation))

    def __execute(self, operation):
        """
        This function is going to be replaced when real operations are
        implemented and ready to be executed by a shortcut.

        @type  operation: string
        @param operation: String for sample output
        """
        print(operation + " executed")
