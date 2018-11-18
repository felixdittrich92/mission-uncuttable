from tkinter import *

"""
Verbesserungsvorschläge:
- mehrere Klassen verwenden
- nur eine Klasse pro Datei (außer private Klassen)
- Trennung von Datenmodell, Logik und Darstellung
- Statt 1 und 2 als Werte zu benutzen eignen sich Booleans
  diese können auch einfacher invertiert werden (not)
- Methodennamen sollten noch eindeutiger bzw. ausdrücklicher sein
"""

# constanten groß und oben zu schreiben ist gut
WINDOW_SIZE = 600  # pixels
GRID_LINE_WIDTH = 2  # pixels

SYMBOL_SIZE = 0.99

GRID_COLOR = 'light grey'


class Game(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.won = 0
        self.fields = 3
        self.cell_size = WINDOW_SIZE / self.fields
        self.newCanvas()

        self.button = Button(self,
                             text="3x3", fg="black",
                             command=self._3x3)
        self.button.pack(side=LEFT)

        self.button = Button(self,
                             text="4x4", fg="black",
                             command=self._4x4)
        self.button.pack(side=LEFT)

        self.button = Button(self,
                             text="5x5", fg="black",
                             command=self._5x5)
        self.button.pack(side=LEFT)

        self.button = Button(self,
                             text="restart", fg="black",
                             command=self.restart)
        self.button.pack(side=RIGHT)

    def _3x3(self):
        self.fields = 3
        self.new_board()

    def _4x4(self):
        self.fields = 4
        self.new_board()

    def _5x5(self):
        self.fields = 5
        self.new_board()

    def restart(self):
        self.new_board()

    def newCanvas(self):
        self.canvas = Canvas(
            height=WINDOW_SIZE, width=WINDOW_SIZE,
            bg='white')

        self.canvas.pack()

        self.bind('<x>', self.exit)
        self.canvas.bind('<Button-1>', self.click)

        self.new_board()

    def new_board(self):

        self.canvas.delete('all')
        self.cell_size = WINDOW_SIZE / self.fields

        if self.fields == 3:
            self.board = [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]]
        elif self.fields == 4:
            self.board = [
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1],
                [1, 1, 1, 1]]
        elif self.fields == 5:
            self.board = [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1]]

        # draw grid
        for n in range(1, self.fields):
            # vertical
            self.canvas.create_line(
                self.cell_size * n, 0,
                self.cell_size * n, WINDOW_SIZE,
                width=GRID_LINE_WIDTH, fill=GRID_COLOR)
            # horizontal
            self.canvas.create_line(
                0, self.cell_size * n,
                WINDOW_SIZE, self.cell_size * n,
                width=GRID_LINE_WIDTH, fill=GRID_COLOR)

    def drawAll(self):
        win = 1;
        for x in range(0, self.fields):
            for y in range(0, self.fields):
                if self.board[x][y] == 1:
                    self.draw(x, y, 'white')
                    win = 0
                else:
                    self.draw(x, y, 'black')
        if win == 1:
            self.has_won()

    def has_won(self):
        self.won = 1
        self.canvas.create_rectangle(
           20,20,
            WINDOW_SIZE-20, WINDOW_SIZE-20,
            fill='white', outline='white')
        self.canvas.create_text(
            int(WINDOW_SIZE/2), int(WINDOW_SIZE/2),
            text='Gewonnen!', fill='black',
            font=('Franklin Gothic', int(-WINDOW_SIZE/6), 'bold'))
        self.canvas.create_text(
            int(WINDOW_SIZE / 1.95), int(WINDOW_SIZE / 1.3),
            text='Klicke um neu \n zu starten!', fill='black',
            font=('Franklin Gothic', int(-WINDOW_SIZE / 30)))


    # ----------------------------------------------------------------------------------------
    def click(self, event):

        x = self.ptgrid(event.x)
        y = self.ptgrid(event.y)

        if self.won == 1:
            self.new_board()
            self.won = 0
        else:
            self.new_move(x, y)

        self.drawAll()

    def new_move(self, grid_x, grid_y):

        self.flip(grid_x, grid_y)

        if grid_x + 1 <= self.fields-1:
            self.flip(grid_x+1, grid_y)
        if grid_x - 1 >= 0:
            self.flip(grid_x - 1, grid_y)
        if grid_y + 1 <= self.fields-1:
            self.flip(grid_x, grid_y + 1)
        if grid_y - 1 >= 0:
            self.flip(grid_x, grid_y - 1)

    def draw(self, grid_x, grid_y, color):
        """
        draw the X symbol at x, y in the grid
        """

        x = self.gtpix(grid_x)
        y = self.gtpix(grid_y)
        delta = self.cell_size / 2 * SYMBOL_SIZE

        self.canvas.create_rectangle(
            x - delta, y - delta,
            x + delta, y + delta,
            fill=color, outline='white')

    def flip(self, x, y):
        if self.board[x][y] == 1:
            self.board[x][y] = 2
        elif self.board[x][y] == 2:
            self.board[x][y] = 1

    def gtpix(self, grid_coord):

        pixel_coord = grid_coord * self.cell_size + self.cell_size / 2
        return pixel_coord

    def ptgrid(self, pixel_coord):

        if pixel_coord >= WINDOW_SIZE:
            pixel_coord = WINDOW_SIZE - 1

        grid_coord = int(pixel_coord / self.cell_size)
        return grid_coord

    def exit(self, event):
        self.destroy()


def main():
    root = Game()
    root.mainloop()


main()
