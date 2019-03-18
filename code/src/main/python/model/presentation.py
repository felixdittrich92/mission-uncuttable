from pdf2image import convert_from_path
from pathlib import Path


class Presentation:
    """Class that divides a PDF into individual images and converts them to jpg"""

    def __init__(self):
        """Constructor of the class"""
        pass

    def convert(self, path, filename, new_project_path, new_project_name):
        """a function that creates a new project folder split the pdf to pictures and save them in the new folder"""
        folder = Path(new_project_path, new_project_name)
        folder.mkdir(exist_ok=True) 
        input_file = Path(path, filename)
        pages = convert_from_path(str(input_file), 300)
        for page_number, page in enumerate(pages, start=1):
            target = folder / f"{page_number:03d}.jpg"
            page.save(str(target),  'JPEG')