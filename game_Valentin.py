from tkinter import Tk, Button, messagebox

class Board:

    size = 4

    def __init__(self, size):
        self.size=size
        self.empty = ''
        print(size)
        self.fields = {}
        for y in range(size):
            for x in range(size):
                self.fields[x, y] = self.empty

class GUI:

    def __init__(self, size):
        self.app = Tk()
        self.app.title('Spiel')
        self.app.resizable(width=False, height=False)
        self.board = Board(size)
        self.buttons = {}
        for x, y in self.board.fields:
            handler = lambda x=x, y=y: self.move(x, y)
            button = Button(self.app, command=handler, bg='white', fg="white", width=10, height=5)
            button.grid(row=y, column=x)
            self.buttons[x, y] = button
        handler = lambda: self.reset()
        handler2 = lambda: self.three()
        handler3 = lambda: self.four()
        button = Button(self.app, text='reset', command=handler, bg='coral')
        button.grid(row=self.board.size + 1, column=2, sticky="WE")
        button2 = Button(self.app, text='3x3', command=handler2, bg='light grey')
        button2.grid(row=self.board.size + 1, column=0, sticky="WE")
        button3 = Button(self.app, text='4x4', command=handler3, bg='light grey')
        button3.grid(row=self.board.size + 1, column=1, sticky="WE")
        self.update()

    def three(self):
        if self.board.size == 4:
            self.app.destroy()
            self.gui = GUI(3)
        else:
            return None

    def four(self):
        if self.board.size == 3:
            self.app.destroy()
            self.gui = GUI(4)
        else:
            return None

    def reset(self):
        for x in range(self.board.size):
            for y in range(self.board.size):
                self.buttons[x, y]['bg'] = 'white'

    def winning(self):
        i = 0
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.buttons[x, y].cget('bg') == 'black':
                    i = i +1
                else:
                    break
        if i == ((self.board.size)*(self.board.size)):
            messagebox.showinfo("Spielstatus", "Sie haben gewonnen.")
            self.reset()
        else:
            return None

    def move(self, x, y):
       if self.buttons[x, y].cget('bg') == 'white':
          self.buttons[x, y]['bg'] = 'black'
          self.movearound(x+1, y)
          self.movearound(x-1, y)
          self.movearound(x, y+1)
          self.movearound(x, y-1)

       elif self.buttons[x, y].cget('bg') == 'black':
           self.buttons[x, y]['bg'] = 'white'
           self.movearound(x+1, y)
           self.movearound(x-1, y)
           self.movearound(x, y+1)
           self.movearound(x, y-1)
       self.winning()

    def movearound(self, x, y):
      if (x<self.board.size and x>=0) and (y<self.board.size and y>=0):
          if self.buttons[x, y].cget('bg') == 'white':
              self.buttons[x, y]['bg'] = 'black'
          elif self.buttons[x, y].cget('bg') == 'black':
              self.buttons[x, y]['bg'] = 'white'
      else:
          return None

    def update(self):
        for (x, y) in self.board.fields:
          self.buttons[x, y].update()

    def mainloop(self):
      self.app.mainloop()

if __name__ == '__main__':
  GUI(3).mainloop()
