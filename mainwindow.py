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
        MainWindow.resize(1158, 744)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.drawBox = QtWidgets.QGraphicsView(self.centralwidget)
        self.drawBox.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.drawBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.drawBox.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.drawBox.setLineWidth(1)
        self.drawBox.setMidLineWidth(0)
        self.drawBox.setObjectName("drawBox")
        self.gridLayout.addWidget(self.drawBox, 0, 1, 1, 8)
        self.botonIniciar = QtWidgets.QPushButton(self.centralwidget)
        self.botonIniciar.setObjectName("botonIniciar")
        self.gridLayout.addWidget(self.botonIniciar, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 7, 1, 1)
        self.stateLabel = QtWidgets.QLabel(self.centralwidget)
        self.stateLabel.setObjectName("stateLabel")
        self.gridLayout.addWidget(self.stateLabel, 2, 8, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 7, 1, 1)
        self.coordsLabel = QtWidgets.QLabel(self.centralwidget)
        self.coordsLabel.setObjectName("coordsLabel")
        self.gridLayout.addWidget(self.coordsLabel, 3, 8, 1, 1)
        self.searchNewDevicesButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchNewDevicesButton.setObjectName("searchNewDevicesButton")
        self.gridLayout.addWidget(self.searchNewDevicesButton, 3, 1, 1, 1)
        self.increaseZoomButton = QtWidgets.QPushButton(self.centralwidget)
        self.increaseZoomButton.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.increaseZoomButton.setFont(font)
        self.increaseZoomButton.setObjectName("increaseZoomButton")
        self.gridLayout.addWidget(self.increaseZoomButton, 3, 2, 1, 1)
        self.decreaseZoomButton = QtWidgets.QPushButton(self.centralwidget)
        self.decreaseZoomButton.setMaximumSize(QtCore.QSize(30, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.decreaseZoomButton.setFont(font)
        self.decreaseZoomButton.setObjectName("decreaseZoomButton")
        self.gridLayout.addWidget(self.decreaseZoomButton, 3, 3, 1, 1)
        self.oneShotButton = QtWidgets.QPushButton(self.centralwidget)
        self.oneShotButton.setObjectName("oneShotButton")
        self.gridLayout.addWidget(self.oneShotButton, 3, 4, 1, 1)
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
        self.botonIniciar.setText(_translate("MainWindow", "Iniciar"))
        self.label.setText(_translate("MainWindow", "Estado:"))
        self.stateLabel.setText(_translate("MainWindow", "Parado"))
        self.label_2.setText(_translate("MainWindow", "Coordenadas:"))
        self.coordsLabel.setText(_translate("MainWindow", "[x,y,z]"))
        self.searchNewDevicesButton.setText(_translate("MainWindow", "Buscar Nuevos Dispositivos"))
        self.increaseZoomButton.setText(_translate("MainWindow", "+"))
        self.decreaseZoomButton.setText(_translate("MainWindow", "-"))
        self.oneShotButton.setText(_translate("MainWindow", "OneShot"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

