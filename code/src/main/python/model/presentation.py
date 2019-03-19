from pdf2image import convert_from_path
import os
import numpy
import cv2
from PIL import Image
from pathlib import Path

def convert(file_path, filename, new_project_path, new_project_name):
    """a function that creates a new project folder takes a pdf-file and split it into pictures which will save in the new folder"""
    folder = Path(new_project_path, new_project_name)
    folder.mkdir(exist_ok=True) 
    input_file = Path(file_path, filename)
    pages = convert_from_path(str(input_file), 250) #dont touch this number !!
    files = []

    for page_number, page in enumerate(pages, start=1):
        target = folder / f"{page_number:03d}.jpg"
        page.save(str(target),  'JPEG')

    for file in os.listdir(folder):
        files.append(file)

    files.sort()


def check_color(file_path, filename, left_pixel, upper_pixel, right_pixel, lower_pixel):
    """a function that checks if the place in the picture for video is free"""
    """description: left_pixel and upper_pixel are the (x,y) points for the video place like (0,0) in a coordinate system, right_pixel and lower_pixel are the coordinates of the lower right corner"""
    """@return: true / false"""
    input_file = Path(file_path, filename)
    img = Image.open(input_file)
    width, height = img.size  #1260x945
    imgload = img.load()
    x = left_pixel
    y = upper_pixel
    window_width = right_pixel - left_pixel   #width of the videoplace
        
    while True:
        point = imgload[x, y]
        if point == (255, 255, 255):
            x += 1
            if x == width:
                x -= window_width
                y += 1
            elif x == right_pixel and y == lower_pixel:  
                return True
        else:
            return False