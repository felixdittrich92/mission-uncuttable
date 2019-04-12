from pdf2image import convert_from_path
import os
import numpy as np
import cv2
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
import shutil


def convert_pdf(file_path, filename, new_project_path, new_project_name):
    """
    a function that takes a path and a PDF file, converts them to JPG, and then saves the individual images
    in the new created folder
    
    @param file_path: the path to the pdf
    @param filename: the name of the pdf
    @param new_project_path: path for the new project
    @param new_project_name: name for the new project
    """
    input_file = Path(file_path, filename)
    check_pdf = fnmatch(input_file, '*.pdf')
    
    if check_pdf == True:
        folder = Path(new_project_path, new_project_name)

        if os.path.exists(folder):
            print("Error: folder exists select a new project name")
            return

        folder.mkdir(exist_ok=True) 
        pages = convert_from_path(str(input_file), 250)
        files = []
    
        #images = Slide()
        for page_number, page in enumerate(pages, start=1):
            target = folder / f"{page_number:03d}.jpg"
            page.save(str(target),  'JPEG')  #in Klasse slide speichern  # page.save(images, 'JPEG')

        for file in os.listdir(folder):
            files.append(file)

        files.sort()
    else:
        print("the datatype must be .pdf")

def convert_mp4(file_path, filename, new_project_path, new_project_name):
    """
    a function that takes a path and a mp4 file, split the video in frames, and then saves the individual images
    in the new created folder
    
    @param file_path: the path to the pdf
    @param filename: the name of the pdf
    @param new_project_path: path for the new project
    @param new_project_name: name for the new project
    """
    input_file = Path(file_path, filename)
    check_mp4 = fnmatch(input_file, '*.mp4')

    if check_mp4 == True:
        folder = Path(new_project_path, new_project_name)

        if os.path.exists(folder):
            print("Error: folder exists select a new project name")
            return

        folder.mkdir(exist_ok=False) 
        input_file = Path(file_path, filename)
        cap = cv2.VideoCapture(str(input_file))
        files = []
        current_frame = 0

        while (True):
            ret, frame = cap.read()
            if not ret:
                break
            else:
                cv2.imwrite(os.path.join(folder, "%04d.jpg" % current_frame), frame) #in Klasse Video speichern
                current_frame += 1

        cap.release()
        cv2.destroyAllWindows()
    
        for file in os.listdir(folder):
            files.append(file)
       
        files.sort()

    else:
        print("the datatype must be .mp4")


def add_file_to_project(file_path, filename, project_path, project_name):
    """
    a function which takes a file and write it in the specific folder if the file has a usefull format
    
    @param file_path: path to the file
    @param filename: name of the file
    @param project_path: the path from the project folder
    @param project_name: the name of the folder
    """
    file_to_add = Path(file_path, filename)

    if file_to_add.suffix in ['.jpg', '.mp4', '.png']:
        folder = Path(project_path, project_name)
        shutil.copy(str(file_to_add), str(folder))
    else:
        print("the datatype must be .jpg or .mp4 or .png")


def delete_folder(project_path, project_name):
    """
    a function which delete a project folder and all files
    
    @param project_path: the path to the folder
    @param project_name: the name of the folder
    """
    folder = Path(project_path, project_name)
    shutil.rmtree(folder, ignore_errors=True)


def check_color(file_path, filename, y1, y2, x1, x2):
    """
    a function which checks if the place for a video is free to show it 

    @param file_path: the path to the file
    @param filename: the name of the file
    @param y1: Point(x,min) in a coordinate system for the region of interest
    @param y2: Point(x,max)
    @param x1: Point(min, y)
    @param x2: Point(max, y)

    @return: True if region of interest is completly white or gray
    """
    input_file = Path(file_path, filename)
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
    

def picture_in_presentation(file_path, filename, file_path_small_img, small_img, y1, y2, x1, x2):
    """
    a function which takes two images and overlay the second one above the first one if place is white

    @param file_path: the path to the presentation image
    @param filename: the name of the presentation image
    @param file_path_small_img: the path to the overlay image
    @param small_img: the name of the overlay image
    @param y1: Point(x,min) in a coordinate system for the region of interest
    @param y2: Point(x,max)
    @param x1: Point(min, y)
    @param x2: Point(max, y)

    @return: a image with a overlay or a image without a overlay

    """
    large_img = Path(file_path, filename)
    large_img = cv2.imread(str(large_img))
    height = large_img.shape[0]
    width = large_img.shape[1]

    small_img = Path(file_path_small_img, small_img)
    small_img = cv2.imread(str(small_img))
    small_img = cv2.resize(small_img, (250, 200))

    x_offset = width - 250 #only for resolution 250 
    y_offset = height - 235 #only for resolution 250 

    if check_color(file_path, filename, y1, y2, x1, x2) == True:
        large_img[y_offset:y_offset+small_img.shape[0], x_offset:x_offset+small_img.shape[1]] = small_img
        #cv2.imwrite('test.jpg', large_img)
        return large_img
    else:
        #cv2.imwrite('test.jpg', large_img)
        return large_img
