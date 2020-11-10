# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1158, 841)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.radiosBox = QtWidgets.QScrollArea(self.centralwidget)
        self.radiosBox.setMaximumSize(QtCore.QSize(16777215, 150))
        self.radiosBox.setLineWidth(3)
        self.radiosBox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.radiosBox.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.radiosBox.setWidgetResizable(False)
        self.radiosBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.radiosBox.setObjectName("radiosBox")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 818, 352))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setGeometry(QtCore.QRect(0, -20, 821, 371))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.radiosBox.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.radiosBox, 2, 4, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setMinimumSize(QtCore.QSize(180, 0))
        self.groupBox_3.setObjectName("groupBox_3")
        self.loadLogsButton = QtWidgets.QPushButton(self.groupBox_3)
        self.loadLogsButton.setGeometry(QtCore.QRect(10, 60, 80, 23))
        self.loadLogsButton.setObjectName("loadLogsButton")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(0, 30, 84, 15))
        self.label_2.setObjectName("label_2")
        self.coordsLabel = QtWidgets.QLabel(self.groupBox_3)
        self.coordsLabel.setGeometry(QtCore.QRect(90, 30, 91, 16))
        self.coordsLabel.setObjectName("coordsLabel")
        self.gridLayout.addWidget(self.groupBox_3, 2, 5, 1, 2)
        self.drawBox = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.drawBox.sizePolicy().hasHeightForWidth())
        self.drawBox.setSizePolicy(sizePolicy)
        self.drawBox.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.drawBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.drawBox.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.drawBox.setLineWidth(1)
        self.drawBox.setMidLineWidth(0)
        self.drawBox.setObjectName("drawBox")
        self.gridLayout.addWidget(self.drawBox, 0, 1, 1, 6)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(100, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.invertAxisButton = QtWidgets.QPushButton(self.groupBox_2)
        self.invertAxisButton.setGeometry(QtCore.QRect(0, 20, 89, 23))
        self.invertAxisButton.setObjectName("invertAxisButton")
        self.increaseZoomButton = QtWidgets.QPushButton(self.groupBox_2)
        self.increaseZoomButton.setGeometry(QtCore.QRect(60, 50, 30, 27))
        self.increaseZoomButton.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.increaseZoomButton.setFont(font)
        self.increaseZoomButton.setObjectName("increaseZoomButton")
        self.zoomLabel = QtWidgets.QLabel(self.groupBox_2)
        self.zoomLabel.setGeometry(QtCore.QRect(0, 90, 89, 21))
        self.zoomLabel.setObjectName("zoomLabel")
        self.decreaseZoomButton = QtWidgets.QPushButton(self.groupBox_2)
        self.decreaseZoomButton.setGeometry(QtCore.QRect(0, 50, 30, 27))
        self.decreaseZoomButton.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.decreaseZoomButton.setFont(font)
        self.decreaseZoomButton.setObjectName("decreaseZoomButton")
        self.gridLayout.addWidget(self.groupBox_2, 2, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1158, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Control"))
        self.loadLogsButton.setText(_translate("MainWindow", "Load Logs"))
        self.label_2.setText(_translate("MainWindow", "Coordenadas:"))
        self.coordsLabel.setText(_translate("MainWindow", "[x,y,z]"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Zoom"))
        self.invertAxisButton.setText(_translate("MainWindow", "Invert   Y"))
        self.increaseZoomButton.setText(_translate("MainWindow", "+"))
        self.zoomLabel.setText(_translate("MainWindow", "----------"))
        self.decreaseZoomButton.setText(_translate("MainWindow", "-"))
