from .connectable_scroll_area import ConnectableScrollArea
from PyQt5.QtCore import pyqtSlot


class ContentAdjustableConnectableScrollArea(ConnectableScrollArea):
    """
    Todo doc
    """

    def __init__(self, parent=None):
        super(ContentAdjustableConnectableScrollArea, self).__init__(parent)
        self.__adjusting_to_width = False
        self.__adjusting_to_height = False

    def set_adjusting_to_width(self, b):
        if b and not self.__adjusting_to_width:
            self.widget().width_changed.connect(self.__adjust_to_width)
            self.__adjust_to_width(self.widget().width())
            self.__adjusting_to_width = True
        elif not b and self.__adjusting_to_width:
            self.widget().width_changed.disconnect(self.__adjust_to_width)
            self.__adjusting_to_width = False

    def set_adjusting_to_height(self, b):
        if b and not self.__adjusting_to_height:
            self.widget().height_changed.connect(self.__adjust_to_height)
            self.__adjust_to_height(self.widget().height())
            self.__adjusting_to_height = True
        elif not b and self.__adjusting_to_height:
            self.widget().height_changed.disconnect(self.__adjust_to_height)
            self.__adjusting_to_height = False

    @pyqtSlot(int)
    def __adjust_to_width(self, width):
        widget_border_width = self.width() - self.viewport().width()
        self.setFixedWidth(width + widget_border_width)\

    @pyqtSlot(int)
    def __adjust_to_height(self, height):
        widget_border_height = self.height() - self.viewport().height()
        self.setFixedHeight(height + widget_border_height)