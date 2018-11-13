import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Game')
        self.game_widget = Game(parent=self)
        self.setCentralWidget(self.game_widget)

        menubar = self.menuBar()
        settingsMenu = menubar.addMenu('&Settings')

        opt1 = QtWidgets.QAction('3x3', self)
        opt2 = QtWidgets.QAction('4x4', self)
        opt3 = QtWidgets.QAction('reset', self)

        settingsMenu.addAction(opt1)
        settingsMenu.addAction(opt2)
        settingsMenu.addAction(opt3)

        opt1.triggered.connect(lambda: self.game_widget.setupGUI(3))
        opt2.triggered.connect(lambda: self.game_widget.setupGUI(4))
        opt3.triggered.connect(self.game_widget.reset)


class Game(QtWidgets.QWidget):
    n = 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupGUI(Game.n)

    def buttonClicked(self):
        button = self.sender()
        idx = self.layout().indexOf(button)
        location = self.layout().getItemPosition(idx)
        self.changeColor(button)
        if location[0] - 1 >= 0:
            buttonAbove = self.layout().itemAtPosition(location[0] - 1, location[1]).widget()
            self.changeColor(buttonAbove)
        if location[0] + 1 <= Game.n - 1:
            buttonBelow = self.layout().itemAtPosition(location[0] + 1, location[1]).widget()
            self.changeColor(buttonBelow)
        if location[1] - 1 >= 0:
            buttonLeft = self.layout().itemAtPosition(location[0], location[1] - 1).widget()
            self.changeColor(buttonLeft)
        if location[1] + 1 <= Game.n - 1:
            buttonRight = self.layout().itemAtPosition(location[0], location[1] + 1).widget()
            self.changeColor(buttonRight)
        self.checkWin()

    def changeColor(self, button):
        color = button.palette().button().color().name()
        if color == "#ffffff":
            button.setStyleSheet("background-color: #d4d4d4; border: 2px solid #d4d4d4;")
        elif color == "#d4d4d4":
            button.setStyleSheet("background-color: white; border: 2px solid #d4d4d4;")

    def checkWin(self):
        won = True
        for i in range(Game.n * Game.n):
            button = self.layout().itemAt(i).widget()
            color = button.palette().button().color().name()
            if color == "#ffffff":
                won = None
                break
        if won:
            msgBox = QMessageBox()
            msgBox.about(self, "Gewonnen", "Du hast gewonnen!")
            self.reset()

    def reset(self):
        for i in range(Game.n * Game.n):
            button = self.layout().itemAt(i).widget()
            button.setStyleSheet("background-color: #ffffff; border: 2px solid #d4d4d4")

    def setupGUI(self, n):
        if n == 3:
            self.setFixedSize(330, 330)
            self.parent().adjustSize()
        else:
            self.setFixedSize(436, 436)
        Game.n = n
        self.clearLayout(self.layout())
        self.setLayout(QtWidgets.QGridLayout())

        for i in range(n):
            for j in range(n):
                button = QtWidgets.QPushButton(" ")
                button.setFixedSize(100, 100)
                button.setStyleSheet("background-color: white; border: 2px solid #d4d4d4;")
                button.clicked.connect(self.buttonClicked)
                self.layout().addWidget(button, i, j)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
