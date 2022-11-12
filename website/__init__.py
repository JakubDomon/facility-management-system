from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_apscheduler import APScheduler
from website.query import QueryMachines
from pymongo import MongoClient
from website.openweathermap import OpenWeatherMapQuery


API_KEY = '99069dfe999ff748e8d4fbc0c1678b2a'
city = 'Rzeszów'

# CREATE MONGODB INSTANCE
mongoDatabase = MongoClient('localhost', 27017)
# CREATE DATABASE AND COLLECTION
database = mongoDatabase.SCADA
collection = database.PLC
weatherCollection = database.weather
data = database.data

OWM = OpenWeatherMapQuery(city, API_KEY, weatherCollection)

## QUERYMACHINES
queryMachines = QueryMachines()
## SQLAlchemy instance and SQLite file name
db = SQLAlchemy()
DB_NAME = 'database1.db'

# SCHEDULER INSTANCE
scheduler = APScheduler()

def create_app():
    
    ## INITIALIZATION
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'JustRandomSecretKeyLol'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    ## SQLite INIT WITH APP
    db.init_app(app)

    from .views import views
    from .auth import auth

    ## URL ROUTING - VIEWS AND AUTHORIZATION
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Role

    # CREATE DATABASE
    with app.app_context():
        db.create_all()

    # SCHEDULER CONFIG
    scheduler.api_enabled = True
    scheduler.init_app(app=app)

    # FLASK-USER LOGIN INSTANCE
    login_manager = LoginManager()
    # FLASK-USER CONFIG
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app