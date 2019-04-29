import math

from config.settings import Settings


def get_px_per_second():
    s = Settings.get_instance().get_dict_settings()

    return s["Timeline"]["pixels_per_second"]


def pos_to_seconds(pos, px_per_sec):
    return pos / px_per_sec


def seconds_to_pos(sec, px_per_sec):
    return int(math.ceil(sec * px_per_sec))


# for debugging
def print_clip_info(clip):
    print('position: {}\nstart: {}\nend: {}\nduration: {}'.format(
        clip.Position(), clip.Start(), clip.End(), clip.Duration()))
