class Slide:
    pass

    def __init__(self, page_number, page):
        self.page_number = page_number
        self.page = page

    def get_image(self):
        return self.page