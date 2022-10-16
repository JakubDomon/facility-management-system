from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key = True)
    manufacturer = db.Column(db.String(200))
    approxProduction = db.Column(db.Integer)
    montageDate = db.Column(db.DateTime(timezone = True))
    addedBy = db.Column(db.Integer, db.ForeignKey('user.id'))

## MANY TO ONE RELATIONSHIP ROLES - USER
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    empNb = db.Column(db.Integer, unique = True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime(timezone=True), default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    users = db.relationship('User', backref='role')
    