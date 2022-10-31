from website import create_app, db, scheduler
from website.models import Role, User
from werkzeug.security import generate_password_hash
from website.opc_client.client import connect_clients, saveOPC_data, create_Mongo, create_clients
from flask_apscheduler import APScheduler
import atexit

# UTWORZENIE INSTANCJI
app = create_app()

names = ["Peelce1"]
endpoints = ["opc.tcp://192.168.0.51:4840"]
nodesID = ["ns=4;i=4"]

@app.before_first_request
def before_first_request():
    if not (db.session.query(db.exists().where(Role.name == 'admin')).scalar() and db.session.query(db.exists().where(Role.name == 'user')).scalar()):
        newRole1 = Role(name = "admin")
        newRole2 = Role(name = "user")
        firstAdminUser = User(empNb=1234567, empName = 'Admin Admin', password= generate_password_hash("firstAdmin"),role_id = 1)
        thingsToAdd = [newRole1, newRole2, firstAdminUser]
        db.session.add_all(thingsToAdd)
        db.session.commit()

collection = create_Mongo('localhost', 27017)
clients = create_clients(endpoints)
connect_clients(clients)

@scheduler.task('interval', id='task1', seconds=2, misfire_grace_time=900)
def task_every_2seconds():
    saveOPC_data(names, clients, nodesID, collection)

mongoDB = create_Mongo('localhost', 27017)

# START APKI
if __name__ == '__main__':
    if scheduler.state == 0:
        scheduler.start()
    app.run(debug=True)
    
    atexit.register(lambda: scheduler.stop())