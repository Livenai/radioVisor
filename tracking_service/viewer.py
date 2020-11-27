from mainwindow import *
import numpy as np
import glob
import json
from datetime import datetime

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsItem, QWidget
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import QTimer
from PyQt5.Qt import Qt



class estela():
    """ Construye y representa una estela, es decir, una serie de elementos repetidos que desaparecen con las iteraciones. """

    def __init__(self, MainWindow, leader, maxDots, ticks_per_dot, dotSize, brush, pen):
        self.MainWindow = MainWindow
        self.leader = leader # referencia al punto maestro paraobtener sus coordenadas
        self.maxDots = maxDots
        self.ticks_per_dot = ticks_per_dot
        self.dotSize = dotSize
        self.brush = brush
        self.pen = pen

        self.iterCounter = 0
        self.elements = []
        self.filled = False # booleano para optimizar el rendimiento una vez se ha llenado la lista

    def iniciarEstela(self):
        """ Inicia el contador que va dejando elementos con las iteracciones. """

    def countIter(self):
        """ Añade una iterraccion al contador y realiza las acciones pertienentes respecto del nuevo valor. """
        self.iterCounter += 1

        if self.iterCounter >= self.ticks_per_dot:
            # Toca añadir un nuevo elemento a la estela...
            rec = self.leader.boundingRect()

            x = self.leader.scenePos().x() + (rec.width()/2)
            y = self.leader.scenePos().y() + (rec.height()/2)
            newDot = self.MainWindow.scene.addEllipse(0,0, self.dotSize,self.dotSize, self.pen, self.brush)
            newDot.setPos(x-(self.dotSize/2),y-(self.dotSize/2))
            newDot.setZValue(-1)

            self.elements.append(newDot)

            # Eliminar el ultimo elemento, si toca...
            if self.filled:
                victim = self.elements.pop(0)
                self.MainWindow.scene.removeItem(victim)
            elif len(self.elements) >= self.maxDots:
                self.filled = True

            # Y redimensionar el resto descendentemente.[WIP]



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
        self.reproduccionDot = None # Punto en la escena que se mueve con el panel de reproduccion
        self.estela = None
        self.isWhite = False

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
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.setTickInterval(60) # ticks cada minuto



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
            self.isWhite = True
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

        print(self.filename, "\t log elements created succesfully")





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

        # reproduccion
        self.playTimer = QTimer()
        self.playTimer.setInterval(1000)
        self.minPlaySec = 0
        self.maxPlaySec = 0
        self.actualPlaySec = 0




        # graficos
        self.scene  = QGraphicsScene()
        self.drawBox.setScene(self.scene)



        self.increaseZoomButton.clicked.connect(self.increaseZoom)
        self.decreaseZoomButton.clicked.connect(self.decreaseZoom)
        self.invertAxisButton.clicked.connect(self.invertSceneAxis)

        self.loadLogsButton.clicked.connect(self.loadLogs)

        self.playTimer.timeout.connect(self.playTimerRang)
        self.playStopButton.clicked.connect(self.playStopButton_clicked)
        self.playPositionSlider.valueChanged.connect(self.playPositionSlider_changed)
        self.speedTickBox.valueChanged.connect(self.speedTickBox_changed)
        self.enableReproduccionBoxCheckBox.stateChanged.connect(self.enableReproduccionBoxCheckBox_changed)

        # inicio
        self.drawAnchorLines()
        ########################################################################

    def enableReproduccionBoxCheckBox_changed(self):
        if self.enableReproduccionBoxCheckBox.isChecked():
            [x.setEnabled(True) for x in self.reproduccionBox.findChildren(QWidget)]
        else:
            if self.playStopButton.isChecked():
                # paramos el playTimer
                self.playStopButton.click()
            # Desactivamos los controles
            [x.setEnabled(False) for x in self.reproduccionBox.findChildren(QWidget)]
            self.enableReproduccionBoxCheckBox.setEnabled(True)
            # Quitamos los puntos de la escena
            for k in self.logs.keys():
                log = self.logs[k]
                if log.reproduccionDot is not None:
                    self.scene.removeItem(log.reproduccionDot)
                    log.reproduccionDot = None



    def playPositionSlider_changed(self, newValue):
        self.actualPlaySec = newValue

        strDate = datetime.fromtimestamp(newValue).strftime("%Y/%m/%d  %H:%M:%S")
        self.actualPlayLabel.setText(strDate)

    def playStopButton_clicked(self):
        if self.playStopButton.isChecked():
            # activamos el playTimer
            self.playTimer.start()
            self.playStopButton.setText("||")
        else:
            # paramos el playTimer
            self.playTimer.stop()
            self.playStopButton.setText(">")

    def speedTickBox_changed(self, newValue):
        ms = (1 / newValue) * 1000
        self.playTimer.setInterval(ms)

    def playTimerRang(self):
        addition = (self.speedMinBox.value()*60) + self.speedSecBox.value()
        newValue = self.playPositionSlider.value() + addition
        self.playPositionSlider_changed(newValue)
        self.playPositionSlider.setValue(newValue)

        # saber que logs entan checkeados
        checkedLogs = []
        for k in self.logs.keys():
            log = self.logs[k]
            if log.checkBox.isChecked():
                checkedLogs.append(log)
            else:
                if log.reproduccionDot is not None:
                    self.scene.removeItem(log.reproduccionDot)
                    log.reproduccionDot = None



        # para cada log checkeado:
        for log in checkedLogs:
            # saber entre que dos puntos de tiempo estamos de su log
            actual = self.actualPlaySec
            logKeysList = [k for k in log.json.keys()]
            #logKeysList.sort(key=lambda key: float(str(key)))

            x_list = [log.json[k]['x'] for k in logKeysList]
            y_list = [log.json[k]['y'] for k in logKeysList]

            # interpolar el punto actual
            interpolated_X = np.interp(actual, logKeysList, x_list)
            interpolated_Y = np.interp(actual, logKeysList, y_list)

            # mostrar el punto con el color correspondiente
            x = interpolated_X * self.reduFactor
            y = interpolated_Y * self.reduFactor
            if log.reproduccionDot is None:
                log.reproduccionDot = self.scene.addEllipse(0,0, log.dotSize,log.dotSize, QPen(Qt.black, log.dotBorderSize), log.brush)
                log.reproduccionDot.setPos(x-(log.dotSize/2),y-(log.dotSize/2))

                # Creamos la estela (MainWindow, leader, maxDots, ticks_per_dot, dotSize, brush, pen)
                brush = [QBrush(Qt.black) if log.isWhite else log.brush][0]
                log.estela = estela(self, log.reproduccionDot, 30, 1, 7, brush, QPen(Qt.NoPen))

            else:
                log.reproduccionDot.setPos(x-(log.dotSize/2),y-(log.dotSize/2))
                # Actualizamos la estela
                log.estela.countIter()








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
        timeLabelX = 770

        Y_phase = 30
        Y_initial_phase = 100

        for i in range(0,log_num):

            label = QtWidgets.QLabel(parent)
            label.setGeometry(QtCore.QRect(0, 0, 110, 21))
            label.setObjectName("logLabel_" + str(i))
            label.setText("test_" + str(i))
            label.move(labelX, (Y_phase*i)+Y_initial_phase)
            label.show()

            checkBox = QtWidgets.QCheckBox(parent)
            checkBox.setGeometry(QtCore.QRect(10, 20, 85, 21))
            checkBox.setObjectName("logCheckBox_" + str(i))
            checkBox.move(checkBoxX, (Y_phase*i)+Y_initial_phase)
            checkBox.show()

            slider = QtWidgets.QSlider(parent)
            slider.setGeometry(QtCore.QRect(30, 30, 600, 25))
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider.setObjectName("logSlider_" + str(i))
            slider.move(sliderX, (Y_phase*i)+Y_initial_phase+2)
            slider.show()

            timeLabel = QtWidgets.QLabel(parent)
            timeLabel.setGeometry(QtCore.QRect(0, 0, 145, 21))
            timeLabel.setObjectName("timeLabel_" + str(i))
            timeLabel.setText("--/--/--  --:--:--")
            timeLabel.move(timeLabelX, (Y_phase*i)+Y_initial_phase)
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

        # preparamos el panel de reproduccion
        [x.setEnabled(False) for x in self.reproduccionBox.findChildren(QWidget)]
        self.reproduccionBox.setEnabled(True)
        self.enableReproduccionBoxCheckBox.setEnabled(True)

        allKeys = []
        for key in self.logs:
            [allKeys.append(str(x)) for x in self.logs[key].json.keys()]

        print("Keys: ", len(allKeys))
        allKeys = np.array(allKeys).astype(np.float)
        self.minPlaySec = np.min(allKeys)
        self.maxPlaySec = np.max(allKeys)
        self.actualPlaySec = self.minPlaySec
        self.playPositionSlider.setMinimum(self.minPlaySec)
        self.playPositionSlider.setMaximum(self.maxPlaySec)

        minDate = datetime.fromtimestamp(self.minPlaySec).strftime("%Y/%m/%d  %H:%M:%S")
        maxDate = datetime.fromtimestamp(self.maxPlaySec).strftime("%Y/%m/%d  %H:%M:%S")
        self.minPlayLabel.setText(minDate)
        self.maxPlayLabel.setText(maxDate)
        self.actualPlayLabel.setText(minDate)

        self.loadLogsButton.setEnabled(False)

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
