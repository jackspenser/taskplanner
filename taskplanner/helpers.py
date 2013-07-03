from taskplanner import app
from taskplanner.model import db, User
from flask import request, session, redirect, url_for, abort
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def getuser():
    if session.get('user'):
        return User.query.filter_by(username=session.get('user')).one()
    else:
        abort(404)
    
def in_role(role):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            user = getuser()
            if not user.has_role(role):
                abort(401)
            return f(*args, **kwargs)
        return wrapped_f
    return wrap
        
    
