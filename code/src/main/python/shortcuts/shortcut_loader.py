from config import Settings
from shortcuts import Shortcut


class ShortcutLoader:
    """A class that creates shortcuts."""

    def __init__(self, window):
        """
        Creates the shortcuts.

        Queries all entries of the Shortcuts section in the config file.
        For every entry a new shortcut is going to be created.

        @type  window: QMainWindow
        @param window: The Window, the shortcut gets assigned to.
        """
        shortcuts = Settings.get_instance().get_dict_settings()["shortcuts"]

        self.loaded_shortcuts = []
        for operation in shortcuts:
            if operation == "starter":
                self.starter = shortcuts[operation]["current"]
            else:
                key = shortcuts[operation]["current"]
                key_sequence = self.starter + "+" + key
                shortcut = Shortcut(window, key_sequence, operation)
                self.loaded_shortcuts.append(shortcut)
