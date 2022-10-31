from time import sleep
from opcua import Client
from pymongo import MongoClient
import datetime

def read_input_value(nodeID, client):
    clientNode = client.get_node(nodeID)
    clientNodeVal = clientNode.get_value()
    return clientNodeVal

def create_Mongo(host, port):
    ## CREATE MONGODB INSTANCE
    mongoClient = MongoClient(host,port)

    ## CREATE DATABASE AND COLLECTION
    mongoDB = mongoClient.SCADA
    mongoDBcollection = mongoDB.PLC
    
    return mongoDBcollection

def create_clients(endpoints):
    clients = []

    for i in endpoints:
        clients.append(Client(i))
    
    return clients

def connect_clients(clients):
    for clients in clients:
        if True:
            try:
                clients.connect()
            except:
                print("Błąd połączenia z PLC: " + str(clients))

def saveOPC_data(names, clients, nodesID, mongoCollection):
    nodeIndex = 0

    for clients in clients:
        readVal = read_input_value(nodesID[nodeIndex], client=clients)

        print(readVal)
        post = {
            "name": names[nodeIndex],
            "time": datetime.datetime.utcnow(),
            "data1": readVal[0],
            "data2": readVal[1]
        }

        nodeIndex += 1

        mongoCollection.insert_one(post)
        mongoCollection.delete_many({'time': {"$lt" :  datetime.datetime.utcnow() - datetime.timedelta(minutes=1)}})