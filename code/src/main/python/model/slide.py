from presentation import Presentation

class Slide:
    """Constructor that saves the current page and page number"""

    def __init__(self, page_number, page):
        self.page_number = page_number
        self.page = page
