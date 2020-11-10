# -*- coding: utf-8 -*-


import multiprocessing, os, json, time, traceback
import radios_BLE_GATT_API as blapi
import psutil


parent_folder = os.path.abspath(os.path.dirname(__file__))
saving_folder = os.path.join(parent_folder, "tracking_logs")

MAX_TRYS = 1
MAX_DELAY_SECS = 60


def f(paramList):
    """
    Funcion generica que ejecuta cada hilo del pool.

    Esta funcion se encarga de recoger los datos de posicion de
    cada dispositivo y de escribirlos en su fichero correspondiente.
    """
    idHilo = str(multiprocessing.current_process()).split("-")[1].split(",")[0]
    print("//////////   hilo: " + idHilo + "   //////////")
    print(multiprocessing.current_process())
    print(paramList)

    trys = 0


    while trys < MAX_TRYS:
        try:
            # Obtenemos el nombre y peso del dispositivo
            name = paramList[0]
            pos  = blapi.readPos(paramList[1])
            if None in pos:
                time.sleep(1)
                raise Exception("pos = None")
            else:
                print("------------->>  Pos de " + str(idHilo) + " obtenida con exito")

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
    # Comprueba la memoria RAM usada en el sistema. Si supera el 80%, se sale del programa
    mem = psutil.virtual_memory()
    percentMem = mem.percent
    print("Memory Usage:  ", percentMem, "%")
    if percentMem > 80.0:
        raise Exception("[!]    MEMORIA RAM AL 80%   [!]")

    # Creamos el directiorio tracking/ si no existe ya
    print("Folder: ", parent_folder)

    if not os.path.exists(saving_folder):
        os.mkdir(saving_folder)
        print("+ Creando carpeta tracking/")
    else:
        print("Carpeta tracking/ ENCONTRADA")


    # Obtenemos la lista de dispositivos y la formateamos
    listDone = False
    while not listDone:
        try:
            deviceList = blapi.getNearDevices() # comprobar si es lista o dicc
            if len(deviceList) > 0:
                listDone=True
            else:
                print("[!] No hay dispositivos al alcance.")
        except:
            print("[!] Error al buscar los dispositivos cercanos.")

    paramList = list(deviceList.items())

    print("Num Devices: ", len(deviceList))
    print("paramList:\n" + str(paramList) + "\n\n")

    # Montamos el pool de trabajo
    try:
        p = multiprocessing.Pool(len(deviceList))
        solus = p.map(f,paramList)
        p.close()
        p.join()
        del p
    except Exception as e:
        print(e)






#######  INICIO  #######
if __name__ == "__main__":
    while True:
        print("===========================================================================================")
        # Guardamos el timestamp
        t1 = time.time()

        # Ejecutamos
        iniciarPool()

        # Guardamos el timestamp
        t2 = time.time()

        # Calculamos la diferencia y el tiempo restante
        diff = t2-t1
        rest = (MAX_DELAY_SECS - diff) if diff < MAX_DELAY_SECS else 0
        print("Iteracion acabada.     Tiempo restante: " , rest)

        # Si rest es positivo, esperamos esa cantidad
        time.sleep(rest)
