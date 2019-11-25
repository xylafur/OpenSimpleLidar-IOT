import socket

import queue

import string

from threading import Thread


def convert_to_bytes(obj):
    """
        Python can encode multiple different object types, but if it is a string then you have to
        pass in an encoding.  This function just passes in an encoding of utf-8 if the object is
        an string
    """
    return bytes(obj, 'utf-8') if isinstance(obj, str) else bytes(obj)

def convert_from_bytes(obj):
    """ Here we will just assume that the bytes we are recieveing are a string
    """
    return obj.decode('utf-8')

ESP_IP = '192.168.0.101'
ESP_PORT = 5555

LABVIEW_PORT = 5005

BUFFER_SIZE = 728
MESSAGE = "Hello World!"

data = None

running = True

data_queue = queue.Queue()

# As a client we need to connect our socket to an existing address

from lidar_server import remove_header, remove_status, remove_rotation, \
                         swap_endianness, convert_to_byte_string

def write_to_labview():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", LABVIEW_PORT))

    print("Created server at {}:{}".format("localhost", LABVIEW_PORT))

    s.listen(1)
    s.settimeout(1)

    while running:
        # no guarantee but /shrug
        if data_queue.qsize() > 0:

            lidar_data = data_queue.get()
            try:
                conn, client_address = s.accept()
            except socket.timeout:
                continue

            try:
                lidar_data = remove_header(lidar_data)
                lidar_data = remove_status(lidar_data)
                lidar_data = remove_rotation(lidar_data)
                
                lidar_data = swap_endianness(lidar_data)
                lidar_data = convert_to_byte_string(lidar_data)
                print("Sending data of {} bytes".format(len(lidar_data)))

                conn.sendall(lidar_data)


            finally:
                conn.close()




def read_from_esp():
    while running:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to ESP32")
        s.connect((ESP_IP, ESP_PORT))

        try:
            print("Connected")
            data = s.recv(BUFFER_SIZE)
            print("Got data of {} bytes".format(len(data)))
            data_queue.put(data)

        finally:
            print("Closing socket")
            s.close()

if __name__ == '__main__':
    esp_thread = Thread(target=read_from_esp)
    labview_thread = Thread(target=write_to_labview)

    try:
        esp_thread.start()
        labview_thread.start()
        while 1:
            pass
    except KeyboardInterrupt:
        print("User issues Ctrl^C! Stopping program")
    finally:
        running = False

        esp_thread.join()
        labview_thread.join()




