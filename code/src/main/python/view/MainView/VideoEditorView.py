from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
import sys
import os

print("cwd:", os.getcwd())
print("listdir:", os.listdir("."))
print("Ist da?", os.path.isfile("main_window.ui"))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('view/MainView/main_window.ui', self)


class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):                              # 2. Implement run()
        window = QMainWindow()
        window.setWindowTitle("UbiCut")
        window.resize(250, 150)

        window.show()
        return self.app.exec_()                 # 3. End run() with this line


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run                     # 5. Invoke run()
    sys.exit(exit_code)
