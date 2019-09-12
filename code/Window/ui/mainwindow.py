# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1254, 596)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalSplitter = QtWidgets.QSplitter(self.centralWidget)
        self.horizontalSplitter.setSizeIncrement(QtCore.QSize(0, 0))
        self.horizontalSplitter.setOrientation(QtCore.Qt.Vertical)
        self.horizontalSplitter.setObjectName("horizontalSplitter")
        self.verticalSplitter = QtWidgets.QSplitter(self.horizontalSplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.verticalSplitter.sizePolicy().hasHeightForWidth())
        self.verticalSplitter.setSizePolicy(sizePolicy)
        self.verticalSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.verticalSplitter.setObjectName("verticalSplitter")
        self.topleftFrame = QtWidgets.QFrame(self.verticalSplitter)
        self.topleftFrame.setMinimumSize(QtCore.QSize(200, 0))
        self.topleftFrame.setStyleSheet("background: rgb(255, 179, 248);")
        self.topleftFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topleftFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topleftFrame.setObjectName("topleftFrame")
        self.toprightFrame = QtWidgets.QFrame(self.verticalSplitter)
        self.toprightFrame.setMinimumSize(QtCore.QSize(200, 0))
        self.toprightFrame.setStyleSheet("background: rgb(255, 250, 170);")
        self.toprightFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toprightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toprightFrame.setObjectName("toprightFrame")
        self.bottomFrame = QtWidgets.QFrame(self.horizontalSplitter)
        self.bottomFrame.setEnabled(True)
        self.bottomFrame.setMinimumSize(QtCore.QSize(0, 120))
        self.bottomFrame.setStyleSheet("background: lightblue;")
        self.bottomFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottomFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottomFrame.setObjectName("bottomFrame")
        self.gridLayout.addWidget(self.horizontalSplitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1254, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

