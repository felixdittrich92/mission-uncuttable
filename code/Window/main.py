import sys
from qtpy import QtWidgets
from ui.mainwindow import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QMainWindow()

ui_window = Ui_MainWindow()
ui_window.setupUi(window)
window.setWindowTitle("Mission-Uncuttable")

window.showMaximized()
sys.exit(app.exec_())