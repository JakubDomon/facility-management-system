from email.policy import default
from time import timezone

from sqlalchemy import true
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key = true)
    manufacturer = db.Column(db.String(200))
    approxProduction = db.Column(db.Integer)
    montageDate = db.Column(db.DateTime(timezone = True))
    addedBy = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    empNb = db.Column(db.String(15), unique = True)
    password = db.Column(db.String(25))
    isAdmin = db.Column(db.Boolean)
    createDate = db.Column(db.DateTime(timezone = True),default=func.now())
    addedMachines = db.relationship('Machine')


    