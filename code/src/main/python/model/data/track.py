# Todo: Implement change of the TimelineModel to which a TrackModel eventually
#  belongs if the TrackModel changes.


class TrackModel:
    """
    Representation of a track in a timeline. This class provides easier
    and more flexible handling of the Openshot layers.
    """

    def __init__(self, track_id, name="Track"):
        """
        Create a C{TrackModel} with the given ID which contains no
        timeables and has no layer specified.

        @param track_id: The ID which the C{TrackModel} should have.
        """
        self.__track_id = track_id
        self.__name = name

        self.__layer = None
        self.__timeables = dict()  # {timeable_id: timeable}

        self.__timeline_model = None
        self.__timeline_controller = None

    def get_track_id(self):
        """ Return the id of the C{TrackModel}.

        @return: The track id.
        """
        return self.__track_id

    def get_name(self):
        """ Return the name.

        @return: The track name.
        @rtype:  str
        """
        return self.__name

    def set_name(self, name):
        """ Set the name of the C{TrackModel}

        @param name: The new name.
        @type name:  str
        """
        self.__name = name

    def add_timeable(self, timeable):
        """ Add a C{TimeableModel} to the C{TrackModel}.

        @param timeable: The timeable which should be added.
        @type timeable:  model.data.TimeableModel
        @raise ValueError: If the C{TrackModel} already contains a
                           timeable with the same ID as the timeable to
                           be added.
        """
        timeable_id = timeable.get_id()
        if timeable_id in self.__timeables.keys():
            raise ValueError(
                "There's already a timeable existing in this track "
                "with ID = {}"
                .format(timeable_id)
            )
        else:
            self.__timeables[timeable_id] = timeable
            timeable.set_track(self)
            if self.__timeline_model is not None:
                self.__timeline_model.timeline.addClip(timeable.clip)
            if self.__timeline_controller is not None:
                self.__timeline_controller.timeable_added(timeable)

    def remove_timeable(self, timeable_id):
        """ Remove a timeable from the C{TrackModel}.

        @param timeable_id: The ID of the timeable to be removed.
        @raise KeyError:    If the C{TrackModel} doesn't contain the
                            specified timeable.
        """
        try:
            t = self.__timeables[id]
        except KeyError:
            raise KeyError(
                "Timeable doesn't exist in this track: ID = {}"
                .format(timeable_id)
            )
        finally:
            t.set_track(None)
            self.__timeables.pop(timeable_id)
            if self.__timeline_model is not None:
                self.__timeline_model\
                    .change("delete", ["clips", {"id": t.clip.Id()}], {})
            if self.__timeline_controller is not None:
                self.__timeline_controller.timeable_removed(timeable_id)

    def remove_all_timeables(self):
        """ Remove all timeables from the C{TrackModel}. """
        for timeable_id in self.__timeables.keys():
            self.remove_timeable(timeable_id)

    def get_layer(self):
        """ Return the layer of the C{TrackModel}.

        @return: The layer.
        """
        return self.__layer

    def set_layer(self, layer):
        """ Set the layer of the C{TrackModel}.

        @param layer: The new layer.
        @type layer:  int
        """
        self.__layer = layer
        for t in self.__timeables.values():
            t.set_layer(self.__layer)

    def set_timeline_model(self, model):
        """ Set the timeline model of the C{TrackModel}

        @param model: The timeline model.
        @type model:  model.data.TimelineModel
        """
        self.__timeline_model = model


class VideoTrack(TrackModel):
    def __init__(self, track_id):
        super(VideoTrack, self).__init__(track_id)

    def add_timeable(self, timeable):
        """ Add a C{TimeableModel} to the C{TrackModel}.

        @param timeable:   The timeable which should be added.
        @type timeable:    model.data.TimeableModel
        @raise ValueError: If the C{TrackModel} already contains a
                           timeable with the same ID as the timeable to
                           be added or if the specified timeable is not
                           a video timeable.
        """
        if not timeable.is_video:
            raise ValueError(
                "This timeable is not a video timeable: {}"
                .format(timeable.get_id())
            )
        else:
            super(VideoTrack, self).add_timeable(timeable)


class AudioTrack(TrackModel):
    def __init__(self, track_id):
        super(AudioTrack, self).__init__(track_id)

    def add_timeable(self, timeable):
        """ Add a C{TimeableModel} to the C{TrackModel}.

        @param timeable:   The timeable which should be added.
        @type timeable:    model.data.TimeableModel
        @raise ValueError: If the C{TrackModel} already contains a
                           timeable with the same ID as the timeable to
                           be added or if the specified timeable is not
                           an audio timeable.
        """
        if timeable.is_video is not False:
            raise ValueError(
                "This timeable is not an audio timeable: {}"
                .format(timeable.get_id())
            )
        else:
            super(AudioTrack, self).add_timeable(timeable)
