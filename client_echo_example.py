import socket

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

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20
MESSAGE = "Hello World!"

data = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# As a client we need to connect our socket to an existing address
s.connect((TCP_IP, TCP_PORT))

try:
    s.sendall(convert_to_bytes(MESSAGE))

    data = s.recv(BUFFER_SIZE)
finally:
    print("Closing socket")
    s.close()

# since we have the finally, if we hit an exception data might be none
if data:
    print("Recieved Data: {}".format(convert_from_bytes(data)))
