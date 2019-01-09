from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence


class Shortcut:
    """A class for simplifying the creation of a shortcut using PyQt5 QShortcuts."""
    def __init__(self, window, key_sequence, operation):
        """
        Creates a new QShortcut

        @param window QMainWindow the shortcut gets assigned to
        @param key_sequence The key sequence to activate the shortcut
        @param operation String for sample output
        """
        shortcut = QShortcut(QKeySequence(key_sequence), window)
        shortcut.activated.connect(lambda: self.__execute(operation))

    def __execute(self, operation):
        """
        Placeholder

        @param operation String for sample output
        """
        print(operation + " executed")
