from shortcuts import Shortcut


class ShortcutLoader:
    """A class that creates shortcuts."""
    starter = "Ctrl+"
    key_combinations = {
        "O": "Operation 'O'",
        "E": "Operation 'E'"
    }

    def __init__(self, window):
        """
        Creates the shortcuts.

        Queries all entries of the 'key_combination' dictionary and creates a shortcut for the given starter key(s) and
        the execution keys from the dictionary and assigns a symbolic operation.

        @param window QMainWindow the shortcut gets assigned to
        """
        self.loaded_shortcuts = []
        for key in self.key_combinations:
            key_sequence = self.starter + key
            self.loaded_shortcuts.append(Shortcut(window, key_sequence, self.key_combinations[key]))
