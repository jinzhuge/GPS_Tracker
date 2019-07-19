
import socket
import json
import datetime
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
db = myclient['GPS_database']
collection = db['GPS_info']


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 8080)
# print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming gps device connections
sock.listen(5)

while True:
    # Wait for a gps device connection
    print('waiting for a Gps Device connection')
    connection, client_address = sock.accept()
    try:
        # print('connection from', client_address)
        i=0;
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(4096)

            # data = json.loads(response_data.decode("utf-8"))
            # data = json.loads(resp_parsed)


            if data:
                # print('sending data back to the client')
                #
                # if sys.version_info < (3, 0):
                #     data = bytes(data)
                # else:
                #     data = bytes(data, 'utf8')

                connection.sendall(data)
                data = str(data)
                print(data)
                i = i+1
                # insert gps data in MongoDB
                post = {"id": i,
                        "gps_info": data,
                        "date": datetime.datetime.utcnow()}

                x = collection.insert_one(post)

            else:
                # print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        # print("Closing current connection")
        connection.close()