from mainwindow import *
import numpy as np
import glob
import json
from datetime import datetime

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import QTimer
from PyQt5.Qt import Qt


class logControl():
    def __init__(self, label, checkBox, slider, timeLabel, filename, fileroute, MainWindow_reference):
        # params
        self.label = label
        self.checkBox = checkBox
        self.slider = slider
        self.timeLabel = timeLabel
        self.filename  = filename
        self.fileroute = fileroute
        self.MainWindow = MainWindow_reference
        self.json = {}
        self.elements = []
        self.pen = QPen(Qt.black)
        self.brush = QBrush(Qt.black)
        self.lastSlideValue = 1
        self.minOpacity = 0.001 # 1.0 opaco; 0.0 invisible
        self.lineSize = 2
        self.dotSize = 10
        self.dotBorderSize = 2
        self.opacityTailLen = 40

        # default
        self.slider.setEnabled(False)
        self.json = json.load(open(self.fileroute, "r"))
        self.slider.setMinimum(1)
        self.slider.setMaximum(len(self.json))


        # conexiones
        self.checkBox.stateChanged.connect(self.checkBox_changed)
        self.slider.valueChanged.connect(self.slider_changed)

        # primeros pasos
        self.setColors()
        self.createAllObjects()



    def checkBox_changed(self):
        if self.checkBox.isChecked():
            self.slider.setEnabled(True)
            self.slider_changed(self.slider.value())
        else:
            self.slider.setEnabled(False)
            self.slider_changed(1)


    def slider_changed(self, newValue):
        print(self.filename, "last value:", self.lastSlideValue, "   new value:", newValue)
        # Si el nuevo valor es mayor que el anterior
        if newValue > self.lastSlideValue:
            # mostramos todos los elementos desde lastValue hasta newValue
            for i in range(self.lastSlideValue, newValue):
                self.elements[i][0].show()
                self.elements[i][1].show()
        elif self.lastSlideValue > newValue:
            # si el nuevo valor es menor, ocultamos los elementos desde newValue hasta lastValue
            for i in range(newValue, self.lastSlideValue):
                self.elements[i][0].hide()
                self.elements[i][1].hide()
        else:
            # newValue y lastValue son iguales, por lo que no deberia hacerse nada
            pass


        # Si es posible, aumentamos la opacidad de los ultimos elementos mostrados
        try:
            opacityDecay = (1.0-self.minOpacity)/self.opacityTailLen
            opacityNow = 1.0
            # Empezando por el ultimo, vamos ajustando la opacidad de los
            # self.opacityTailLen elementos gradualmente menor, desde 1 hasta la minima
            for i in range(newValue, newValue-self.opacityTailLen, -1):
                self.elements[i][0].setOpacity(opacityNow)
                self.elements[i][1].setOpacity(opacityNow)
                opacityNow -= opacityDecay
        except:
            pass # si no se puede pues nada :)


        # Actualizamos lastSlideValue y el label de tiempo
        self.lastSlideValue = newValue
        strTime = datetime.fromtimestamp(int(float(self.elements[newValue-1][2]))).strftime("%Y/%m/%d  %H:%M:%S")
        self.timeLabel.setText(strTime)

    def setColors(self):
        """
        Establece el color en funcion del nombre del archivo.
        Si no puede obtener un color concreto, lo escoge aleatoriamente.
        """
        if "Am" in self.filename:
            self.pen = QPen(Qt.yellow, self.lineSize)
            self.brush = QBrush(Qt.yellow)
        elif "Az" in self.filename:
            self.pen = QPen(Qt.blue, self.lineSize)
            self.brush = QBrush(Qt.blue)
        elif "Bl" in self.filename:
            self.pen = QPen(Qt.black, self.lineSize)
            self.brush = QBrush(Qt.white)
        elif "Li" in self.filename:
            self.pen = QPen(Qt.magenta, self.lineSize)
            self.brush = QBrush(Qt.magenta)
        elif "Na" in self.filename:
            self.pen = QPen(QColor(235, 118, 40), self.lineSize)
            self.brush = QBrush(QColor(235, 118, 40))
        elif "Ro" in self.filename:
            self.pen = QPen(Qt.red, self.lineSize)
            self.brush = QBrush(Qt.red)
        elif "Ve" in self.filename:
            self.pen = QPen(Qt.green, self.lineSize)
            self.brush = QBrush(Qt.green)
        else:
            self.pen = QPen(Qt.white, self.lineSize)
            self.brush = QBrush(Qt.black)


    def createAllObjects(self):
        """
        Crea y añade a la escena todos los puntos y flechas que representan
        a este log y los oculta.
        """
        # Primero creamos los puntos
        for key in self.json:
            x = self.json[key]["x"]
            y = self.json[key]["y"]

            x = x * self.MainWindow.reduFactor
            y = y * self.MainWindow.reduFactor

            dot = self.MainWindow.scene.addEllipse(0,0, self.dotSize,self.dotSize, QPen(Qt.black, self.dotBorderSize), self.brush)
            dot.setPos(x-(self.dotSize/2),y-(self.dotSize/2))
            dot.setOpacity(self.minOpacity)
            dot.hide()
            self.elements.append([dot, None, key])


        # Ahora creamos las flechas que unen los puntos.
        """
        Cada flecha se guarda con el punto destino de forma que,
        en la lista de elementos, todos los elementos son una lista [punto, linea],
        excepto el primero que solo es el punto
        """
        for i in range(1, len(self.elements)):
            # Obtenemos los dos puntos
            sourceDot  = self.elements[i-1][0]
            destinyDot = self.elements[i][0]
            key = self.elements[i][2]

            # Obtenemos el radio de los puntos, asi podemos llevar la linea hasta el centro
            ellipseRadious = sourceDot.rect().width()/2


            # Obtenemos las coordenadas
            xo = sourceDot.scenePos().x()  + ellipseRadious
            yo = sourceDot.scenePos().y()  + ellipseRadious
            xd = destinyDot.scenePos().x() + ellipseRadious
            yd = destinyDot.scenePos().y() + ellipseRadious
            #print(xo,yo,xd,yd)


            # Creamos una linea desde sourceDot a destinyDot
            line = self.MainWindow.scene.addLine(xo,yo,xd,yd, self.pen)
            line.setOpacity(self.minOpacity)
            line.hide()

            # Guardamos el conjunto en self.elements
            self.elements[i] = [destinyDot, line, key]

        print(self.filename, " log elements created succesfully")





    def recreateElementList(self):
        """
        Recrea la lista de elementos acorde al nuevo reduFactor.
        Ha de llamarse despues de que reduFactor se haya actualizado y
        de que la escena se haya reseteado.
        """
        # Eliminamos todo de la lista
        del self.elements
        self.elements = []

        # Remontamos la lista
        self.createAllObjects()

        # Ponemos lastSlideValue a 1
        self.lastSlideValue = 1

        # Lanzamos la funcion de movimiento del slider para pintar los puntos de nuevo
        self.slider_changed(self.slider.value())





