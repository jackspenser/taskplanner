from flask.ext.sqlalchemy import SQLAlchemy
import base64
import os
from taskplanner import app
from pbkdf2 import PBKDF2

db = SQLAlchemy(app)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    )

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(100), unique=True)
    salt = db.Column(db.String(45))
    pw_hash = db.Column(db.String(80))
    roles = db.relationship('Role', secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'))
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        
    def set_password(self, password):
        if not self.salt:
            self.salt = base64.b64encode(os.urandom(32))
        self.pw_hash = PBKDF2(password, self.salt, 10000).hexread(32)
    
    def check_password(self, password):
        return PBKDF2(password, self.salt, 10000).hexread(32) == self.pw_hash
    
    def has_role(self, rolename):
        rolenames = [x.name for x in self.roles]
        if rolenames.count(rolename) > 0:
            return True
        else:
            return False
    
    def __repr__(self):
        return '<User %r>' % self.username
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Role %r>' % self.name
    


