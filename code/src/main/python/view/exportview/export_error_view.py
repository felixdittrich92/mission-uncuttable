from PyQt5.QtWidgets import QMessageBox


class ExportErrorView(QMessageBox):
    def __init__(self, error, parent=None):
        super(ExportErrorView, self).__init__(parent)

        self.setWindowTitle("Fehler beim Export")
        self.setText("Es gab einen Fehler beim exportieren. "
                     + "Versuche es mit anderen Einstellungen.")
        self.setDetailedText(error)

        self.exec_()
