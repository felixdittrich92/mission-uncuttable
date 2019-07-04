import json

import openshot
from PyQt5.QtWidgets import QApplication

from .timeable_group import TimeableGroup

from model.project import Project

TIMELINE_DEFAULT_SETTINGS = {
    "fps": {
        "num": 25,
        "den": 1
    },
    "width": 1280,
    "height": 720,
    "sample_rate": 48000,
    "channels": 2,
    "channel_layout": 3
}


class TimelineModel:
    __instance = None

    @staticmethod
    def get_instance():
        """ returns the timeline instance """
        if TimelineModel.__instance is None:
            TimelineModel()

        return TimelineModel.__instance

    def __init__(self, timeline_data=TIMELINE_DEFAULT_SETTINGS):
        """
        initalize the timeline model with given settings
        this class is a singleton so it can only be initialized once

        @param timeline_data: dict with timeline settings
                              (fps, width, height, sample_rate ...)
        """
        if TimelineModel.__instance is not None:
            raise Exception("singleton!")

        TimelineModel.__instance = self

        fps = timeline_data["fps"]
        width = timeline_data["width"]
        height = timeline_data["height"]
        sample_rate = timeline_data["sample_rate"]
        channels = timeline_data["channels"]
        channel_layout = timeline_data["channel_layout"]

        # create openshot timeline object
        self.timeline = openshot.Timeline(width, height, openshot.Fraction(
            fps["num"], fps["den"]), sample_rate, channels, channel_layout)

        self.timeline.Open()

        self.groups = dict()

    def get_clip_by_id(self, clip_id):
        """
        @param clip_id: id of the clip
        """
        for clip in self.timeline.Clips():
            if clip.Id() == clip_id:
                return clip

        return None

    def getTimeline(self):
        return self.timeline

    def get_fps(self):
        return self.timeline.info.fps.num / self.timeline.info.fps.den

    def get_group_dict(self):
        res = dict()
        for g in list(self.groups.keys()):
            res[g] = self.groups[g].get_timeable_ids()

        return res

    def change(self, change_type, key, data):
        """
        @param change_type: insert, delete or update
        @param key: defines what will be changed (clips or effects)
        @param data: dict with data to update
        """
        update_dict = {
            "type": change_type,
            "key": key,
            "value": data
        }

        update_string = json.dumps([update_dict])
        self.timeline.ApplyJsonDiff(update_string)

        project = Project.get_instance()
        if not project.changed:
            project.changed = True

    def update_duration(self):
        new_duration = self.get_last_frame() / self.get_fps()
        self.change("update", ["duration"], new_duration)

    def create_group(self, group_id, timeables):
        """
        Create a TimeableGroup with all timeables in ids in it.
        The group will be added to the timeline model.

        @param ids: list of ids of timeable views
        @return: Nothing
        """
        self.groups[group_id] = TimeableGroup(group_id, timeables)
        project = Project.get_instance()
        if not project.changed:
            project.changed = True

    def get_last_frame(self):
        """ returns the number of the last frame in the timeline """
        last_frame = 0
        for c in self.timeline.Clips():
            clip_last_frame = c.Position() + c.Duration()
            if clip_last_frame > last_frame:
                last_frame = clip_last_frame

        last_frame = round(last_frame * self.timeline.info.fps.ToFloat()) + 1

        return last_frame

    def export(self, filename, audio_options, video_options, start_frame,
               last_frame, view):
        """
        Writes the video to the disk.

        @param filename: name of the file in which the video is saved
        @param audio_options: list of audio options
        @param video_options: list of video options
        @param last_frame: number of the last frame that's exported
        """
        self.timeline.Open()

        # create writer
        w = openshot.FFmpegWriter(filename)

        # set options
        w.SetAudioOptions(*audio_options)
        w.SetVideoOptions(*video_options)

        w.Open()

        bar = view.export_progress

        step = int((last_frame - start_frame) / 100)

        # export video
        for frame_number in range(start_frame, last_frame):
            if view.canceled:
                break

            QApplication.processEvents()
            w.WriteFrame(self.timeline.GetFrame(frame_number))
            if frame_number % step == 0:
                bar.setValue(bar.value() + 1)

        print("finished export")

        w.Close()

    def remove_track(self, number):
        """
        Removes all Clips with the same layer as numer.

        @param number: the Layer of the clips that will be removed
        """
        for c in self.timeline.Clips():
            if c.Layer() == number:
                self.change("delete", ["clips", {"id": c.Id()}], {})

    def remove_all_clips(self):
        """ Deletes all clips in the timeline (but not the views!!!) """
        for c in self.timeline.Clips():
            self.change("delete", ["clips", {"id": c.Id()}], {})
