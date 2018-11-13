import grid_game_model


class ToggleButtonObserver:
    def __init__(self, model, pos_x, pos_y):
        self.__model = model
        self.__pos_x = pos_x
        self.__pos_y = pos_y

    def action_performed(self):
        self.__model.trigger(self.__pos_x, self.__pos_y)

class GridModelObserver:
    def __init__(self, gui):
        self.__gui = gui

    def grid_changed(self):
        self.__gui.refresh()
