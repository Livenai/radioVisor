# -*- coding: utf-8 -*-


import multiprocessing, os, json, time, traceback
from PyQt5.QtCore import QTimer


parent_folder = os.path.abspath(os.path.dirname(__file__))
saving_folder = os.path.join(parent_folder, "tracking")

MAX_TRYS = 5
MAX_DELAY_SECS = 10


def f(paramList):
    """
    Funcion generica que ejecuta cada hilo del pool.

    Esta funcion se encarga de recoger los datos de posicion de
    cada dispositivo y de escribirlos en su fichero correspondiente.
    """
    idHilo = str(multiprocessing.current_process()).split("-")[1][0]
    print("//////////   hilo: " + idHilo + "   //////////")
    print(paramList)

    trys = 0

    while trys < MAX_TRYS:
        try:
            # Obtenemos el nombre y peso del dispositivo
            name = paramList[0]
            pos = paramList[1] # cambiar por funcion de la api

            # Comprobamos si el archivo existe
            saving_file = os.path.join(saving_folder, name+".json")
            if os.path.isfile(saving_file):
                # Si existe, cargamos en formato json y añadimos los datos:
                # {timestamp:{x,y}}
                f = open(saving_file, "r")
                new_json = json.load(f)
                f.close()

                new_json[time.time()] = {"x": pos[0], "y": pos[1]}
            else:
                # Si no existe, creamos un json nuevo y añadimos los primeros datos
                # {timestamp: {x,y}}
                new_json = {str(time.time()): {"x": pos[0], "y": pos[1]}}

            # Guardamos los datos en el archivo
            print("new_json.len: ", len(new_json))
            f = open(saving_file, "w")
            f.write(json.dumps(new_json))
            f.close()

            # Para terminar, cancelamos el contador
            trys = MAX_TRYS
        except Exception as e:
            print(e)
            trys += 1






def iniciarPool():
    """ Obtiene la lista de dispositivos y levanta un proceso ejecutando f() para cada uno. """
    # Creamos el directiorio tracking/ si no existe ya
    print("Folder: ", parent_folder)

    if not os.path.exists(saving_folder):
        os.mkdir(saving_folder)
        print("+ Creando carpeta tracking/")
    else:
        print("Carpeta tracking/ ENCONTRADA")


    # Obtenemosla lista de dispositivos y la formateamos
    deviceList = {"a": [1,1], "b": [2,2], "c": [3,3]}

    paramList = list(deviceList.items())

    print("Num Devices: ", len(deviceList))
    print("paramList:\n" + str(paramList) + "\n\n")

    # Montamos el pool de trabajo
    p = multiprocessing.Pool(len(deviceList))
    solus = p.map(f,paramList)







#######  INICIO  #######
if __name__ == "__main__":
    while True:
        # Guardamos el timestamp
        t1 = time.time()

        # Ejecutamos
        iniciarPool()

        # Guardamos el timestamp
        t2 = time.time()

        # Calculamos la diferencia y el tiempo restante
        diff = t2-t1
        rest = MAX_DELAY_SECS - diff

        # Si rest es positivo, esperamos esa cantidad
        time.sleep(rest)
