from GUI import Window

class GriddedWindow(Window):
    def __init__(self, **kwds):
        Window.__init__(self, **kwds)
        self.__set_to_initial_state()

    def __set_to_initial_state(self):
        self.__items = []
        self.__col_widths = []
        self.__row_heights = []
        self.__inner_sep = 0
        self.__col_seps = []
        self.__row_seps = []

    def reset_everything(self):
        self.__reset_items()
        self.__set_to_initial_state()
        self.__refresh_placements()

    def __reset_items(self):
        # Bugfix: without the loop there can be components remaining for
        # some reason
        while self.contents:
            self.remove(self.contents)
        self.__items = []

    def get_items(self):
        return self.__items

    def place_item(self, item, row, col):
        num_of_rows = len(self.__items)
        if num_of_rows <= row:
            for i in range(row-num_of_rows+1):
                self.__items.append([])
        num_of_cols = len(self.__items[row])
        if num_of_cols <= col:
            self.__items[row].extend([None]*(col-num_of_cols+1))
        self.__items[row][col] = item
        self.__refresh_placements()

    def set_col_seps(self, seps):
        self.__col_seps = seps
        self.__refresh_placements()

    def set_row_seps(self, seps):
        self.__row_seps = seps
        self.__refresh_placements()

    def set_inner_sep(self, sep):
        self.__inner_sep = sep
        self.__refresh_placements()

    def __refresh_placements(self):
        self.__calc_col_widths()
        self.__calc_row_heights()

        self.__remove_unused_items()

        y = self.__inner_sep
        for row_index in range(len(self.__items)):
            x = self.__inner_sep
            for col_index in range(len(self.__items[row_index])):
                item = self.__items[row_index][col_index]
                if item:
                    self.place(item, left=x, top=y)
                x += self.__col_widths[col_index]
                if len(self.__col_seps) > col_index:
                    x += self.__col_seps[col_index]
            y += self.__row_heights[row_index]
            if len(self.__row_seps) > row_index:
                y += self.__row_seps[row_index]

        self.shrink_wrap()

    def __calc_row_heights(self):
        self.__row_heights = []
        for row in self.__items:
            max_height = 0
            for item in row:
                if item:
                    if item.get_height() > max_height:
                        max_height = item.get_height()
            self.__row_heights.append(max_height)

    def __calc_col_widths(self):
        self.__col_widths = []
        for row in self.__items:
            while len(row) > len(self.__col_widths):
                self.__col_widths.append(0)
            for i in range(len(row)):
                if row[i]:
                    if self.__col_widths[i] < row[i].get_width():
                        self.__col_widths[i] = row[i].get_width()

    def __remove_unused_items(self):
        all_items = []
        for row in self.__items:
            all_items.extend(row)
        for c in self.contents:
            if c not in all_items:
                # Bug fix. The loop ensures that c gets removed
                while c in self.contents:
                    self.remove(c)