##############################################################################################################################################################################




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # variables
        self.A1 = np.array([0,0])
        self.A2 = np.array([6500,-1840])
        self.A3 = np.array([6600,6760])
        self.A4 = np.array([0,6820])

        self.reduFactor = 0.05
        self.zoomLabel.setText(str(round(self.reduFactor, 3)))

        # {nombre: {label, checkBox, slider}}
        self.logs = {}




        # graficos
        self.scene  = QGraphicsScene()
        self.drawBox.setScene(self.scene)



        self.increaseZoomButton.clicked.connect(self.increaseZoom)
        self.decreaseZoomButton.clicked.connect(self.decreaseZoom)
        self.invertAxisButton.clicked.connect(self.invertSceneAxis)

        self.loadLogsButton.clicked.connect(self.loadLogs)




        # inicio
        self.drawAnchorLines()


    def increaseZoom(self):
        self.reduFactor = self.reduFactor * 1.1
        self.zoomLabel.setText(str(round(self.reduFactor, 3)))
        self.reDrawAll()

    def decreaseZoom(self):
        self.reduFactor = self.reduFactor * 0.9
        self.zoomLabel.setText(str(round(self.reduFactor, 3)))
        self.reDrawAll()

    def invertSceneAxis(self):
        self.drawBox.scale(1, -1)



    def getLogsControlEntries(self, log_num, parent):
        """ Crea log_num controles en parent. """

        logEntriesList = []

        labelX = 10
        checkBoxX = 120
        sliderX = 150
        timeLabelX = 670

        Y_phase = 30

        for i in range(0,log_num):

            label = QtWidgets.QLabel(parent)
            label.setGeometry(QtCore.QRect(0, 0, 85, 21))
            label.setObjectName("logLabel_" + str(i))
            label.setText("test_" + str(i))
            label.move(labelX, Y_phase*i)
            label.show()

            checkBox = QtWidgets.QCheckBox(parent)
            checkBox.setGeometry(QtCore.QRect(10, 20, 85, 21))
            checkBox.setObjectName("logCheckBox_" + str(i))
            checkBox.move(checkBoxX, Y_phase*i)
            checkBox.show()

            slider = QtWidgets.QSlider(parent)
            slider.setGeometry(QtCore.QRect(30, 20, 500, 16))
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider.setObjectName("logSlider_" + str(i))
            slider.move(sliderX, Y_phase*i)
            slider.show()

            timeLabel = QtWidgets.QLabel(parent)
            timeLabel.setGeometry(QtCore.QRect(0, 0, 145, 21))
            timeLabel.setObjectName("timeLabel_" + str(i))
            timeLabel.setText("--/--/--  --:--:--")
            timeLabel.move(timeLabelX, Y_phase*i)
            timeLabel.show()


            logEntriesList.append([label, checkBox, slider, timeLabel])

        return logEntriesList



    def loadLogs(self):
        print("Loading logs...")
        # buscamos y cargamos los logs que haya en la carpeta tracking_logs
        logFiles = glob.glob("./tracking_logs/*.json")
        print("logs: ", len(logFiles))

        # creamos los sliders
        logEntriesList = self.getLogsControlEntries(len(logFiles), self.groupBox)

        # rellenamos los labels con los datos
        for i, log in enumerate(logFiles, 0):
            logName = log[log.rfind("/")+1:]
            logEntriesList[i][0].setText(logName)

            # creamos la clase
            lc = logControl(logEntriesList[i][0],
                            logEntriesList[i][1],
                            logEntriesList[i][2],
                            logEntriesList[i][3],
                            logName,
                            log,
                            self)

            # guardamos en el dicc
            self.logs[i] = lc


        print("--- Creation done ---")




    def reDrawAll(self):
        """ Funcion que borra la escena y la redibuja """
        # Borramos toda la escena
        self.scene  = QGraphicsScene()
        self.drawBox.setScene(self.scene)

        # Re dibujamos los bordes
        self.drawAnchorLines()

        # Re dibujamos los elementos de los logs si hubiera
        for log in self.logs:
            self.logs[log].recreateElementList()




    def drawAnchorLines(self):
        #factor de reduccion
        A1 = self.A1 * self.reduFactor
        A2 = self.A2 * self.reduFactor
        A3 = self.A3 * self.reduFactor
        A4 = self.A4 * self.reduFactor
        self.pen = QPen(Qt.black)
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
