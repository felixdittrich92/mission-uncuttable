import tkinter as tk
import grid_game_model
import grid_game_controller
import sys


class GridGui(tk.Frame):
    def __init__(self, grid_model, master=None):
        tk.Frame.__init__(self, master)
        self.__grid_model = grid_model

        ## adding an observer for getting information about model changes:
        self.__grid_model.add_grid_model_observer(
            grid_controller.GridModelObserver(self)
        )

        ## adding a grid of buttons to the gui:
        self.__buttons = []
        for y in range(self.__grid_model.get_height()):
            row = []
            for x in range(self.__grid_model.get_width()):
                b = tk.Button(self, width='10', height='4', bg='black')
                ## every button gets a function object of a unique instance of
                ## ToggleButtonObserver to make every button toggle its own
                ## position in the grid:
                o = grid_controller.ToggleButtonObserver(
                    self.__grid_model, x, y
                )
                b.configure(command=o.action_performed)
                row.append(b)
                b.grid(column=str(x), row=str(y))
            self.__buttons.append(row)

        ## finally gridding the gui:
        self.grid()

    def refresh(self):
        for y in range(self.__grid_model.get_height()):
            for x in range(self.__grid_model.get_width()):
                if self.__grid_model.get_grid()[y][x]:
                    self.__buttons[y][x].configure(bg='white')
                else:
                    self.__buttons[y][x].configure(bg='black')
