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

        self.timeline_controller.create_track(name, 0)

        self.view.accept()
