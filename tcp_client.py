import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
# server_address = ('18.221.174.251', 8080)
server_address = ('192.168.1.4', 8080)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # gps data
    message = '!1,865472032140613;'
    if sys.version_info < (3, 0):
        data = bytes(message)
    else:
        data = bytes(message, 'utf8')

    print(str(message))
    sock.sendall(data)

    # Look for the response from tcp server
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        recvData = sock.recv(16)
        amount_received += len(recvData)
        print(str(recvData))

finally:
    print('closing socket')
    sock.close()
