from website import create_app, db, scheduler, OWM, weatherCollection, queryMachines, collection
from website.models import Role, User, Machine, OPCUA
from werkzeug.security import generate_password_hash
from opcua import Client
import atexit
import socket
import datetime

# UTWORZENIE INSTANCJI
app = create_app()
clients = {}

@app.before_first_request
def before_first_request():
    if not (db.session.query(db.exists().where(Role.name == 'admin')).scalar() and db.session.query(db.exists().where(Role.name == 'user')).scalar()):
        newRole1 = Role(name = "admin")
        newRole2 = Role(name = "user")
        firstAdminUser = User(empNb=1234567, empName = 'Admin Admin', password= generate_password_hash("firstAdmin"),role_id = 1)
        thingsToAdd = [newRole1, newRole2, firstAdminUser]
        db.session.add_all(thingsToAdd)
        db.session.commit()

        data = OWM.get_temp_icon()
        weatherCollection.insert_one(data)


with app.app_context():
    names, endpoints, nodesID = queryMachines.get_all(Machine)
    if not clients:
        for endpoints in endpoints:
            clients[endpoints] = Client(endpoints)
    
    for client in clients.values():
        print(client.server_url.geturl())

@scheduler.task('interval', id='task1', seconds=3, misfire_grace_time=900)
def connect():
    global clients
    with app.app_context():
        names, endpoints, nodesID = queryMachines.get_all(Machine)

        #  CHECK IF THERE IS A NEW INSTANCE ADDED
        if not len(clients.keys()) == len(endpoints):
            missingClientsEndpoints = []
            for endpoints in endpoints:
                if not endpoints in clients:
                    missingClientsEndpoints.append(endpoints)

            for endpoints in missingClientsEndpoints:
                clients[endpoints] = Client(endpoints)

        for cli in clients.values():
            if cli.keepalive is None:
                try:
                    cli.connect()
                    print('Połączono ze sterownikiem: ' + str(cli.server_url.geturl()))
                except:
                    print('Błąd połączenia ze sterownikiem: ' + str(cli.server_url.geturl()))

@scheduler.task('interval', id='task2', seconds=1, misfire_grace_time=900)
def save_data():
    global clients
    with app.app_context():
        names, endpoints, nodesID = queryMachines.get_all(Machine)
        
        # CHECK IF THERE IS A DELETED INSTANCE
        if not len(clients.keys()) == len(endpoints):
            missingEndpoints = []
            for client in clients.keys():
                if not client in endpoints:
                    missingEndpoints.append(client)
            print(missingEndpoints)

            for endpoints in missingEndpoints:
                clients.pop(endpoints)

        for cli in clients.values():
            if not cli.keepalive is None:
                machine = OPCUA.query.filter_by(endpoint = cli.server_url.geturl()).first()
                nodeVal = cli.get_node(machine.nodes).get_value()
                post = {
                    "machine_id": machine.machine_id,
                    "time": datetime.datetime.utcnow(),
                    "data1": nodeVal[0],
                    "data2": nodeVal[1]
                }

                collection.insert_one(post)
                collection.delete_many({'time': {"$lt" :  datetime.datetime.utcnow() - datetime.timedelta(minutes=1)}})

@scheduler.task('interval', id='task3', seconds=120, misfire_grace_time=900)
def weather():
    data = OWM.get_temp_icon()
    weatherCollection.insert_one(data)

# DO SKOŃCZENIA
# @scheduler.task('interval', id='task3', seconds=5, misfire_grace_time=900)
# def prepare_data():
#     machines = Machine.query.order_by(Machine.id).all()
    
#     # PREPARE DATA IN EVERY MACHINE
#     for machine in machines:

# START APKI
if __name__ == '__main__':
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("127.0.0.1", 47200))
    except socket.error:
        print("Scheduler już działa")
    else:
        scheduler.start()
        print("Scheduler wystartował")
    
    app.run(debug=True)
    
    atexit.register(lambda: scheduler.stop())