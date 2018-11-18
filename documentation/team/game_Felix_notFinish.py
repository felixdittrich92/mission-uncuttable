# not finished
import sys
import subprocess

from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication, QSizePolicy,)

"""
Verbesserungsvorschläge:
- mehrere Klassen verwenden
- nur eine Klasse pro Datei (außer private Klassen)
- Trennung von Datenmodell, Logik und Darstellung
- Verwendung von Schleifen, Arrays und allgemein gültigen Funktionen zur Reduzierung des Codes
- Code abstrahieren und wiederverwenden!!!
- bessere Logik überlegen
"""
class basicWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Game - Gruselcode')

        button1 = QPushButton("3 x 3", self)
        button1.move(106, 115)
        button1.resize(38, 30)
        button1.setStyleSheet("background-color: grey")
        button1.clicked.connect(self.button1clicked)

        button2 = QPushButton("4 x 4", self)
        button2.move(153, 115)
        button2.resize(38, 30)
        button2.setStyleSheet("background-color: grey")
        button2.clicked.connect(self.button2clicked)

    def button1clicked(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        for x in range(3):
            for y in range(3):
                button = QPushButton()
                policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                button.setSizePolicy(policy)
                button.setStyleSheet("background-color: white")
                grid_layout.addWidget(button, x, y)
                button.clicked.connect(self.buttonColor)
        button3 = QPushButton("Restart", self)
        grid_layout.addChildWidget(button3)
        button3.move(125, 0)
        button3.resize(50, 20)
        button3.setStyleSheet("background-color: grey")
        button3.clicked.connect(self.button3clicked)

    def button2clicked(self):
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        for x in range(4):
            for y in range(4):
                button = QPushButton()
                policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                button.setSizePolicy(policy)
                button.setStyleSheet("background-color: white")
                grid_layout.addWidget(button, x, y)
                button.clicked.connect(self.buttonColor1)
        button3 = QPushButton("Restart", self)
        grid_layout.addChildWidget(button3)
        button3.move(125, 0)
        button3.resize(50, 20)
        button3.setStyleSheet("background-color: grey")
        button3.clicked.connect(self.button3clicked)

    def buttonColor(self):
        button = self.sender()
        index = self.layout().indexOf(button)
        loc = self.layout().getItemPosition(index)
        black = "background color: black"
        white = "background-color: white"

        if loc[0] == 0 and loc[1] == 0:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0]+1, loc[1]).widget()
                b2.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1]+1).widget()
                b3.setStyleSheet("background-color: black")

        elif loc[0] == 1 and loc[1] == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()  #clicked
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget() #down
                b2.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget() #right
                b3.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget() #up
                b4.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget() #left
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 1 and loc[1] == 0:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
                b2.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()
                b4.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
                b3.setStyleSheet("background-color: black")

        elif loc[0] == 2 and loc[1] == 0:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
                b3.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()
                b4.setStyleSheet("background-color: black")

        elif loc[0] == 2 and loc[1] == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
                b3.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()
                b4.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 2 and loc[1] == 2:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()
                b4.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 1 and loc[1] == 2:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
                b2.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()
                b4.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 0 and loc[1] == 2:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
                b2.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 0 and loc[1] == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
                b2.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()
                b5.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
                b3.setStyleSheet("background-color: black")


    # loc[0] > 2 and loc[1] > 2 no function
    # only test
    def buttonColor1(self):
        button = self.sender()
        index = self.layout().indexOf(button)
        loc = self.layout().getItemPosition(index)

        if loc[0] == 0 and loc[1] == 0:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
            b2.setStyleSheet("background-color: black")
            b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
            b3.setStyleSheet("background-color: black")
            a = 1
            if a == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
                b2.setStyleSheet("background-color: white")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
                b3.setStyleSheet("background-color: white")

        elif loc[0] == 1 and loc[1] == 1:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()  # geklickte
            b1.setStyleSheet("background-color: black")
            b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
            b2.setStyleSheet("background-color: black")
            b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
            b3.setStyleSheet("background-color: black")
            b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
            b4.setStyleSheet("background-color: black")
            b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
            b5.setStyleSheet("background-color: black")
            b = 1
            if b == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()  # geklickte
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
                b2.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
                b3.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
                b4.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 1 and loc[1] == 0:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
            b2.setStyleSheet("background-color: black")
            b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()
            b4.setStyleSheet("background-color: black")
            b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
            b3.setStyleSheet("background-color: black")
            c = 1
            if c == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()
                b2.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()
                b4.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()
                b3.setStyleSheet("background-color: black")

        elif loc[0] == 2 and loc[1] == 0:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
            b3.setStyleSheet("background-color: black")
            b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
            b4.setStyleSheet("background-color: black")
            d = 1
            if d == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
                b3.setStyleSheet("background-color: white")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
                b4.setStyleSheet("background-color: white")

        elif loc[0] == 2 and loc[1] == 1:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
            b3.setStyleSheet("background-color: black")
            b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
            b4.setStyleSheet("background-color: black")
            b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
            b5.setStyleSheet("background-color: black")
            e = 1
            if e == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
                b3.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
                b4.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 2 and loc[1] == 2:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
            b4.setStyleSheet("background-color: black")
            b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
            b5.setStyleSheet("background-color: black")
            f = 1
            if f == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
                b4.setStyleSheet("background-color: white")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
                b5.setStyleSheet("background-color: white")

        elif loc[0] == 1 and loc[1] == 2:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
            b2.setStyleSheet("background-color: black")
            b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
            b4.setStyleSheet("background-color: black")
            b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
            b5.setStyleSheet("background-color: black")
            g = 1
            if g == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
                b2.setStyleSheet("background-color: black")
                b4 = self.layout().itemAtPosition(loc[0] - 1, loc[1]).widget()  # hoch
                b4.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
                b5.setStyleSheet("background-color: black")

        elif loc[0] == 0 and loc[1] == 2:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
            b2.setStyleSheet("background-color: black")
            b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
            b5.setStyleSheet("background-color: black")
            h = 1
            if h == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
                b2.setStyleSheet("background-color: white")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
                b5.setStyleSheet("background-color: white")

        elif loc[0] == 0 and loc[1] == 1:
            b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
            b1.setStyleSheet("background-color: black")
            b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
            b2.setStyleSheet("background-color: black")
            b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
            b5.setStyleSheet("background-color: black")
            b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
            b3.setStyleSheet("background-color: black")
            i = 1
            if i == 1:
                b1 = self.layout().itemAtPosition(loc[0], loc[1]).widget()
                b1.setStyleSheet("background-color: black")
                b2 = self.layout().itemAtPosition(loc[0] + 1, loc[1]).widget()  # runter
                b2.setStyleSheet("background-color: black")
                b5 = self.layout().itemAtPosition(loc[0], loc[1] - 1).widget()  # links
                b5.setStyleSheet("background-color: black")
                b3 = self.layout().itemAtPosition(loc[0], loc[1] + 1).widget()  # rechts
                b3.setStyleSheet("background-color: black")

    def button3clicked(self):
        self.close()
        subprocess.call("python" + " game.py", shell=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = basicWindow()
    window.setStyleSheet("background-color: orange")
    window.setFixedSize(300, 300)
    window.show()
    sys.exit(app.exec_())

