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

        self.video_editor_view = window

    def __execute(self, operation):
        """
        This function executes the operations.

        @param operation: Name of the operation as String
        """
        if operation == "undo":
            self.video_editor_view.actionUndo.trigger()
        elif operation == "redo":
            self.video_editor_view.actionRedo.trigger()
        elif operation == "export":
            self.video_editor_view.actionExport.trigger()
        elif operation == "save":
            self.video_editor_view.actionSpeichern.trigger()
        elif operation == "saveas":
            self.video_editor_view.actionSpeichern_als.trigger()
