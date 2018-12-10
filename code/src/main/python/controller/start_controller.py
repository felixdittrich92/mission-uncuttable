import sys

from controller import VideoEditorController
from view import VideoEditorView


class StartController:
    def __init__(self, view):
        self.startView = view
        self.startView.show()

        self.startView.pushButton.clicked.connect(self.openVideoEditor)

    def openVideoEditor(self):
        v = VideoEditorView()
        videoEditorController = VideoEditorController(v)


