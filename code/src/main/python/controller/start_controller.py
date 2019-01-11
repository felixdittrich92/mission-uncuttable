class StartController:
    """A class used as the Controller for the start window."""
    def __init__(self, view):
        self.start_view = view
        self.start_view.show()
