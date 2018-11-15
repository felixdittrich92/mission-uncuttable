from tkinter import *
from tkinter import messagebox


def selectgamesize():
    gamesize = IntVar ()
    Label (mainwin, text="Choose a size:").pack ()
    Radiobutton (mainwin, text="3 x 3", padx=20, variable=gamesize, value=3).pack (anchor=W)
    Radiobutton (mainwin, text="4 x 4", padx=20, variable=gamesize, value=4).pack (anchor=W)

    gamestartbutton = Button (mainwin, text="Start new game", fg='black',
                              command=lambda: newgamewin (gamesize.get()))
    gamestartbutton.pack ()


def newgamewin(size):
    gamesize = size
    gamewin = Toplevel (mainwin)


    global button1
    global button2
    global button3
    global button4
    global button5
    global button6
    global button7
    global button8
    global button9
    global button10
    global button11
    global button12
    global button13
    global button14
    global button15
    global button16


    if gamesize == 3:


       
        button1 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button1.grid (row=0, column=0)
        button2 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button2.grid (row=0, column=1)
        button3 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button3.grid (row=0, column=2)
        button4 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button4.grid (row=1, column=0)
        button5 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button5.grid (row=1, column=1)
        button6 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button6.grid (row=1, column=2)
        button7 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button7.grid (row=2, column=0)
        button8 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button8.grid (row=2, column=1)
        button9 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button9.grid (row=2, column=2)

        button1.configure (
            command=lambda: (changecolor (button1), changecolor (button2), changecolor (button4), isgamefinished(gamesize)))
        button2.configure (
            command=lambda: (
            changecolor (button1), changecolor (button2), changecolor (button3), changecolor (button5), isgamefinished(gamesize)))
        button3.configure (
            command=lambda: (changecolor (button2), changecolor (button3), changecolor (button6), isgamefinished(gamesize)))
        button4.configure (
            command=lambda: (
            changecolor (button1), changecolor (button4), changecolor (button7), changecolor (button5), isgamefinished(gamesize)))
        button5.configure (
            command=lambda: (changecolor (button2), changecolor (button4), changecolor (button5), changecolor (button6),
                             changecolor (button8), isgamefinished(gamesize)))
        button6.configure (
            command=lambda: (
            changecolor (button3), changecolor (button5), changecolor (button6), changecolor (button9), isgamefinished(gamesize)))
        button7.configure (
            command=lambda: (changecolor (button4), changecolor (button7), changecolor (button8), isgamefinished(gamesize)))
        button8.configure (
            command=lambda: (
            changecolor (button5), changecolor (button7), changecolor (button8), changecolor (button9), isgamefinished(gamesize)))
        button9.configure (
            command=lambda: (changecolor (button6), changecolor (button8), changecolor (button9), isgamefinished(gamesize)))

    else:

        
        button1 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button1.grid (row=0, column=0)
        button2 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button2.grid (row=0, column=1)
        button3 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button3.grid (row=0, column=2)
        button4 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button4.grid (row=0, column=3)
        button5 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button5.grid (row=1, column=0)
        button6 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button6.grid (row=1, column=1)
        button7 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button7.grid (row=1, column=2)
        button8 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button8.grid (row=1, column=3)
        button9 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button9.grid (row=2, column=0)
        button10 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button10.grid (row=2, column=1)
        button11 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button11.grid (row=2, column=2)
        button12 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button12.grid (row=2, column=3)
        button13 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button13.grid (row=3, column=0)
        button14 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button14.grid (row=3, column=1)
        button15 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button15.grid (row=3, column=2)
        button16 = Button (gamewin, fg='white', bg='white', text='X', padx=17, pady=10)
        button16.grid (row=3, column=3)

        button1.configure (
            command=lambda: (
                changecolor (button1),
                changecolor (button2),
                changecolor (button5), isgamefinished(gamesize)))
        button2.configure (
            command=lambda: (
                changecolor (button1),
                changecolor (button2),
                changecolor (button3),
                changecolor (button6), isgamefinished(gamesize)))
        button3.configure (
            command=lambda: (
                changecolor (button2),
                changecolor (button3),
                changecolor (button4),
                changecolor (button7), isgamefinished(gamesize)))
        button4.configure (
            command=lambda: (
                changecolor (button3),
                changecolor (button4),
                changecolor (button8), isgamefinished(gamesize)))
        button5.configure (
            command=lambda: (
                changecolor (button1),
                changecolor (button5),
                changecolor (button6),
                changecolor (button9), isgamefinished(gamesize)))
        button6.configure (
            command=lambda: (
                changecolor (button2),
                changecolor (button5),
                changecolor (button6),
                changecolor (button7),
                changecolor (button10), isgamefinished(gamesize)))
        button7.configure (
            command=lambda: (
                changecolor (button3),
                changecolor (button6),
                changecolor (button7),
                changecolor (button8),
                changecolor (button11), isgamefinished(gamesize)))
        button8.configure (
            command=lambda: (
                changecolor (button4),
                changecolor (button7),
                changecolor (button8),
                changecolor (button12), isgamefinished(gamesize)))
        button9.configure (
            command=lambda: (
                changecolor (button5),
                changecolor (button9),
                changecolor (button10),
                changecolor (button13), isgamefinished(gamesize)))
        button10.configure (
            command=lambda: (
                changecolor (button6),
                changecolor (button9),
                changecolor (button10),
                changecolor (button11),
                changecolor (button14), isgamefinished(gamesize)))
        button11.configure (
            command=lambda: (
                changecolor (button7),
                changecolor (button10),
                changecolor (button11),
                changecolor (button12),
                changecolor (button15), isgamefinished(gamesize)))
        button12.configure (
            command=lambda: (
                changecolor (button8),
                changecolor (button11),
                changecolor (button12),
                changecolor (button16), isgamefinished(gamesize)))
        button13.configure (
            command=lambda: (
                changecolor (button9),
                changecolor (button13),
                changecolor (button14), isgamefinished(gamesize)))
        button14.configure (
            command=lambda: (
                changecolor (button10),
                changecolor (button13),
                changecolor (button14),
                changecolor (button15), isgamefinished(gamesize)))
        button15.configure (
            command=lambda: (
                changecolor (button11),
                changecolor (button14),
                changecolor (button15),
                changecolor (button16), isgamefinished(gamesize)))
        button16.configure (
            command=lambda: (
                changecolor (button12),
                changecolor (button15),
                changecolor (button16), isgamefinished(gamesize)))

    clearbutton = Button(gamewin, text='Clear all')
    clearbutton.grid(row=0, column=gamesize+1)
    clearbutton.configure(command= lambda: clearall(gamesize))


