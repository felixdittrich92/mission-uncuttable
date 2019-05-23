class AutocutController:
    """A class used as the Controller for the autocut window."""
    def __init__(self, view):
        self.autocut_view = view
        self.autocut_view.show()
