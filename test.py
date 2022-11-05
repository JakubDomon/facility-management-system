from opcua import Client

clients = []

clients.append(Client('opc.tcp://192.168.0.55:4840'))
clients.append(Client('opc.tcp://192.168.0.52:4840'))
clients.append(Client('opc.tcp://192.168.0.55:4822'))

print(clients)