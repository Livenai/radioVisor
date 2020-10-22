import decawave_ble

####################   API   ####################


def readPos(device):
    """ Devuelve la posicion en un vector de 3: [x, y, z] """
    try:
        location = decawave_ble.get_location_data(device)
        x = location["position_data"]["x_position"]
        y = location["position_data"]["y_position"]
        z = location["position_data"]["z_position"]
        return [x,y,z]
    except:
        return [9999,9999,9999]


def getNearDevices():
    """ Devuelve un diccionario con los dispositivos cercanos """
    return decawave_ble.scan_for_decawave_devices()


####################   MAIN   ####################

test = False

if test:
    device_list = getNearDevices()
    print("getNearDevices() result: ", device_list)
    for key in device_list:
        print("readPos() result:        ", readPos(device_list[key]))
