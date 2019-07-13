from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QAction, QMenu, QApplication
from PyQt5.QtCore import QDataStream, Qt, QIODevice, QRectF, QPoint

from .add_track_view import AddTrackView
from model.project import Project
from controller import TimelineController, AddTrackController
from config import Language, Resources, Settings


class TrackView(QGraphicsView):
    """
    A View for a single Track, which can be added to the TrackFrame in the Timeline along
    with other TrackViews. The TrackView can hold Timeables.
    """

    def __init__(self, track_id, width, height, layer,
                 name, button, is_video, is_overlay=False, parent=None):
        """
        Creates TrackView with fixed width and height. The width and height should be
        the same for all TrackViews.

        @param track_id:
        @param width: track width
        @param height: track height
        @param layer: the layer of the track, clips in tracks with
                    higher numbers get rendered above others
        """
        super(TrackView, self).__init__(parent)

        self.__track_id = track_id
        self.width = width
        self.height = height
        self.layer = layer
        self.name = name
        self.button = button

        # Change note: Before, this has been the only place where the
        # overlay property had been stored. This information now was
        # moved to the model. This object variable remains here to give
        # give the opportunity to optically mark the track as overlay in
        # the view. But it has no effect on the model's data anymore.
        self.is_overlay = is_overlay

        self.is_video = is_video

        # set button context menu policy so you can get a rightclick menu on the button
        self.button.setContextMenuPolicy(Qt.CustomContextMenu)
        self.button.customContextMenuRequested.connect(self.on_context_menu)

        # for drag and drop handling
        self.item_dropped = False
        self.current_timeable = None
        self.drag_from_track = False
        self.dragged_timeable_id = None

        self.__timeline_controller = TimelineController.get_instance()

        self.setAcceptDrops(True)

        self.setup_ui()

    def setup_ui(self):
        """ sets up the trackview """
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setScene(QGraphicsScene())

        self.resize()

    def get_info_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "num": self.layer,
            "name": self.name,
            "is_overlay": self.is_overlay,
            "type": self.is_video,
        }

    def on_context_menu(self, point):
        """ shows a menu on rightclick """
        button_menu = QMenu()
        current_stylesheet = Settings.get_instance().get_settings().design.color_theme.current
        if current_stylesheet == 0:
            button_menu.setStyleSheet(open(Resources.files.qss_dark, "r").read())     
        elif current_stylesheet == 1:
            button_menu.setStyleSheet(open(Resources.files.qss_light, "r").read())

        delete = QAction(str(Language.current.track.delete))
        button_menu.addAction(delete)
        delete.triggered.connect(self.delete)

        add = QAction(str(Language.current.track.add))
        button_menu.addAction(add)
        add.triggered.connect(self.add)

        if self.is_video:
            overlay = QAction(str(Language.current.track.overlay))
            overlay.setCheckable(True)
            if self.is_overlay:
                overlay.setChecked(True)

            button_menu.addAction(overlay)
            overlay.toggled.connect(self.handle_overlay_toggle)

        button_menu.exec_(self.button.mapToGlobal(point) + QPoint(10, 0))

    def add(self):
        """
        Calls the TimelineController to add a track
        This method is only for the context menu on the track button
        """
        view = AddTrackView()
        AddTrackController(self.__timeline_controller, view).start()

    def delete(self):
        """
        Calls the TimelineController to removes this track.
        This method is only for the context menu on the track button
        """
        self.__timeline_controller.delete_track(self.__track_id)

    def handle_overlay_toggle(self, checked):
        """ Slot for the toggle of the overlay checkbox.
        @param checked: The state of the checkbox.
        """
        self.__timeline_controller\
            .set_track_overlay(self.__track_id, checked)

        # Todo: Find out if this code line is needed and if yes what
        #  it's there for. Maybe it can be removed?
        QApplication.processEvents()

    def wheelEvent(self, event):
        """ Overrides wheelEvent from QGraphicsView to prevent scrolling in a track """
        pass

    def keyPressEvent(self, event):
        """
        Overrides wheelEvent from QGraphicsView to prevent scrolling in a
        track. If a keyPressEvent should occur it needs to be explicitly
        handled here.

        :param event: Event
        """
        pass

    def resize(self):
        """ sets the size of the trackview to self.width and self.height """
        self.scene().setSceneRect(0, 0, self.width, self.height)
        self.setFixedSize(self.width, self.height)

    def set_width(self, new_width):
        """
        Changes the width of the trackview.

        @param new_width: the new width of the track
        """
        self.width = new_width
        self.resize()
        # Todo: This line seems to handle semantic information. This
        #  should happen through the controller.
        #  The width of a TrackView can't be a measurement for how long
        #  the video is because later there will be zooming in the
        #  timeline and also there could be special inconsistencies to
        #  the model because of graphical optimization of the timeline
        #  view's picture. So it's a little bold to update the player
        #  only because the view changed.
        self.update_player()

    # Todo: Find out if the player update is really needed inside this
    #  method and if it is not remove it.
    def add_timeable(self, timeable):
        """ Adds a TimeableView to the GraphicsScene """
        self.scene().addItem(timeable)
        self.update_player()

    def add_from_filemanager(self, drag_event):
        """ Adds a timeable when item from filemanager is dragged into the track """
        # get the path from the dropped item
        item_data = drag_event.mimeData().data('ubicut/file')
        stream = QDataStream(item_data, QIODevice.ReadOnly)
        path = QDataStream.readString(stream).decode()
        # width = QDataStream.readInt(stream)

        x_pos = drag_event.pos().x()

        # Change note: Collision checking is left out completely for
        #  now. This should happen using the model and the controller.
        # check if theres already another timeable at the drop position
        # rect = QRectF(x_pos, 0, width, self.height)
        # colliding = self.scene().items(rect)
        # add the timeable when there are no colliding items

        # This is one line of the code needed for collision checking or
        #  similar things. For now, we directly add the timeable to the
        #  timeline
        # self.__timeline_controller.create_preview_timeable(path, "timeable")

        self.current_timeable = self.__timeline_controller\
            .create_timeable(
                path,
                self.__track_id,
                "timeable",
                x_pos)

        # model = TimeableModel(path, generate_id(), is_video=True)
        # model_withoutgroup = TimeableModel(path, generate_id())
        # model_audio = TimeableModel(path, generate_id(), is_video=False)
        # model.move(x_pos)
        # model.set_end(width)
        # name = os.path.basename(path)
        #
        # clip_id = generate_id()
        # clip_id_audio = generate_id()
        #
        #
        #
        # if Settings.get_instance().get_dict_settings()["general"]["autoaudio"]["current"]:
        #     self.__controller.create_timeable(None, self.layer, name, x_pos)
        #     self.__controller.create_timeable(None, None, name, x_pos)
        #     self.__controller.create_group([clip_id, clip_id_audio])
        # else:
        #     self.__controller.create_timeable(None, self.layer, name, x_pos)

        self.item_dropped = True

    def add_from_track(self, drag_event):
        """ Adds a timeable when a drag was started from a timeable on a track """
        # get the data thats needed to check for collisions
        item_data = drag_event.mimeData().data('ubicut/timeable')
        stream = QDataStream(item_data, QIODevice.ReadOnly)

        view_id = QDataStream.readString(stream).decode()
        self.current_timeable = self.__timeline_controller\
            .get_timeable_by_id(view_id)

        pos = self.current_timeable.mouse_press_pos
        start_pos = drag_event.pos().x()

        self.__timeline_controller\
            .move_timeable(view_id, self.__track_id, start_pos - pos)

        # self.dragged_timeable_id = view_id
        #
        # name = timeable.name
        # width = timeable.width
        # group_id = timeable.group_id
        #
        # # get a list of items at the position where the timeable would be added
        # if start_pos < pos:
        #     return
        #
        # rect = QRectF(start_pos - pos, 0, width, self.height)
        # colliding = [item for item in self.scene().items(rect)
        #              if item.isVisible]
        #
        # # only add the timeable if colliding is empty
        # if not colliding:
        #     res_left = timeable.resizable_left
        #     res_right = timeable.resizable_right
        #     file_name = timeable.model.file_name
        #     old_pos = timeable.x_pos
        #
        #     # create new timeable
        #     model = TimeableModel(generate_id(), file_name, is_video=timeable.model.is_video)
        #
        #     old_clip = timeable.model.clip
        #
        #     # adjust the new model
        #     model.set_start(old_clip.Start(), is_sec=True)
        #     model.set_end(old_clip.End(), is_sec=True)
        #     model.move(start_pos - pos)
        #
        #     new_id = generate_id()
        #
        #     # add the timeable to the track
        #     self.__timeline_controller.create_timeable(None, self.layer, name, 50, start_pos,,,
        #     self.drag_from_track = True
        #
        #     if group_id is not None:
        #         new_pos = -(old_pos - (start_pos - pos))
        #         self.__timeline_controller.remove_timeable_from_group(group_id, view_id)
        #         self.__timeline_controller.try_group_move(group_id, new_pos)
        #         self.__timeline_controller.add_timeable_to_group(group_id, new_id)
        #

        # set item_dropped to True because the timeable was succesfully created
        self.item_dropped = True

        self.update_player()

    def move_dropped_timeable(self, event):
        pos = event.pos().x() - self.current_timeable.mouse_press_pos
        self.current_timeable.move_on_track(pos)

    def dragEnterEvent(self, event):
        """ Gets called when something is dragged into the track """
        if event.mimeData().hasFormat('ubicut/timeable'):
            if self.is_video:
                if event.mimeData().text() == "is_video":
                    # try to add a timeable
                    self.add_from_track(event)
                    event.accept()
                else:
                    event.ignore()
            else:
                if event.mimeData().text() == "is_audio":
                    self.add_from_track(event)
                    event.accept()
                else:
                    event.ignore()

        elif event.mimeData().hasFormat('ubicut/file'):
            # try to add a timeable
            self.add_from_filemanager(event)

            event.accept()
        else:
            event.ignore()
        self.update_player()

    def dragLeaveEvent(self, event):
        """ Gets called when something is dragged out of the track """
        if self.current_timeable is not None:
            if event.mimeData().hasFormat('ubicut/file'):
                # delete dragged timeable if mouse leaves track
                self.current_timeable.delete(hist=False)
                Project.get_instance().get_history().remove_last_operation()

            # clear data
            self.item_dropped = False
            self.current_timeable = None

            event.ignore()

        self.update()
        event.accept()
        self.update_player()

    def dragMoveEvent(self, event):
        """ Gets called when there is an active drag and the mouse gets moved """
        if event.mimeData().hasFormat('ubicut/timeable'):
            # move the timeable if it was created
            if self.item_dropped:
                self.move_dropped_timeable(event)
                event.accept()
                return

            # try to add the timeable if it wasn't added before
            self.add_from_track(event)
            event.accept()
        elif event.mimeData().hasFormat('ubicut/file'):
            # move the timeable if it was created
            if self.item_dropped:
                self.move_dropped_timeable(event)
                event.accept()
                return

            # try to add the timeable if it wasn't added before
            self.add_from_filemanager(event)
            event.accept()
        else:
            event.ignore()
        self.update_player()

    def dropEvent(self, event):
        """ Gets called when there is an active drag and the mouse gets released """
        if event.mimeData().hasFormat('ubicut/timeable')\
                or event.mimeData().hasFormat('ubicut/file'):
            # accept MoveAction if timeable was succesfully created
            if self.current_timeable is not None:
                self.__timeline_controller.move_timeable(
                    self.current_timeable.view_id,
                    self.__track_id,
                    self.current_timeable.x_pos
                )
                # self.current_timeable.model.move(self.current_timeable.x_pos)
                self.current_timeable = None

                event.acceptProposedAction()

            # set item_dropped to false for next drag
            self.item_dropped = False
            self.update()
        else:
            event.ignore()

        self.update_player()

    def update_player(self):
        # self.parent().parent().parent().parent().parent().parent().parent().parent().connect_update()
        pass
