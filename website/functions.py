from os import path
from FlaskWebApp.website import DB_NAME
from django import db
import models

# DATABASE FUNCTIONS:

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
