import sys

class GridGameModel:
    '''
    Describes a grid of boolean values for a game where the challenge is
    to switch the color of all boxes from white to black. If one box is
    changed the adjacent boxes are changed too automatically.
    '''

    def __init__(self, width, height):
        '''
        Initialises a GridModel with the given width and height, which
        all boxes of are filled with False.
        '''

        self.__width = width
        self.__height = height
        self.__grid = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(False)
            self.__grid.append(row)
        self.__observer_list = []


    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_grid(self):
        return self.__grid

    def print_grid(self):
        print('+' + '--' * self.__width + '+')  ## horizontal borderline

        ## content ('#' where True, ' ' where False):
        for row in self.__grid:
            out = ""
            for el in row:
                if el:
                    out += ' #'
                else:
                    out += '  '
            print('|' + out + '|')    ## with leading and trailing vertical
                                      ## borderlines

        print('+' + '--' * self.__width + '+')  ## borderline

    def add_grid_game_model_observer(self, grid_model_observer):
        self.__observer_list.append(grid_model_observer)

    def __notify_observers_grid_changed(self):
        for grid_model_observer in self.__observer_list:
            grid_model_observer.grid_changed()

    def trigger(self,x,y):
        self.__toggle(x,y)
        for coordinate in [(x,y-1), (x-1,y), (x+1,y), (x,y+1)]:
            if (coordinate[0] in range(self.__width)
                    and coordinate[1] in range(self.__height)):
                self.__toggle(coordinate[0], coordinate[1])
        self.__notify_observers_grid_changed()

    def __toggle(self,x,y):
        if self.__grid[y][x]:
            self.__grid[y][x] = False
        else:
            self.__grid[y][x] = True
