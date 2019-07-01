from PyQt5.QtWidgets import QVBoxLayout, QApplication
from .size_linkable_frame import SizeLinkableFrame


class TrackButtonFrame(SizeLinkableFrame):
    """
    Extends SizeLinkableFrame to a frame which is mainly intended to
    display TrackButtons.

    The TrackButtonFrame has the size-linkable property. For information
    on how to use this see the SizeLinkableFrame class.
    """

    def __init__(self, parent=None):
        """
        Create an empty TrackButtonFrame without any size linkage.

        :param parent: the parent component
        """
        super(TrackButtonFrame, self).__init__(parent)

        self.button_counter = 0
        box_layout = QVBoxLayout()
        box_layout.setSpacing(0)
        box_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(box_layout)

        # self.setStyleSheet('background-color: orange')

    def add_button(self, button, type, index):
        """
        Adds a new Button to the TrackButtonFrame

        @param button: the button to add
        """
        if type:
            self.button_counter += 1
            if self.button_counter % 2 == 1:
                button.setObjectName('track_button')
            else:
                button.setObjectName('track_button_light')
        else:
            button.setObjectName('track_button_audio')

        self.layout().insertWidget(index, button)
        self.adjustSize()
        QApplication.processEvents()
        self.parent().adjustSize()

    def remove_button(self, button):
        """
        Removes a button from the TrackButtonFrame

        @param button: the button to remove
        """
        self.layout().removeWidget(button)
        button.deleteLater()
        self.adjustSize()
        QApplication.processEvents()
        self.parent().adjustSize()
