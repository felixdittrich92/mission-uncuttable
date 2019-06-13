from PyQt5.QtWidgets import QMessageBox

from config import Language


class ExportErrorView(QMessageBox):
    def __init__(self, error, parent=None):
        super(ExportErrorView, self).__init__(parent)

        self.setWindowTitle(str(Language.current.errors.export.windowtitle))
        self.setText(str(Language.current.errors.export.errormessage))
        self.setDetailedText(error)

        self.exec_()
