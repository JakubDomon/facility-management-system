from enum import unique

from pytz import timezone
from sqlalchemy import ForeignKey
from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class OPCUA(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key = True)
    endpoint = db.Column(db.String(255))
    nodes = db.Column(db.String(255))
    machine_id = db.Column(db.Integer, ForeignKey('machines.id'))
    status = db.Column(db.Boolean, default = False)

class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200))
    dateOfProduction = db.Column(db.Integer)
    montageDate = db.Column(db.DateTime(timezone = True))
    addDate = db.Column(db.DateTime(timezone = True), default = func.now())
    addedBy = db.Column(db.Integer, db.ForeignKey('user.id'))
    opcua = db.relationship('OPCUA', uselist=False, backref='machines', cascade="all, delete-orphan")

## MANY TO ONE RELATIONSHIP ROLES - USER
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    empNb = db.Column(db.Integer, unique=True)
    empName = db.Column(db.String(255))
    password = db.Column(db.String(255))
    confirmed_at = db.Column(db.DateTime(timezone=True), default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    users = db.relationship('User', backref='role')
    