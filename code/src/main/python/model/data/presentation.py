from pdf2image import convert_from_path
import os
import numpy as np
import cv2
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
from slide import Slide
from media_file import MediaFile

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
        in the project folder
    
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


    def check_color(self):
        """
        a method which checks if the place for a video is free to show it 

        @return: True if region of interest is completly white or gray
        """
        input_file = Path(self.file_path, self.filename)
        picture = cv2.imread(str(input_file))
        height = picture.shape[0]
        width = picture.shape[1]
        # upper y point
        y1 = int((73.8 * height) / 100)
        # lower y point
        y2 = int((94.7 * height) / 100)
        # left x point
        x1 = int((79.3 * width) / 100)
        # right x point
        x2 = int(width)
        white = 255
        gray = 32
        img = cv2.imread(str(input_file), cv2.IMREAD_GRAYSCALE)
        roi = img[y1:y2, x1:x2]

        if np.all(roi == white) == True:
            return True
        elif np.all(roi == gray) == True:
            return True
        else:
            return False

    def picture_in_presentation(self, file_path_small_img, small_img):
        """
        a method which takes two images and overlay the second one above the first one if place is white

        @param file_path_small_img: the path to the overlay image
        @param small_img: the name of the overlay image
        """

        large_img = Path(self.file_path, self.filename)
        large_img = cv2.imread(str(large_img))
        height = large_img.shape[0]
        width = large_img.shape[1]

        small_img = Path(file_path_small_img, small_img)
        small_img = cv2.imread(str(small_img))
        small_img = cv2.resize(small_img, (250, 200)) # little picture size (width,height)

        x_offset = width - 250 # only for resolution 250 
        bottom = ((3.7 * height) / 100) # blue bottom ground
        y_offset = int((height - 200) - bottom) # only for resolution 200 

        if self.check_color() == True: 
            large_img[y_offset:y_offset+small_img.shape[0], x_offset:x_offset+small_img.shape[1]] = small_img
            self.files.append(Slide(large_img[y_offset:y_offset+small_img.shape[0], x_offset:x_offset+small_img.shape[1]]))
        else:
            self.files.append(Slide(large_img))
