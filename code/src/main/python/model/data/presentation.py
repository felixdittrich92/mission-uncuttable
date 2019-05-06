from pdf2image import convert_from_path
import os
import numpy as np
import cv2
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
from .slide import Slide

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

    
    def convert_pdf(self, folder_path, folder_name):

        """
        a function that takes a path and a PDF file, converts them to JPG, and then saves the individual images
        in the project folder
    
        @param folder_path: path to the project folder
        @param folder_name: name of the project folder
        """

        input_file = Path(self.file_path, self.filename)
        check_pdf = fnmatch(input_file, '*.pdf')
        if check_pdf == True:
            folder = Path(folder_path, folder_name)

            pages = convert_from_path(str(input_file), 250)

            for page_number, page in enumerate(pages, start=1):
                target = folder / f"{page_number:03d}.jpg"
                page.save(str(target),  'JPEG')

            for file in os.listdir(folder):
                self.files.append(Slide(file))
            
        else:
            print("the datatype must be .pdf")


    def check_color(self, y1, y2, x1, x2):
        """
        a function which checks if the place for a video is free to show it 

        @param y1: Point(x,min) in a coordinate system for the region of interest
        @param y2: Point(x,max)
        @param x1: Point(min, y)
        @param x2: Point(max, y)

        @return: True if region of interest is completly white or gray
        """
        input_file = Path(self.file_path, self.filename)
        white = 255
        gray = 32
        img = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)
        # automatisieren img width and height y1/y2 x1/x2 prozentual berechnen
        roi = img[y1:y2, x1:x2]

        if np.all(roi == white) == True:
            return True
        elif np.all(roi == gray) == True:
            return True
        else:
            return False

    def picture_in_presentation(self, file_path_small_img, small_img, y1, y2, x1, x2):
        """
        a function which takes two images and overlay the second one above the first one if place is white

        @param file_path_small_img: the path to the overlay image
        @param small_img: the name of the overlay image
        @param y1: Point(x,min) in a coordinate system for the region of interest
        @param y2: Point(x,max)
        @param x1: Point(min, y)
        @param x2: Point(max, y)
        """

        large_img = Path(self.file_path, self.filename)
        large_img = cv2.imread(str(large_img))
        height = large_img.shape[0]
        width = large_img.shape[1]

        small_img = Path(file_path_small_img, small_img)
        small_img = cv2.imread(str(small_img))
        small_img = cv2.resize(small_img, (250, 200)) #automatisieren ?

        x_offset = width - 250 #only for resolution 250 
        y_offset = height - 235 #only for resolution 250 

        if self.check_color(y1, y2, x1, x2) == True: 
            large_img[y_offset:y_offset+small_img.shape[0], x_offset:x_offset+small_img.shape[1]] = small_img
            self.files.append(Slide(large_img[y_offset:y_offset+small_img.shape[0], x_offset:x_offset+small_img.shape[1]]))
        else:
            self.files.append(Slide(large_img))
