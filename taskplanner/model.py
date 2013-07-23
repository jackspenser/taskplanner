from flask.ext.sqlalchemy import SQLAlchemy
import base64
import os
import datetime
from taskplanner import app
from pbkdf2 import PBKDF2

db = SQLAlchemy(app)

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.UniqueConstraint('user_id', 'role_id', name='uix_user_role')
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
    tasks = db.relationship('Task', backref='owner', lazy='dynamic')
    
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
    
    @property
    def fullname(self):
        return "{0} {1}".format(self.fname, self.lname)
    
    
    def __repr__(self):
        return '<User %r>' % self.username
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Role %r>' % self.name

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(100), unique=True)
    company = db.Column(db.String(100))
    projects = db.relationship('Project', backref='client',
                               lazy='dynamic')
    
    def __repr__(self, ):
        return "<Client %r (self.email)>" % (self.name, self.email)
    
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    percent_complete = db.Column(db.Integer)
    complete_date = db.Column(db.Date)
    tasks = db.relationship('Task', backref='project', lazy='dynamic')
    
    def __repr__(self, ):
        return "<Project %r - %r>" % (self.title, self.client.name)
    
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    percent_complete = db.Column(db.Integer)
    complete_date = db.Column(db.Date)
    notes = db.relationship('TaskNote', backref='task', lazy='dynamic')
    
    def __repr__(self):
        return "<Task %r>" % self.title
    
class TaskNote(db.Model):
    __tablename__ = 'tasknotes'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))

def initialize_db():
    db.create_all()
    j = User('jack', 'password')
    j.fname = 'Jack'
    j.lname = 'Spenser'
    j.email = 'jack.spenser@gmx.us'
    admin = Role('admin')
    j.roles.append(admin)
    db.session.add(j)
    db.session.commit()

    


