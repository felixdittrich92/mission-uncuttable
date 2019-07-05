""" Utilities that are needed in the timelineview. """


def frames_to_pixels_float(frames, zoom_factor):
    """ Convenience function for conversion from frames to pixels.

    @param frames:      The number of frames.
    @type frames:       int
    @param zoom_factor: The zoom factor in pixels per frame.
    @type zoom_factor:  float
    @return:            The corresponding number of pixels to the number
                        of frames.
    """
    return frames * zoom_factor


def pixels_to_frames_float(pixels, zoom_factor):
    """ Convenience function for conversion from pixels to frames.

    @param pixels:      The number of pixels.
    @type pixels:       int
    @param zoom_factor: The zoom factor in pixels per frame.
    @type zoom_factor:  float
    @return:            The corresponding number of frames to the number
                        of pixels.
    """
    return pixels / zoom_factor


def frames_to_pixels(frames, zoom_factor):
    """
    Convenience function for conversion from frames to pixels. Returns
    a rounded value.

    @param frames:      The number of frames.
    @type frames:       int
    @param zoom_factor: The zoom factor in pixels per frame.
    @type zoom_factor:  float
    @return:            The corresponding number of pixels to the number
                        of frames, rounded to the nearest integer.
    """
    return round(frames_to_pixels_float(frames, zoom_factor))


def pixels_to_frames(pixels, zoom_factor):
    """
    Convenience function for conversion from pixels to frames. Returns
    a rounded value.

    @param pixels:      The number of pixels.
    @type pixels:       int
    @param zoom_factor: The zoom factor in pixels per frame.
    @type zoom_factor:  float
    @return:            The corresponding number of frames to the number
                        of pixels, rounded to the nearest integer.
    """
    return round(pixels_to_frames_float(pixels, zoom_factor))
