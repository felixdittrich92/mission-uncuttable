import tkinter as tk
from tkinter import messagebox
from field import Field


class Window(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.field = Field(4)
        self.init_window()
        self.restart()

    def init_window(self):
        self.master.title("Programmieraufgabe")
        self.master.resizable(False, False)
        self.grid()

        restart_button = tk.Button(self, text="restart", command=self.restart)
        restart_button.grid(row=0, column=0, padx=5, pady=5)

        self.v = tk.IntVar()
        tk.Radiobutton(self, text="4x4", variable=self.v, value=4).grid(
            row=0, column=1)
        tk.Radiobutton(self, text="3x3", variable=self.v, value=3).grid(
            row=0, column=2)
        self.v.set(4)

    def window_pos(self):
        self.update_idletasks()
        if self.v.get() == 3:
            width = 350
            height = 335
        else:
            width = 460
            height = 435

        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_field(self):
        self.window_pos()

        self.field.buttons = []

        for i in range(self.v.get()):
            for j in range(self.v.get()):
                neighbours = self.field.get_neighbours(i, j)
                neighbours.append(((i * self.v.get()) + (j + 1)) - 1)
                b = tk.Button(self, width=10, height=5, bg="white",
                              activebackground="white",
                              command=lambda c=neighbours:
                              self.change_colour(c))
                self.field.buttons.append(b)
                b.grid(row=i+1, column=j)

    def change_colour(self, indexes):
        for ind in indexes:
            if self.field.buttons[ind].cget("bg") == "black":
                self.field.buttons[ind].configure(bg="white",
                                                  activebackground="white")
            else:
                self.field.buttons[ind].configure(bg="black",
                                                  activebackground="black")

        if self.field.is_won():
            messagebox.showinfo(message="Glückwunsch, du hast gewonnen")
            self.restart()

    def restart(self):
        for b in self.field.buttons:
            b.destroy()

        self.field = Field(self.v.get())
        self.create_field()
