from pdf2image import convert_from_path
import os
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
import Slide

class Presentation:

    def __init__(self, file_path, filename):
        """
        Constructor of the class
        @param file_path: the path to the pdf
        @param filename: the name of the pdf
        """
        self.file_path = file_path
        self.filename = filename
        self.files = []


    def convert_pdf(self, folder_path, folder_name, resolution):

        """
        a method that takes a path and a PDF file, converts them to JPG, and then saves the individual images
        in the project folder and creates a object with the list of single files

        @param folder_path: path to the project folder
        @param folder_name: name of the project folder
        @param resolution: resolution for every converted pdf picture
        """

        input_file = Path(self.file_path, self.filename)
        check_pdf = fnmatch(input_file, '*.pdf')
        if check_pdf == True:
            folder = Path(folder_path, folder_name)

            pages = convert_from_path(str(input_file), resolution) #Standardwert sollte 250 sein

            for page_number, page in enumerate(pages, start=1):
                target = folder / f"{page_number:03d}.jpg"
                page.save(str(target),  'JPEG')

            for file in os.listdir(folder):
                self.files.append(Slide(file))

        else:
            print("the datatype must be .pdf")

