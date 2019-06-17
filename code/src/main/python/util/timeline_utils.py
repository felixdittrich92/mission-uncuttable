import math
import uuid
import os

import cv2
import openshot
from PyQt5.QtGui import QImage, QPixmap

from config import Resources, Settings
from model.data import FileType


def get_width_from_file(path):
    t = get_file_type(path)

    width = 0

    if t == FileType.VIDEO_FILE:
        v = cv2.VideoCapture(path)
        v.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
        d = v.get(cv2.CAP_PROP_POS_MSEC)
        width = seconds_to_pos(d / 1000)

    elif t == FileType.AUDIO_FILE:
        c = openshot.Clip(path)
        d = c.Duration()
        width = seconds_to_pos(d)

    elif t == FileType.IMAGE_FILE:
        width = get_px_per_second()

    return width


def get_pixmap_from_file(path, frame):
    t = get_file_type(path)

    if t == FileType.IMAGE_FILE:
        image = cv2.imread(path)
        if image is None:
            return None

    elif t == FileType.VIDEO_FILE:
        v = cv2.VideoCapture(path)
        v.set(cv2.CAP_PROP_POS_FRAMES, frame)

        success, image = v.read()
        if not success:
            return None

    elif t == FileType.AUDIO_FILE:
        path = Resources.images.media_symbols
        path_to_file = os.path.join(path, "mp3.png")
        pixmap = QPixmap(path_to_file)

        return pixmap

    else:
        return None

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height, width, channel = image.shape
    q_img = QImage(image.data, width, height, 3 * width, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(q_img)

    return pixmap


def get_file_type(path):
    """ Gets the file type from the extension of the file """
    _, ext = os.path.splitext(path)
    if ext in ['.jpg', '.png', '.jpeg']:
        return FileType.IMAGE_FILE
    elif ext in ['.mp4', '.mov']:
        return FileType.VIDEO_FILE
    elif ext in ['.mp3', '.wav']:
        return FileType.AUDIO_FILE

    return FileType.OTHER_FILE


def get_px_per_second():
    s = Settings.get_instance().get_settings()
    return int(s.Invisible.pixels_per_second)


def pos_to_seconds(pos):
    return pos / get_px_per_second()


def seconds_to_pos(sec):
    return int(math.ceil(sec * get_px_per_second()))


def generate_id():
    return str(uuid.uuid4())

# for debugging


def print_clip_info(clip):
    print('position: {}\nstart: {}\nend: {}\nduration: {}'.format(
        clip.Position(), clip.Start(), clip.End(), clip.Duration()))
