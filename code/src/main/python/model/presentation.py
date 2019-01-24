from wand.image import Image as wa
from slide import Slide


class Presentation:
    """Class that divides a PDF into individual images and converts them to jpg"""
    def __init__(self):
        """Constructor of the class"""
        print('Image erstellt')
        pass

    def convert(self, path, filename):
        """a method that takes a path and a PDF file, converts them to JPG, and then saves the individual images"""
        pdf = wa(file=path + filename, resolution=300)
        pdf_images = pdf.convert("jpeg")
        page_number = 1
        for img in pdf_images.sequence:
            page = wa(image=img)
            slide = []
            slide.append(Slide(page_number, page))
            page_number += 1
