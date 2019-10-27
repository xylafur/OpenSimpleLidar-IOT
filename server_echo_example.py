import socket

def convert_from_bytes(obj):
    """ Here we will just assume that the bytes we are recieveing are a string
    """
    return obj.decode('utf-8')

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 20

# Create a socket and then bind it to the ip / port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

s.settimeout(.5)

# Listen for incoming connections.  This puts the socket in server mode
s.listen(1)

conn, client_addr = s.accept()
print("Connection address: {}".format(client_addr))

try:
    while 1:
        # there is data from the sender, receive it and store in variable
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        # Echo back to the sender
        print("Recieved data: {}".format(convert_from_bytes(data)))
        conn.send(data)

# No matter what happens we want to close the connection
finally:
    print("Cleaning connection")
    conn.close()
