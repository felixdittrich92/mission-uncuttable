from pdf2image import convert_from_path
import os
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
from model.data import Slide

class Presentation:

    def __init__(self, file_data):
        """
        Constructor of the class
        """
        self.file_data = file_data
        self.files = []


    def convert_pdf(self, folder_path, folder_name, resolution):

        """
        a method that takes a path and a PDF file, converts them to JPG, and then saves the individual images
        in the project folder and creates a object with the list of single files

        @param folder_path: path to the project folder
        @param folder_name: name of the project folder
        @param resolution: resolution for every converted pdf picture
        @return: a list with the filepath strings
        """

        input_file = self.file_data
        check_pdf = fnmatch(input_file, '*.pdf')
        if check_pdf == True:
            folder = Path(folder_path, folder_name)

            pages = convert_from_path(str(input_file), resolution) #resolution standard must be 250

            for page_number, page in enumerate(pages, start=1):
                target = folder / f"{page_number:03d}.jpg"
                page.save(str(target),  'JPEG')
                self.files.append(str(target))
            
            Slide(self.files)
            return self.files

        else:
            print("the datatype must be .pdf")

