import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
# server_address = ('18.221.174.251', 8080)
server_address = ('18.221.174.251', 8080)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send Gps data
    # message = b'This is our message. It is very long but will only be transmitted in chunks of 16 at a time'
    message = '{ "name":"John", "age":30, "city":"New York"}'
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
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()