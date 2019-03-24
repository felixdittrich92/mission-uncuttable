from pdf2image import convert_from_path
import os
import numpy as np
import cv2
from fnmatch import fnmatch
from PIL import Image
from pathlib import Path
import shutil

def convert(file_path, filename, new_project_path, new_project_name):
    """a function that takes a path and a PDF file, converts them to JPG, and then saves the individual images
    in the new created folder"""
    folder = Path(new_project_path, new_project_name)
    folder.mkdir(exist_ok=True) 
    input_file = Path(file_path, filename)
    pages = convert_from_path(str(input_file), 250)
    files = []
    for page_number, page in enumerate(pages, start=1):
        target = folder / f"{page_number:03d}.jpg"
        page.save(str(target),  'JPEG')
    for file in os.listdir(folder):
        files.append(file)

    files.sort()

def add_file_to_project(file_path, filename, project_path, project_name):
    """a function which takes a file and write it in the specific folder if the file has a usefull format"""
    folder = Path(project_path, project_name)
    file_to_add = Path(file_path, filename)
    check_jpg = fnmatch(file_to_add, '*.jpg')
    check_mp4 = fnmatch(file_to_add, '*.mp4')
    check_png = fnmatch(file_to_add, '*.png')
    if check_jpg == True:
        shutil.copy(str(file_to_add), str(folder))
    elif check_mp4 == True:
        shutil.copy(str(file_to_add), str(folder))
    elif check_png == True:
        shutil.copy(str(file_to_add), str(folder))
    else:
        print("the datatype must be .jpg or .mp4 or .png")

def delete_folder(project_path, project_name):
    """a function which delete a project folder and all files"""
    folder = Path(project_path, project_name)
    shutil.rmtree(folder, ignore_errors=True)

def check_color(file_path, filename, y1, y2, x1, x2):
    """
    a function which checks if the place for a video is free to show it 
    @param y1: Point(x,min) in a coordinate system for the region of interrest
    @param y2: Point(x,max)
    @param x1: Point(min, y)
    @param x2: Point(max, y)
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
    
# not finished ToDo behind this point
def picture_in_presentation(img, img_overlay, pos, alpha_mask):
    """a function which set a smaller picture over a bigger picture and can make it transparent"""
    img.setflags(write = 1)
    x, y = pos

    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    if y1 >= y2 or x1 >= y2o or x1o >= x2o:
        return
    
    channels = img.shape[2]

    alpha = alpha_mask[y1o:y2o, x1o:x2o]
    alpha_inv = 1.0 - alpha

    for c in range(channels):
        img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] + alpha_inv * img[y1:y2, x1:x2, c])

    return img

def video_in_slide(file_path, filename, video_path, videoname, y1, y2, x1, x2):
    presentation_file = Path(file_path, filename)
    video_file = Path(video_path, videoname)
    if check_color(file_path, filename, y1, y2, x1, x2) == True:
        cap = cv2.VideoCapture(str(video_file))
        if(cap.isOpened() == False):
            print("Error opening video stream or file")
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imshow('Frame', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        img = cv2.imread(str(presentation_file), cv2.IMREAD_COLOR)
        return img