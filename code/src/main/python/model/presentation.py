from pdf2image import convert_from_path
import os


class Presentation:
    """Class that divides a PDF into individual images and converts them to jpg"""

    def __init__(self):
        """Constructor of the class"""
        print('Image erstellt')
        pass

    def convert(self, path, filename, folder_path, folder_name):
        """a method that creates a new project folder split the pdf to pictures and save them in the new folder"""
        folder = os.path.join(folder_path, folder_name)
        os.makedirs(folder)
        pages = convert_from_path(os.path.join(path, filename), 300)
        os.chdir(folder)
        page_number = 1
        for page in pages:
            page.save("{}.jpg".format(page_number), 'JPEG')
            page_number += 1