def changecolor(self):
    if self.cget ('fg') == 'white':
        self.configure (fg='black')
    else:
        self.configure (fg='white')

def isgamefinished(gamesize):
    if (gamesize == 3):
        if((button1.cget('fg') == 'black') &
                (button2.cget('fg') == 'black') &
                (button3.cget('fg') == 'black') &
                (button4.cget('fg') == 'black') &
                (button5.cget('fg') == 'black') &
                (button6.cget('fg') == 'black') &
                (button7.cget('fg') == 'black') &
                (button8.cget('fg') == 'black') &
                (button9.cget('fg') == 'black')):
            messagebox.showinfo ("Congratulations", "You have won! :)")
            clearall(gamesize)
    else:
        if((button1.cget('fg') == 'black') &
                (button2.cget('fg') == 'black') &
                (button3.cget('fg') == 'black') &
                (button4.cget('fg') == 'black') &
                (button5.cget('fg') == 'black') &
                (button6.cget('fg') == 'black') &
                (button7.cget('fg') == 'black') &
                (button8.cget('fg') == 'black') &
                (button9.cget('fg') == 'black') &
                (button10.cget('fg') == 'black') &
                (button11.cget('fg') == 'black') &
                (button12.cget('fg') == 'black') &
                (button13.cget('fg') == 'black') &
                (button14.cget('fg') == 'black') &
                (button15.cget('fg') == 'black') &
                (button16.cget('fg') == 'black')):
            messagebox.showinfo ("Congratulations", "You have won! :)")
            clearall(gamesize)

def clearall(gamesize):
    if gamesize == 3:
        button1.configure (fg='white')
        button2.configure (fg='white')
        button3.configure (fg='white')
        button4.configure (fg='white')
        button5.configure (fg='white')
        button6.configure (fg='white')
        button7.configure (fg='white')
        button8.configure (fg='white')
        button9.configure (fg='white')
    else:
        button1.configure (fg='white')
        button2.configure (fg='white')
        button3.configure (fg='white')
        button4.configure (fg='white')
        button5.configure (fg='white')
        button6.configure (fg='white')
        button7.configure (fg='white')
        button8.configure (fg='white')
        button9.configure (fg='white')
        button10.configure (fg='white')
        button11.configure (fg='white')
        button12.configure (fg='white')
        button12.configure (fg='white')
        button13.configure (fg='white')
        button14.configure (fg='white')
        button15.configure (fg='white')
        button16.configure (fg='white')


mainwin = Tk ()
selectgamesize ()
mainwin.mainloop ()

