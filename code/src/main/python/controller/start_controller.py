class StartController:
    def __init__(self, view):
        self.start_view = view
        self.start_view.show()
        self.start_view.MainWindow.start_frame.new_project_button.clicked.connect(self.test_button)

    def test_button(self):
        print("dsfsdf")
