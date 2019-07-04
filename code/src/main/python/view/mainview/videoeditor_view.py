from PyQt5.QtCore import QObject, QFileSystemWatcher, pyqtSignal
from PyQt5.QtWidgets import (QMainWindow, QWidget, QSplitter, QApplication, QMenu, QAction,
                             QMessageBox)
from PyQt5 import uic

from config import Resources, Language
from view.preview.preview import PreviewView
from view.timeline.timelineview import TimelineView
from controller import TimelineController
from model.project import Project
from config import Settings
from ..view import View
from util.classmaker import classmaker

class VideoEditorView(classmaker(QMainWindow, View)):
    """A class used as the View for the video-editor window."""
    
    save_project = pyqtSignal()
    
    def __init__(self, parent=None):

        """Loads the UI-file and the shortcuts."""
        super(VideoEditorView, self).__init__(parent)
        uic.loadUi(Resources.files.mainview, self)

        self.set_texts()

        self.timeline_view = TimelineView()
        self.load_timeline_widget()

        self.needle = self.findChild(QWidget, "needle_top")

        self.previewview = PreviewView.get_instance()
        self.load_preview()

        self.splittersizes = []
        self.fullscreen = False

        self.init_stylesheet()

        "QSS HOT RELOAD"
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

    def init_stylesheet(self):
        current_stylesheet = Settings.get_instance().get_settings().design.color_theme.current
        if current_stylesheet == 0:
            self.setStyleSheet(open(Resources.files.qss_dark, "r").read())     
        elif current_stylesheet == 1:
            self.setStyleSheet(open(Resources.files.qss_light, "r").read())
            
    
    def testmethod(self):
        PreviewView.get_instance().testprint()

    def set_texts(self):
        """ Loads the text for the menu from the language files """
        menu_program = self.findChild(QMenu, "menuProgramm")
        menu_program.setTitle(str(Language.current.menubar.program))

        action_settings = self.findChild(QAction, "action_settings")
        action_settings.setText(str(Language.current.menubar.settings))

        menu_project = self.findChild(QMenu, "menuProjekt")
        menu_project.setTitle(str(Language.current.menubar.project))

        action_new = self.findChild(QAction, "actionNeu")
        action_new.setText(str(Language.current.menubar.new))

        action_open = self.findChild(QAction, "actionOeffnen")
        action_open.setText(str(Language.current.menubar.open))

        action_save = self.findChild(QAction, "actionSpeichern")
        action_save.setText(str(Language.current.menubar.save))

        action_saveas = self.findChild(QAction, "actionSpeichern_als")
        action_saveas.setText(str(Language.current.menubar.saveas))

        action_projectsettings = self.findChild(QAction, "action_projectsettings")
        action_projectsettings.setText(str(Language.current.menubar.projectsettings))

        action_export = self.findChild(QAction, "actionExport")
        action_export.setText(str(Language.current.menubar.export))

        menu_edit = self.findChild(QMenu, "menuEdit")
        menu_edit.setTitle(str(Language.current.menubar.edit))

        action_undo = self.findChild(QAction, "actionUndo")
        action_undo.setText(str(Language.current.menubar.undo))

        action_redo = self.findChild(QAction, "actionRedo")
        action_redo.setText(str(Language.current.menubar.redo))

    def load_timeline_widget(self):
        """
        Replaces the 'bottomFrame'-named QObject with a new instance of
        TimelineView. The widget doesn't have any real content yet after
        execution of this method.
        """
        splitter = self.findChild(QObject, 'horizontalSplitter')
        bottom_frame = self.findChild(QObject, 'bottomFrame')
        i = splitter.indexOf(bottom_frame)
        TimelineController(self.timeline_view)
        splitter.replaceWidget(i, self.timeline_view)
        self.timeline_view.show()

    def load_preview(self):
        splitter = self.findChild(QSplitter, "verticalSplitter")
        splitter.replaceWidget(1, self.previewview)
        self.previewview.show()
        self.previewview.maximize_button.clicked.connect(self.maxim)

    def show(self):
        """Starts the video-editor-window maximized."""
        self.showMaximized()

    def set_filemanager_view(self, filemanager_view):
        splitter = self.findChild(QSplitter, 'verticalSplitter')
        self.filemanager_view = filemanager_view
        splitter.replaceWidget(0, self.filemanager_view)
        self.filemanager_view.show()

    def update_qss(self):
        """ Updates the View when stylesheet changed, can be removed in production"""
        self.init_stylesheet()
        self.__qss_watcher = QFileSystemWatcher()
        self.__qss_watcher.addPath(Resources.files.qss_dark)
        self.__qss_watcher.fileChanged.connect(self.update_qss)

    def closeEvent(self, event):
        """ Closes all open Windows """
        self.previewview.stop()
        if Project.get_instance().changed:
            msgbox = QMessageBox()
            res = msgbox.question(self, str(Language.current.errors.unsaved.msgboxtitle),
                                  str(Language.current.errors.unsaved.msgboxtext),
                                  QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if res == QMessageBox.Yes:
                self.save_project.emit()
                QApplication.closeAllWindows()

                QMainWindow.closeEvent(self, event)

            elif res == QMessageBox.Cancel:
                event.ignore()
        else:
            QApplication.closeAllWindows()
            QMainWindow.closeEvent(self, event)

    def maxim(self):
        """ Sets Preview Fullscreen """
        if(self.fullscreen == False):   
            self.timeline_view.hide()
            self.filemanager_view.hide()
            self.fullscreen = True

        else:
            self.timeline_view.show()
            self.filemanager_view.show()
            self.fullscreen = False

    def connect_update(self):
        PreviewView.get_instance().update_information()

    def update_window(self):
        self.update()
    
    def refresh(self):
        self.init_stylesheet()
        self.set_texts()
        self.filemanager_view.refresh()
