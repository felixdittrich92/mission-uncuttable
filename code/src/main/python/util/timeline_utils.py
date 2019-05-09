import math

# should be changable later
PIXELS_PER_SECOND = 16


def get_px_per_second():
    # s = Settings.get_instance().get_dict_settings()
    # return int(s["Timeline"]["pixels_per_second"])

    return PIXELS_PER_SECOND


def pos_to_seconds(pos):
    return pos / get_px_per_second()


def seconds_to_pos(sec):
    return int(math.ceil(sec * get_px_per_second()))


# for debugging
def print_clip_info(clip):
    print('position: {}\nstart: {}\nend: {}\nduration: {}'.format(
        clip.Position(), clip.Start(), clip.End(), clip.Duration()))
