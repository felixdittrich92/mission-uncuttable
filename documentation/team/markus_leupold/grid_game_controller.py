import grid_game_model


class ToggleButtonObserver:
    def __init__(self, grid_model, pos_x, pos_y):
        self.__grid_model = grid_model
        self.__pos_x = pos_x
        self.__pos_y = pos_y

    def action_performed(self):
        self.__grid_model.trigger(self.__pos_x, self.__pos_y)

class GridModelObserver:
    def __init__(self, grid_gui):
        self.__grid_gui = grid_gui

    def grid_changed(self):
        self.__grid_gui.refresh()
