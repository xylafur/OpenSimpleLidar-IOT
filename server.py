"""
    Lidar Packet Info:
        This data protocol is used by "lidar4_main_code" firmware. Single data packet consists of parts:

            Header: [0xAA, 0xBB, 0xCC, 0xDD] - 4 bytes.
            Status: [LSB + MSB] - (16-bit value) - 2 bytes.
            Duration of the last turn: [LSB + MSB] - (16-bit value is ms) - 2 bytes.
            Distance data: [(LSB + MSB)*360] - (360 x 16-bit values) - 720 bytes.

        Total number of bytes in this packet - 728.

        Every "distance data value" is a 16-bit unsigned value, corresponding to a certain rotation
        angle. In fact "distance data value" is a position of the laser light spot at the TSL1401.
        High level software must convert that values to a real distance values.
"""

###############################################################################
#   Shared variables and such.  These are used by both threads
###############################################################################
import queue

data_queue = queue.Queue()

running = True

def get_data_from_buffer():
    """
        - Gets the next data packet from the buffer
        - Removes it from the buffer
        - Returns the packet as a bytes object
    """
    # TODO: Real functionality needs to be implemented
    return data_queue.get()


###############################################################################
#   Functions to read from LIDAR
###############################################################################
def generate_mock_lidar_data(device):
    return b'Hello world'

def read_data_from_uart(device):
    """
        - In linux the terminal driver will buffer input even if the device it is not opened
            - this means we should just be able to read from where we last read in linux
    """
    pass

def get_data(device, mock=True):
    return generate_mock_lidar_data(device) if mock else read_data_from_uart(device)

def queue_data(data):
    data_queue.put(data)

def get_serial_device(device):
    """
        set up and open the given serial device so that it is read to be used
    """
    pass


def lidar_main(args):
    # Eventually I think we will have to add windows support
    device = get_serial_device(args.device)
    try:
        # Just continually read from UART and move data to our buffer
        while running:
            queue_data(get_data(device))
    finally:
        pass


###############################################################################
#   Functions to send info to client over TCP
###############################################################################
import socket

def socket_main(args):
    address = args.address
    port = args.port
    buffer_size = args.buffer_size

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((address, port))

    if args.debug:
        print("Created server at {}:{}".format(address, port))

    s.listen(1)
    s.settimeout(args.socket_timeout)

    while running:
        # Accept a connection from a client
        try:
            conn, client_address = s.accept()
        except socket.timeout:
            continue

        try:
            # TODO: Make sure that all data is actually sent
            to_send = get_data_from_buffer()

            if args.debug:
                print("Sending {!r}".format(to_send))

            conn.send(to_send)

        finally:
            conn.close()


###############################################################################
#   Main function and argument parsing
###############################################################################
from threading import Thread
import argparse

parser = argparse.ArgumentParser(
        description="Program to read from LIDAR attached over UART and transmit to LabView over TCP")

parser.add_argument("-a", "--address", default="localhost", type=str)
parser.add_argument("-p", "--port", default=5005, type=int)
parser.add_argument("-b", "--buffer_size", default=728, type=int)
parser.add_argument("-s", "--device", default="/dev/ttyUSB0", type=str)
parser.add_argument("-d", "--debug", action="store_true", default=False)
parser.add_argument("-m", "--mock", action="store_true", default=False)
parser.add_argument("-t", "--socket_timeout", type=float, default=1)

def main():
    global running

    args = parser.parse_args()
    # Start get data in a thread
    # Start ther server in a thread
    lidar_thread = Thread(target=lidar_main, args=(args,))
    tcp_thread = Thread(target=socket_main, args=(args,))

    if args.debug:
        print("Starting LIDAR and TCP threads")

    try:
        lidar_thread.start()
        tcp_thread.start()
        while 1:
            pass
    except KeyboardInterrupt:
        print("User issues Ctrl^C! Stopping program")
    finally:
        running = False

        lidar_thread.join()
        tcp_thread.join()

    if args.debug:
        print("End of Program, thread status:")
        print("   LIDAR: {}".format(lidar_thread.is_alive()))
        print("   TCP:   {}".format(tcp_thread.is_alive()))


if __name__ == '__main__':
    main()
