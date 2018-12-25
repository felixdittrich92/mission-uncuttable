from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


# Comment-toggle these two lines to switch the theme (only one should
# be active at the same time):
# styleSheet = open('light_theme.qss', 'r')
styleSheet = open('dark_theme.qss', 'r')


# Create and run an application showing the dialog:
app = QApplication([])
window = QDialog()
uic.loadUi("demo_gui_unstyled_pyqt5.ui", window)
app.setStyleSheet(styleSheet.read())
window.show()
app.exec()
