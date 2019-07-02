class AddTrackController:
    """ Controller for adding a new Track """

    def __init__(self, timeline_controller, view):
        self.timeline_controller = timeline_controller
        self.view = view

        self.view.add_button.clicked.connect(self.create_track)

    def start(self):
        self.view.exec_()

    def create_track(self):
        name = self.view.name_edit.text()

        is_video = True
        if self.view.audio_button.isChecked():
            is_video = False

        self.timeline_controller.add_track(name, 1, 50, 0, is_video)

        self.view.accept()
