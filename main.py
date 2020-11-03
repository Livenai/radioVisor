from mainwindow import *
import numpy as np

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import QTimer
from PyQt5.Qt import Qt

import radios_BLE_GATT_API as blapi

class DrawingDevice():
    """
    Clase que representa un dispositivo dibujado en la escena. Almacena los
    datos del dispositivo utiles para dibujar u obtener mas datos mediante
    la API.
    """

    def __init__(self):
        """ Ctor. sencillo """
        self.name = "NULL Name"
        self.coords = [None,None,None]
        self.dot = None # guarda el punto en la escena
        self.DWMapiDevice = None


        self.reduFactor = 1.0
        self.border_color = None
        self.fill_color = None


    def moveDot(self, newX, newY):
        """ Mueve el punto a la nueva posicion en la escena (teniendo en cuenta el factor de reduucion)"""
        self.dot.setPos(newX*self.reduFactor, newY*self.reduFactor)

    def updateDot(self):
        """ Actualiza el punto con los datos de la clase. """
        self.moveDot(self.coords[0], self.coords[1])










class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # variables
        self.iniciar = False
        self.getPosTimer = QTimer()
        self.getPosTimer.setInterval(100)
        self.getPosTimer.timeout.connect(self.getPosTimer_rang)
        self.reduFactor = 0.3
        self.deviceDicc = {}

        self.A1 = np.array([0,0])
        self.A2 = np.array([6500,-1840])
        self.A3 = np.array([6600,6760])
        self.A4 = np.array([0,6820])


        # graficos
        self.scene  = QGraphicsScene()
        self.drawBox.setScene(self.scene)

        self.drawBox.scale(1,-1)

        # default drawers
        self.greenBrush = QBrush(Qt.green)
        self.grayBrush = QBrush(Qt.gray)
        self.pen = QPen(Qt.black)

        self.drawAnchorLines()


        # conexiones
        self.botonIniciar.clicked.connect(self.botonIniciar_clicked)
        self.oneShotButton.clicked.connect(self.getPosTimer_rang)
        self.searchNewDevicesButton.clicked.connect(self.drawAllDWMPositions)
        self.increaseZoomButton.clicked.connect(self.increaseZoom)
        self.decreaseZoomButton.clicked.connect(self.decreaseZoom)


    def addDotToScene(self, X, Y, border_color, fill_color):
        """
        Crea un nuevo punto en la escena, lo dibuja con los colores dados, lo
        posiciona en la coordenadas dadas (teniendo en cuenta el factor de
        reduccion) y devuelve la instancia del punto.

        tanto border_color como fill_color han de ser una lista con los colores:

                [R, G, B]

        """
        pen = QPen(QColor(border_color[0], border_color[1], border_color[2]))
        brush = QBrush(QColor(border_color[0], border_color[1], border_color[2]))

        dot = self.scene.addEllipse(-10,-10, 20,20, pen, brush)
        dot.setPos(X*self.reduFactor, Y*self.reduFactor)

        return dot


    def botonIniciar_clicked(self):
        if self.iniciar == False:
            self.botonIniciar.setText("Parar")
            self.iniciar = True
            self.stateLabel.setText("En ejecucion")
            self.getPosTimer.start()
        else:
            self.botonIniciar.setText("Iniciar")
            self.iniciar = False
            self.stateLabel.setText("Parado")
            self.getPosTimer.stop()

    def increaseZoom(self):
        self.reduFactor = self.reduFactor * 1.1
        self.reDrawAll()

    def decreaseZoom(self):
        self.reduFactor = self.reduFactor * 0.9
        self.reDrawAll()


    def getPosTimer_rang(self):
        self.getPosTimer.stop()

        self.updateKnowedDevices()

        if self.iniciar == True:
            self.getPosTimer.start()


    def updateKnowedDevices(self):
        self.stateLabel.setText("Actualizando...")
        #para cada dispositivo en la lista
        for key in self.deviceDicc:
            #obtenemos el nombre y la posicion de cada dispositivos
            name = key
            pos  = blapi.readPos(self.deviceDicc[name].DWMapiDevice)

            #actualizamos la posicion de la instancia
            self.deviceDicc[name].coords = pos[:3]

            #usamos los datos para mover el punto dentro del dibujo
            self.deviceDicc[name].updateDot()
        self.stateLabel.setText("Fin Actualizacion")




    def drawAllDWMPositions(self):
        self.stateLabel.setText("Buscando dispositivos...")
        d_num = 0

        #obtenemos la lista de dispositivos cercanos y su nombre
        device_list = blapi.getNearDevices()

        #para cada dispositivo en la lista
        for key in device_list:
            #obtenemos el nombre y la posicion de cada dispositivos
            name = key
            pos  = blapi.readPos(device_list[name])

            #si el dispositivo existe dentro de deviceDicc
            if name in self.deviceDicc:
                #actualizamos la posicion de la instancia
                self.deviceDicc[name].coords = pos[:3]

                #usamos los datos para mover el punto dentro del dibujo
                self.deviceDicc[name].updateDot()

            #si el dispositivo no esta en deviceDicc
            else:
                #creamos una nueva instancia de la clase DrawingDevice
                new_device = DrawingDevice()
                d_num += 1

                #rellenamos la instancia con los datos
                new_device.name = name
                new_device.coords = pos[:3]
                new_device.DWMapiDevice = device_list[name]

                new_device.border_color = np.random.randint(20, 200, size=3)
                new_device.fill_color = np.random.randint(20, 200, size=3)
                new_device.reduFactor = self.reduFactor

                #creamos un nuevo punto a dibujar con los datos de de la instancia
                #añadimos el punto a la instancia
                new_device.dot = self.addDotToScene(pos[0], pos[1], new_device.border_color, new_device.fill_color)


                #añadimos la instancia a deviceDicc
                self.deviceDicc[name] = new_device

        self.stateLabel.setText(str(d_num) + " dispositivos nuevos.")



    def reDrawAll(self):
        """ Funcion que borra la escena y la redibuja """
        # borramos toda la escena
        self.scene  = QGraphicsScene()
        self.drawBox.setScene(self.scene)

        # re dibujamos los bordes
        self.drawAnchorLines()

        # re dibujamos los dispositivos
        #para cada dispositivo en la lista
        for key in self.deviceDicc:
                #creamos un nuevo punto a dibujar con los datos de de la instancia
                dot = self.addDotToScene(self.deviceDicc[key].coords[0], self.deviceDicc[key].coords[1], self.deviceDicc[key].border_color, self.deviceDicc[key].fill_color)
                #añadimos el punto a la instancia
                self.deviceDicc[key].dot = dot



    def drawAnchorLines(self):
        #factor de reduccion
        A1 = self.A1 * self.reduFactor
        A2 = self.A2 * self.reduFactor
        A3 = self.A3 * self.reduFactor
        A4 = self.A4 * self.reduFactor
        #A1
        self.A1Dot = self.scene.addEllipse(A1[0]-5,A1[1]-5, 10,10, self.pen, QBrush(Qt.black))
        self.A1Label = self.scene.addText("A1")
        self.A1Label.setDefaultTextColor(Qt.gray)
        self.A1Label.setPos(A1[0]-30,A1[1]-30)
        #A2
        self.A1Dot = self.scene.addEllipse(A2[0]-5,A2[1]-5, 10,10, self.pen, QBrush(Qt.black))
        self.A1Label = self.scene.addText("A2")
        self.A1Label.setDefaultTextColor(Qt.gray)
        self.A1Label.setPos(A2[0]-30,A2[1])
        #A3
        self.A1Dot = self.scene.addEllipse(A3[0]-5,A3[1]-5, 10,10, self.pen, QBrush(Qt.black))
        self.A1Label = self.scene.addText("A3")
        self.A1Label.setDefaultTextColor(Qt.gray)
        self.A1Label.setPos(A3[0],A3[1])
        #A4
        self.A1Dot = self.scene.addEllipse(A4[0]-5,A4[1]-5, 10,10, self.pen, QBrush(Qt.black))
        self.A1Label = self.scene.addText("A4")
        self.A1Label.setDefaultTextColor(Qt.gray)
        self.A1Label.setPos(A4[0],A4[1]-30)

        #Line 1--2
        self.A1A2Line = self.scene.addLine(A1[0],
                                           A1[1],
                                           A2[0],
                                           A2[1],
                                            self.pen)
        #Line 2--3
        self.A1A2Line = self.scene.addLine(A2[0],
                                           A2[1],
                                           A3[0],
                                           A3[1],
                                            self.pen)
        #Line 3--4
        self.A1A2Line = self.scene.addLine(A3[0],
                                           A3[1],
                                           A4[0],
                                           A4[1],
                                            self.pen)
        #Line 4--1
        self.A1A2Line = self.scene.addLine(A4[0],
                                           A4[1],
                                           A1[0],
                                           A1[1],
                                            self.pen)
















#######  INICIO  #######
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
