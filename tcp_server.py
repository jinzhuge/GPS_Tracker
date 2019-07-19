import socket
import datetime
import pymongo


def convertRecvData(str):

    return;


def checkTypeData(str):
    result = [x.strip() for x in str.split(',')]
    insert_data = {}
    if result[0] == '!1':
        insert_data = {
            "Protocol": result[0],
            "GPS_imei": result[1]
        }
    elif result[0] == '!D':
        insert_data = {
            "Protocol": result[0],
            "Date": result[1],
            "Time": result[2],
            "Latitude": result[3],
            "Longitude": result[4],
            "Speed": result[5],
            "Direction": result[6],
            "EventCode": result[7],
            "Altitude": result[8],
            "Battery": result[9],
            "SatelliteUse": result[10],
            "SatelliteNum": result[11],
            "Reserved": result[12]
        }
    elif result[0] == '!3':
        insert_data = {
            "Protocol": result[0],
            "response": result[1]
        }
    elif result[0] == '!4':
        insert_data = {
            "Protocol": result[0],
            "responseFunction": result[1]
        }
    elif result[0] == '!7':
        insert_data = {
            "Protocol": result[0],
            "firmwre_version": result[1],
            "signal_strength": result[2]
        }
    elif result[0] == '!5':
        insert_data = {
            "Protocol": result[0],
            "CSQ":result[1],
            "GPS_location": result[2]
        }
    manageDatabase(insert_data)
    return;


def printme(str):
    print(str)
    return ;


def manageDatabase(insert_data):

    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    db = myclient['GPS_database']
    collection = db['GPS_info']

    x = collection.insert_one(insert_data)
    return;


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 8080)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
# Listen for incoming gps device connections
sock.listen(5)

while True:
    # Wait for a gps device connection
    print('waiting for a Gps Device connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        i = 0
        # Receive the data in small chunks and retransmit it
        while True:
            recvDataFromClient = connection.recv(4096)
            # data = json.loads(response_data.decode("utf-8"))
            # data = json.loads(resp_parsed)

            if recvDataFromClient:
                connection.sendall(recvDataFromClient)
                recvDataString = recvDataFromClient.decode("utf-8")
                print(recvDataString)
                # recvDataString = str(recvDataFromClient, 'utf-8')
                checkTypeData(recvDataString)

            else:
                # print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        print("Closing current connection")
        connection.close()

