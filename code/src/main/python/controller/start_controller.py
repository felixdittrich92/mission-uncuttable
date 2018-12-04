class StartController:
    def __init__(self, view):
        self.startView = view
        self.startView.show()
        self.startView.pushButton.clicked.connect(self.startVideoEditor)

    def startVideoEditor(self):
        self.mainview = view
        self.mainview.showVideoEditor
        print("sdas")
